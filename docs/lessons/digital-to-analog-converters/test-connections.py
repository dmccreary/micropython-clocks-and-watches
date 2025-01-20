from machine import Pin, I2S
import math
import struct

# I2S configuration
SAMPLE_RATE = 44100
BITS_PER_SAMPLE = 16
BUFFER_LENGTH_IN_BYTES = 2048

# Pin assignments for PCM5102A
# Note: WS pin must be SCK pin + 1 for Pico I2S
SCK_PIN = 14   # Serial Clock (BCK)
WS_PIN = 15    # Word Select (LCK) - Must be SCK+1
SD_PIN = 13    # Serial Data (DIN)

# Create I2S object
audio_out = I2S(
    1,                          # I2S peripheral ID
    sck=Pin(SCK_PIN),          # Serial clock
    ws=Pin(WS_PIN),            # Word select
    sd=Pin(SD_PIN),            # Serial data
    mode=I2S.TX,               # Transmit mode
    bits=BITS_PER_SAMPLE,      # Sample size
    format=I2S.MONO,           # Single channel
    rate=SAMPLE_RATE,          # Sample rate
    ibuf=BUFFER_LENGTH_IN_BYTES # Internal buffer size
)

def generate_sine_wave(frequency, duration_ms):
    """Generate a sine wave of given frequency and duration"""
    samples_per_cycle = SAMPLE_RATE // frequency
    num_samples = (SAMPLE_RATE * duration_ms) // 1000
    
    # Create buffer for one period
    buffer = bytearray(num_samples * 2)  # 2 bytes per sample for 16-bit
    
    # Generate sine wave
    for i in range(num_samples):
        # Calculate sine value (-1 to 1)
        sine_value = math.sin(2 * math.pi * i / samples_per_cycle)
        # Scale to 16-bit signed integer range (-32768 to 32767)
        sample_value = int(sine_value * 32767)
        # Pack into buffer as 16-bit signed integer
        struct.pack_into("<h", buffer, i * 2, sample_value)
    
    return buffer

def play_tone(frequency, duration_ms):
    """Play a tone of given frequency for specified duration"""
    # Generate the sine wave buffer
    buffer = generate_sine_wave(frequency, duration_ms)
    
    # Write the buffer to I2S
    audio_out.write(buffer)
    
    # Clear the buffer by writing silence
    silence = bytearray(BUFFER_LENGTH_IN_BYTES)
    audio_out.write(silence)

def test_sequence():
    """Play a test sequence of tones"""
    # Test frequencies
    frequencies = [262, 330, 392, 523]  # C4, E4, G4, C5
    
    print("Playing test sequence...")
    for freq in frequencies:
        print(f"Playing {freq} Hz")
        play_tone(freq, 500)  # Play each tone for 500ms
        
    print("Test sequence complete")

# Run the test
print("Starting I2S DAC test...")
test_sequence()
