from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from utime import localtime

# OLED DATA Pin on GPIO 0
OLED_SSD1306_SDA_PIN = 0
# OLED Clock Pin on GPIO 1
OLED_SSD1306_SCL_PIN = 1

sda=Pin(OLED_SSD1306_SDA_PIN, Pin.OUT)
scl=Pin(OLED_SSD1306_SCL_PIN, Pin.OUT)

# freq=198000 to 3600000 seem to work.  Use 3000000 as a safe option.
i2c = I2C(0, scl=scl, sda=sda, freq=3000000)

# Initialize display (128x64 pixels)
oled = SSD1306_I2C(128, 64, i2c)

# Clear display
oled.fill(0)

year = localtime()[0]
month = localtime()[1]
day = localtime()[2]
hour = localtime()[3]
minute = localtime()[4]

# display the date on the first line
oled.text(str(month) + "/" + str(day) + "/" + str(year), 0, 0, 1)

# display the time in hour and minute on the second line
oled.text(str(hour) + ":" + str(minute), 20, 20, 1)


oled.show()