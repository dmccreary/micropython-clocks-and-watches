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
BUFFER_SIZE = 512  # Larger buffer for smoother playback

# Note frequencies
NOTES = {
    'C4': 261.63,
    'D4': 293.66,
    'E4': 329.63,
    'F4': 349.23,
    'G4': 392.00,
    'A4': 440.00,
    'B4': 493.88,
    'C5': 523.25,
    'REST': 0
}

# Simple melody: each tuple contains (note_name, duration_ms)
MELODY = [
    ('C4', 300), ('E4', 300), ('G4', 300),  # Ascending arpeggio
    ('C5', 600),                            # Hold high note
    ('G4', 200), ('E4', 200), ('C4', 600),  # Descending
    ('REST', 300),                          # Pause
    ('G4', 300), ('F4', 300), ('E4', 300),  # Walking down
    ('D4', 300), ('C4', 600),               # End phrase
]

def apply_envelope(value, i, buffer_size, attack_samples=100, release_samples=100):
    """Apply attack and release envelope to reduce clicks and pops"""
    if i < attack_samples:
        return value * (i / attack_samples)
    elif i > buffer_size - release_samples:
        return value * ((buffer_size - i) / release_samples)
    return value

def make_tone_buffer(frequency):
    """Create a buffer with complete cycles of the sine wave"""
    if frequency == 0:  # For REST
        return bytearray(BUFFER_SIZE * 2)
        
    # Calculate samples for complete cycles
    samples_per_cycle = SAMPLE_RATE / frequency
    num_cycles = max(1, int(BUFFER_SIZE / samples_per_cycle))
    adjusted_buffer_size = int(num_cycles * samples_per_cycle)
    if adjusted_buffer_size > BUFFER_SIZE:
        adjusted_buffer_size = BUFFER_SIZE
    
    buffer = bytearray(adjusted_buffer_size * 2)
    
    # Generate a smoother waveform
    amplitude = 0.15  # Reduced amplitude for cleaner sound
    
    for i in range(0, adjusted_buffer_size * 2, 2):
        # Basic sine wave
        sample_pos = (i // 2) / samples_per_cycle * 2 * math.pi
        raw_value = math.sin(sample_pos)
        
        # Apply envelope and amplitude
        value = int(32767 * amplitude * 
                   apply_envelope(raw_value, i//2, adjusted_buffer_size))
        
        # Pack into buffer
        struct.pack_into("<h", buffer, i, value)
    
    return buffer

# Configure I2S with higher sample precision
audio_out = I2S(
    0,
    sck=Pin(BCK_PIN),
    ws=Pin(WS_PIN),
    sd=Pin(SD_PIN),
    mode=I2S.TX,
    bits=16,
    format=I2S.MONO,
    rate=SAMPLE_RATE,
    ibuf=2048  # Larger internal buffer
)

print("Playing melody... Press Ctrl+C to stop")

try:
    while True:
        for note_name, duration in MELODY:
            print(f"\nPlaying {note_name} for {duration}ms")
            
            # Create buffer for this frequency
            frequency = NOTES[note_name]
            buffer = make_tone_buffer(frequency)
            
            # Play the note for specified duration
            start_time = ticks_ms()
            while ticks_diff(ticks_ms(), start_time) < duration:
                audio_out.write(buffer)
                sleep_ms(10)
                print(".", end="")
            
            # Longer pause between notes for clearer separation
            sleep_ms(70)
        
        # Pause between repetitions
        sleep_ms(1000)
            
except KeyboardInterrupt:
    print("\nStopping...")
finally:
    audio_out.deinit()
    print("Test complete")