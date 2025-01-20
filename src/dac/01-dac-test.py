# Test program for PCM5102A Digital to Analog Converter

from machine import Pin, I2S, PWM
import math
import struct

# Pin assignments for PCM5102A listed from lowest pin to highest pin
SD_PIN = 13     # Serial Data (DIN)
BCK_PIN = 14    # Bit Clock (must be sequential with WS)
WS_PIN = 15     # Word Select/LCK (must be BCK+1)
SCK_PIN = 16    # System Clock output to DAC's SCK

# Setup system clock using PWM
# PCM5102A typically needs a system clock of 12.288MHz for 48kHz sampling
system_clock = PWM(Pin(SCK_PIN))
system_clock.freq(12288000)  # 12.288MHz
system_clock.duty_u16(32768) # 50% duty cycle

# I2S configuration
SAMPLE_RATE = 48000  # Common sample rate that works well with 12.288MHz system clock
BITS_PER_SAMPLE = 16
BUFFER_LENGTH_IN_BYTES = 2048

# Create I2S object
audio_out = I2S(
    1,                          # I2S peripheral ID
    sck=Pin(BCK_PIN),          # Bit clock
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
    
    # Create buffer for samples
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
    print(f"Playing {frequency}Hz tone...")
    
    # Generate the sine wave buffer
    buffer = generate_sine_wave(frequency, duration_ms)
    
    # Write the buffer to I2S
    audio_out.write(buffer)
    
    # Clear the buffer by writing silence
    silence = bytearray(BUFFER_LENGTH_IN_BYTES)
    audio_out.write(silence)

def test_sequence():
    """Play a test sequence of tones"""
    # Test frequencies (A4 scale)
    frequencies = [440, 494, 523, 587, 659, 698, 784, 880]  # A4 to A5
    
    print("Starting test sequence...")
    for freq in frequencies:
        play_tone(freq, 500)  # Play each tone for 500ms
        
    print("Test sequence complete")

# Connection guide printed at startup
print("""
PCM5102A DAC Connection Guide:
-----------------------------
DIN  → GPIO 13 (Data In)
BCK  → GPIO 14 (Bit Clock)
LCK  → GPIO 15 (Word Select)
SCK  → GPIO 16 (System Clock)
VIN  → 3.3V
GND  → Ground
LINE OUT → Speaker/Amplifier

Starting I2S DAC test...
""")

# Run the test
while True:
    print('starting testing')
    test_sequence()