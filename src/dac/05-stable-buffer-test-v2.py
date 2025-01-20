from machine import Pin, I2S
import struct
import gc
from time import sleep_ms

class AudioTest:
    def __init__(self):
        # Pin Definitions
        self.BCK_PIN = 16
        self.WS_PIN = 17
        self.SD_PIN = 18
        self.audio_out = None
        self.buffer = None
        
    def create_buffer(self):
        # Very small buffer to minimize memory usage
        BUFFER_SIZE = 128
        self.buffer = bytearray(BUFFER_SIZE * 2)
        for i in range(0, len(self.buffer), 2):
            value = 32767 if (i // 2) % 2 == 0 else -32767
            struct.pack_into("<h", self.buffer, i, value)
    
    def init_i2s(self):
        # Configure I2S with minimal buffer
        self.audio_out = I2S(
            0,
            sck=Pin(self.BCK_PIN),
            ws=Pin(self.WS_PIN),
            sd=Pin(self.SD_PIN),
            mode=I2S.TX,
            bits=16,
            format=I2S.MONO,
            rate=8000,
            ibuf=256  # Minimal internal buffer
        )
    
    def cleanup(self):
        if self.audio_out:
            self.audio_out.deinit()
            self.audio_out = None
        self.buffer = None
        gc.collect()
    
    def run(self):
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

Starting audio test...
Press Ctrl+C to stop
""")
        try:
            # Initialize everything
            gc.collect()
            self.create_buffer()
            self.init_i2s()
            
            write_count = 0
            while True:
                if self.audio_out and self.buffer:
                    self.audio_out.write(self.buffer)
                    sleep_ms(10)  # Longer delay between writes
                    
                    write_count += 1
                    if write_count % 50 == 0:
                        print(".", end="")
                        gc.collect()  # Regular garbage collection
                        
        except KeyboardInterrupt:
            print("\nStopping...")
        finally:
            self.cleanup()
            print("Test complete")

# Create and run test
test = AudioTest()
test.run()