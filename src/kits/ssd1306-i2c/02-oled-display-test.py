from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

# OLED DATA Pin on GPIO 0
OLED_SSD1306_SDA_PIN = 0
# OLED Clock Pin on GPIO 1
OLED_SSD1306_SCL_PIN = 1

sda=Pin(OLED_SSD1306_SDA_PIN, Pin.OUT)
scl=Pin(OLED_SSD1306_SCL_PIN, Pin.OUT)

# freq=198000 to 3600000 seem to work.  Use 3000000 as a safe option.
i2c = I2C(0, scl=scl, sda=sda)

# Initialize display (128x64 pixels)
oled = SSD1306_I2C(128, 64, i2c)

# Clear display
oled.fill(0)

# Write text
oled.text("MicroPython", 0, 0)
oled.text("Rocks!", 20, 20)

# Show the display
oled.show()