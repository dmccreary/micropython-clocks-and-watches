from machine import Pin, I2C
from sh1106 import SH1106_I2C

# OLED DATA Pin on GPIO 0
OLED_SH11306_SDA_PIN = 0
# OLED Clock Pin on GPIO 1
OLED_SH11306_SCL_PIN = 1

sda=Pin(OLED_SH11306_SDA_PIN, Pin.OUT)
scl=Pin(OLED_SH11306_SCL_PIN, Pin.OUT)

# freq=30000 (30K) to 4000000 (4M) seem to work.  Use 3000000 (3M) as a safe option.
i2c = I2C(0, scl=scl, sda=sda, freq=3000000)

# Initialize display (128x64 pixels)
oled = SH1106_I2C(128, 64, i2c)
oled.rotate(180)

# Clear display
oled.fill(0)

# Write text
oled.text("MicroPython", 0, 0)
oled.text("Rocks!", 20, 20)

# Show the display
oled.show()