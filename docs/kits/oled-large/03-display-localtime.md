# Display Localtime

```py
import machine
import ssd1306
import config
from time import localtime

SCL=machine.Pin(config.SCL_PIN) # SPI CLock
SDA=machine.Pin(config.SDA_PIN) # SPI Data

RES = machine.Pin(config.RESET_PIN) # Reset
DC = machine.Pin(config.DC_PIN) # Data/command
CS = machine.Pin(config.CS_PIN) # Chip Select

spi=machine.SPI(config.SPI_BUS, sck=SCL, mosi=SDA, baudrate=100000)
oled = ssd1306.SSD1306_SPI(config.WIDTH, config.HEIGHT, spi, DC, RES, CS)

year = localtime()[0]
month = localtime()[1]
day = localtime()[2]
hour = localtime()[3]
minute = localtime()[4]

# display the time in hour and minute on the first line
oled.text(str(hour) + ":" + str(minute), 0, 0, 1)

# display the date on the second line
oled.text(str(month) + "/" + str(day) + "/" + str(year), 0, 10, 1)
oled.show()
```

!!! Challenges
    1. Change the display format of the date and time.  Place the date
    and time in the center of the display.
    2. Add code to add a "AM" or "PM" string if the hour is greater than 12 noon
    3. Adding additional text to display if it is morning or evening
