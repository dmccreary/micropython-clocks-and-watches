from machine import Pin, I2S
import struct
from time import sleep_ms

# Pin Definitions
BCK_PIN = 16      # Connect to BCK on DAC (Bit Clock)
WS_PIN = 17       # Connect to LCK on DAC (Word Select)
SD_PIN = 18       # Connect to DIN on DAC (Data Input)

# Create a simple square wave buffer
BUFFER_SIZE = 128
buffer = bytearray(BUFFER_SIZE * 2)
for i in range(0, BUFFER_SIZE, 2):
    value = 32767 if (i // 2) % 2 == 0 else -32767
    struct.pack_into("<h", buffer, i, value)

print("""
PCM5102A DAC Connection Guide:
-----------------------------
SCK  → GND (Ground the system clock pin)
BCK  → GPIO 16 (Bit Clock)
LCK  → GPIO 17 (Word Select)
DIN  → GPIO 18 (Data In)
XSMT → GPIO 19 (Mute Control)
FMT  → 3.3V (I2S Mode)
VIN  → 3.3V
GND  → Ground
LINE OUT → Speaker/Amplifier

Starting audio test...
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
    rate=16000,
    ibuf=256
)

print("Playing tone... Press Ctrl+C to stop")

try:
    while True:
        audio_out.write(buffer)
        sleep_ms(10)
        print(".", end="")
        
except KeyboardInterrupt:
    print("\nMuting DAC...")
    sleep_ms(100)
    print("Stopping...")
finally:
    audio_out.deinit()
    print("Test complete")