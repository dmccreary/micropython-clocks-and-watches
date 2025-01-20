from machine import Pin, I2S
import struct
from time import sleep_ms

# Pin Definitions
BCK_PIN = 16      # Connect to BCK on DAC (Bit Clock)
WS_PIN = 17       # Connect to LCK on DAC (Word Select)
SD_PIN = 18       # Connect to DIN on DAC (Data Input)

# Create a simple square wave buffer - smaller buffer for better control
BUFFER_SIZE = 512
buffer = bytearray(BUFFER_SIZE * 2)  # 2 bytes per sample
for i in range(0, BUFFER_SIZE, 2):
    value = 32767 if (i // 2) % 2 == 0 else -32767
    struct.pack_into("<h", buffer, i, value)

# Configure I2S with smaller internal buffer
audio_out = I2S(
    0,                      # I2S ID
    sck=Pin(BCK_PIN),      # Bit clock
    ws=Pin(WS_PIN),        # Word select
    sd=Pin(SD_PIN),        # Serial data
    mode=I2S.TX,           # Transmit mode
    bits=16,               # Sample size
    format=I2S.MONO,       # Mono format
    rate=44100,            # Sample rate
    ibuf=BUFFER_SIZE * 2   # Smaller internal buffer
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
Press Ctrl+C to stop
""")

write_count = 0
try:
    while True:
        # Write the buffer and get number of bytes written
        bytes_written = audio_out.write(buffer)
        
        # Add a small delay to prevent buffer overflow
        sleep_ms(5)
        
        # Print status every 100 writes
        write_count += 1
        if write_count % 100 == 0:
            print(".", end="")
            
except KeyboardInterrupt:
    print("\nStopping...")
finally:
    audio_out.deinit()
    print("Test complete")