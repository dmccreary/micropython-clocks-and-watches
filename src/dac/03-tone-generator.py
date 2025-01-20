from machine import Pin, I2S
import struct
import math
from time import sleep_ms

# Pin Definitions
BCK_PIN = 16      # Connect to BCK on DAC (Bit Clock)
WS_PIN = 17       # Connect to LCK on DAC (Word Select)
SD_PIN = 18       # Connect to DIN on DAC (Data Input)

# Audio parameters
SAMPLE_RATE = 16000
TONE_FREQUENCY = 5000  # A4 note (440 Hz)
BUFFER_SIZE = 128

# Create a sine wave buffer for smoother sound
buffer = bytearray(BUFFER_SIZE * 2)
for i in range(0, BUFFER_SIZE, 2):
    # Calculate sine wave value
    t = i / 2 / SAMPLE_RATE  # Time at this sample
    value = int(32767 * 0.5 * math.sin(2 * math.pi * TONE_FREQUENCY * t))
    struct.pack_into("<h", buffer, i, value)

print(f"""
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

Starting audio test...
Playing {TONE_FREQUENCY} Hz tone...
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
    ibuf=256
)

print("Press Ctrl+C to stop")

try:
    while True:
        audio_out.write(buffer)
        sleep_ms(10)
        print(".", end="")
        
except KeyboardInterrupt:
    print("\nStopping...")
finally:
    audio_out.deinit()
    print("Test complete")