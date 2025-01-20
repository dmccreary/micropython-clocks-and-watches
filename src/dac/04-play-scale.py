from machine import Pin, I2S
import struct
import math
from utime import sleep_ms, ticks_ms, ticks_diff

# Pin Definitions
BCK_PIN = 16      # Connect to BCK on DAC (Bit Clock)
WS_PIN = 17       # Connect to LCK on DAC (Word Select)
SD_PIN = 18       # Connect to DIN on DAC (Data Input)

# Audio parameters
SAMPLE_RATE = 16000
BUFFER_SIZE = 512  # Increased buffer size for better frequency reproduction

# Musical notes in correct order
SCALE = [
    ('A4', 440.0),    # A
    ('B4', 493.9),    # B
    ('C5', 523.3),    # C
    ('D5', 587.3),    # D
    ('E5', 659.3),    # E
    ('F5', 698.5),    # F
    ('G5', 784.0),    # G
    ('A5', 880.0)     # A (octave up)
]

def make_tone_buffer(frequency):
    """Create a buffer with complete cycles of the sine wave"""
    # Calculate how many samples we need for one complete cycle
    samples_per_cycle = SAMPLE_RATE / frequency
    # Calculate how many complete cycles we can fit in our buffer
    num_cycles = max(1, int(BUFFER_SIZE / samples_per_cycle))
    # Adjust buffer size to fit complete cycles
    adjusted_buffer_size = int(num_cycles * samples_per_cycle)
    if adjusted_buffer_size > BUFFER_SIZE:
        adjusted_buffer_size = BUFFER_SIZE
    
    buffer = bytearray(adjusted_buffer_size * 2)  # 2 bytes per sample
    
    # Generate the waveform
    for i in range(0, adjusted_buffer_size * 2, 2):
        # Calculate sine wave value
        sample_pos = (i // 2) / samples_per_cycle * 2 * math.pi
        value = int(32767 * 0.3 * math.sin(sample_pos))
        struct.pack_into("<h", buffer, i, value)
    
    return buffer

print("""
PCM5102A DAC Connection Guide:
-----------------------------
SCK  → GND (Ground the system clock pin)
BCK  → GPIO 16 (Bit Clock)
LCK  → GPIO 17 (Word Select)
DIN  → GPIO 18 (Data In)
FMT  → 3.3V (I2S Mode)
XSMT → 3.3V (Unmute)
VIN  → 3.3V
GND  → Ground
LINE OUT → Speaker/Amplifier

Starting musical scale player...
""")

# Configure I2S
audio_out = I2S(
    0,
    sck=Pin(BCK_PIN),
    ws=Pin(WS_PIN),
    sd=Pin(SD_PIN),
    mode=I2S.TX,
    bits=16,
    format=I2S.MONO,
    rate=SAMPLE_RATE,
    ibuf=1024
)

print("Playing A major scale... Press Ctrl+C to stop")

try:
    while True:
        # Play each note in the scale
        for note_name, frequency in SCALE:
            print(f"\nPlaying {note_name} ({frequency:.1f} Hz)")
            
            # Create buffer for this frequency
            buffer = make_tone_buffer(frequency)
            
            # Play the note for half a second
            start_time = ticks_ms()
            while ticks_diff(ticks_ms(), start_time) < 500:
                audio_out.write(buffer)
                sleep_ms(10)
                print(".", end="")
            
            # Brief pause between notes
            sleep_ms(100)
            
except KeyboardInterrupt:
    print("\nStopping...")
finally:
    audio_out.deinit()
    print("Test complete")