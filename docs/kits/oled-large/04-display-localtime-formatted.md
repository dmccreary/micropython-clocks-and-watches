# Display Local Time Formatted

![](./display-localtime-formatted.jpg)

That last program did display the correct local time, but it was hard to read.

In this version we will extract data time values,  and then display
a formatted version of both the date and the time.

```py
from machine import Pin, SPI
import ssd1306
from time import localtime
import config

SCL=Pin(config.SPI_SCL_PIN)
SDA=Pin(config.SPI_SDA_PIN)
DC = Pin(config.SPI_DC_PIN)
RES = Pin(config.SPI_RESET_PIN)
CS = Pin(config.SPI_CS_PIN)
SPI_BUS = config.SPI_BUS
WIDTH = config.DISPLAY_WIDTH
HEIGHT = config.DISPLAY_HEIGHT

spi=machine.SPI(SPI_BUS, sck=SCL, mosi=SDA, baudrate=1000000)
oled = ssd1306.SSD1306_SPI(WIDTH, HEIGHT, spi, DC, RES, CS)

while True:
    year = localtime()[0]
    month = localtime()[1]
    day = localtime()[2]
    hour = localtime()[3]
    minute = localtime()[4]
    second = localtime()[5]

    # display in 12 hour time paying special attention with hour == 0 and hour == 12
    if hour == 0:
        # Midnight edge case
        hour = 12
        am_pm = 'AM'
    elif hour == 12:
        # Noon edge case
        am_pm = 'PM'
    elif hour > 12:
        # Afternoon hours
        hour -= 12
        am_pm = 'PM'
    else:
        # Morning hours
        am_pm = 'AM'
    
    oled.fill(0)
    # display the date on the first line
    oled.text(str(month) + "/" + str(day) + "/" + str(year), 0, 0, 1)
    
    # display the time in hours, minute and seconds on the second line
    # note that the ":02" indicates printing in two columns with leading zeros
    oled.text(f"{hour}:{minute:02}:{second:02} " + am_pm, 0, 10, 1)

    oled.show()
```

## Time formatting

When we print out minutes and seconds we want to make sure that we print them in two digits with a leading zero.

```python
f"{minute:02}:{second:02}"
```


The python modulo operator `%` is used to find the remainder of the hour after dividing by 12.  This converts the 24-hour time to 12-hour time.