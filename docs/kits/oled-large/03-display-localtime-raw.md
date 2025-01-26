# Display the Raw Localtime

![](./display-raw-localtime.jpg)

```py
from machine import Pin, SPI
import ssd1306
from time import localtime, sleep
import config

# get the configuration data
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
    # display the raw data from localtime
    oled.fill(0)
    oled.text(str(localtime()[0]), 0, 0, 1)
    oled.text(str(localtime()[1]), 0, 10, 1)
    oled.text(str(localtime()[2]), 0, 20, 1)
    oled.text(str(localtime()[3]), 0, 30, 1)
    oled.text(str(localtime()[4]), 0, 40, 1)
    oled.text(str(localtime()[5]), 0, 50, 1)
    oled.show()
    sleep(1)
```

!!! Challenges
    1. What numbers are fixed and what numbers arc chainging?
    2. What do you think each of the numbers mean?
    3. Why is it hard to read the time using this "raw" unformatted way?