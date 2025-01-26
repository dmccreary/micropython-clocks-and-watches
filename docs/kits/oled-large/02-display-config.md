# Display Configuration File Data

![](./display-config.jpg)

```python
from machine import Pin
import ssd1306
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

# place a hello message at point (0,0) in white
oled.text("Config:", 0, 0, 1)

# row 2
oled.text("SCL:" + str(config.SPI_SCL_PIN), 0, 10, 1)
oled.text("SDA:" + str(config.SPI_SDA_PIN), 50, 10, 1)

# row 3
oled.text("DC:" + str(config.SPI_DC_PIN),     0, 20, 1)
oled.text("RES:" + str(config.SPI_RESET_PIN), 50, 20, 1)

# row 4
oled.text("CS:" + str(config.SPI_CS_PIN), 0, 30, 1)
oled.text("SPI BUS:" + str(config.SPI_BUS), 50, 30, 1)

# row 5
oled.text("Width:" + str(config.DISPLAY_WIDTH), 0, 40, 1)
oled.text("Height:" + str(config.DISPLAY_HEIGHT), 0, 50, 1)

oled.show()
```

