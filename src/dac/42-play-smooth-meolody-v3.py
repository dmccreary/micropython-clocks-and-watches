from machine import Pin, I2S
import struct
import math
from utime import sleep_ms, ticks_ms, ticks_diff

# Pin Definitions
BCK_PIN = 16
WS_PIN = 17
SD_PIN = 18

# Audio parameters - increased sample rate
SAMPLE_RATE = 44100  # Standard CD quality
BUFFER_SIZE = 2048   # Larger buffer

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

# Simple melody
MELODY = [
    ('C4', 300), ('E4', 300), ('G4', 300),
    ('C5', 600),
    ('G4', 200), ('E4', 200), ('C4', 600),
    ('REST', 300),
    ('G4', 300), ('F4', 300), ('E4', 300),
    ('D4', 300), ('C4', 600),
]

def make_tone_buffer(frequency):
    """Create a filtered sine wave buffer"""
    if frequency == 0:  # For REST
        return bytearray(BUFFER_SIZE * 2)
    
    # Calculate samples needed for complete cycles
    samples_per_cycle = SAMPLE_RATE / frequency
    num_cycles = max(1, int(BUFFER_SIZE / samples_per_cycle))
    adjusted_buffer_size = int(num_cycles * samples_per_cycle)
    if adjusted_buffer_size > BUFFER_SIZE:
        adjusted_buffer_size = BUFFER_SIZE
    
    buffer = bytearray(adjusted_buffer_size * 2)
    
    # Parameters for smoother sound
    amplitude = 0.00004  # Greatly reduced amplitude to 1%
    prev_value = 0   # For smoothing
    
    for i in range(0, adjusted_buffer_size * 2, 2):
        # Generate basic sine wave
        phase = (i // 2) / samples_per_cycle * 2 * math.pi
        current_value = math.sin(phase)
        
        # Apply simple low-pass filter
        filtered_value = 0.9 * current_value + 0.1 * prev_value
        prev_value = filtered_value
        
        # Scale and convert to integer
        value = int(32767 * amplitude * filtered_value)
        
        # Soft clipping to reduce distortion
        if value > 32000:
            value = 32000
        elif value < -32000:
            value = -32000
            
        # Pack into buffer
        struct.pack_into("<h", buffer, i, value)
    
    return buffer

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
    ibuf=4096  # Much larger internal buffer
)

print("Playing filtered melody... Press Ctrl+C to stop")

try:
    while True:
        for note_name, duration in MELODY:
            print(f"\nPlaying {note_name} for {duration}ms")
            
            frequency = NOTES[note_name]
            buffer = make_tone_buffer(frequency)
            
            start_time = ticks_ms()
            while ticks_diff(ticks_ms(), start_time) < duration:
                audio_out.write(buffer)
                sleep_ms(10)
                print(".", end="")
            
            # Gentle fade between notes
            sleep_ms(50)
        
        sleep_ms(1000)
            
except KeyboardInterrupt:
    print("\nStopping...")
finally:
    audio_out.deinit()
    print("Test complete")