from machine import Pin, I2S
import struct

# Pin Definitions - Only using 3 pins now
BCK_PIN = 16      # Connect to BCK on DAC (Bit Clock)
WS_PIN = 17       # Connect to LCK on DAC (Word Select)
SD_PIN = 18       # Connect to DIN on DAC (Data Input)

# Create a simple square wave buffer
BUFFER_SIZE = 1000
buffer = bytearray(BUFFER_SIZE * 2)
for i in range(0, BUFFER_SIZE, 2):
    value = 32767 if (i // 2) % 2 == 0 else -32767
    struct.pack_into("<h", buffer, i, value)

# Configure I2S
audio_out = I2S(
    0,                      # I2S ID
    sck=Pin(BCK_PIN),      # Bit clock
    ws=Pin(WS_PIN),        # Word select
    sd=Pin(SD_PIN),        # Serial data
    mode=I2S.TX,           # Transmit mode
    bits=16,               # Sample size
    format=I2S.MONO,       # Mono format
    rate=44100,           # Sample rate
    ibuf=BUFFER_SIZE * 8   # Buffer size
)

print("""
PCM5102A DAC Connection Guide:
-----------------------------
SCK  → GND (Ground the system clock pin)
BCK  → GPIO 16 (Bit Clock)
LCK  → GPIO 17 (Word Select)
DIN  → GPIO 18 (Data In)
VIN  → 3.3V
GND  → Ground
FMT  → 3.3V (I2S Mode)
XSMT → 3.3V (Unmute)
LINE OUT → Speaker/Amplifier

Starting square wave test...
You should hear a continuous tone
""")

try:
    while True:
        audio_out.write(buffer)
        print(".", end="")
        
except KeyboardInterrupt:
    print("\nStopping...")
finally:
    audio_out.deinit()
    print("Test complete")