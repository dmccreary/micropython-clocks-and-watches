# Display Local Time with Updates

Now let's update the display every second.

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

while True:
    # clear the entire screen
    
    oled.fill(0)
    year = localtime()[0]
    month = localtime()[1]
    day = localtime()[2]
    hour = localtime()[3]
    minute = localtime()[4]
    second = localtime()[5]

    # display the time in hour and minute on the first line
    oled.text(str(hour) + ":" + str(minute) + ":" + str(second) , 0, 0, 1)

    # display the date on the second line
    oled.text(str(month) + "/" + str(day) + "/" + str(year), 0, 10, 1)
    # send the entire screen to the display via SPI
    oled.show()
```