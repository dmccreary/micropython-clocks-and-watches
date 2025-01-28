# Hello World



```python
# ST7735 LCD Test
import machine
import ST7735

# SCL=2 and SDK=3 implied for bus 0
spi = machine.SPI(0, baudrate=8000000)
d = ST7735.ST7735(spi, rst=4, ce=6, dc=5)
d.reset()
d.begin()
d.set_rotation(1)
d._bground = 0xffff
# white
d.fill_screen(d._bground)
# make background all white
d._color = 0x0000 # black ink
d.p_string(10,10,'Hello World!')
```

## Config File

```py
# Hardware configuration file for ST7735 clock

SPI_BUS = 0
SPI_SCL_PIN = 2 # Clock
SPI_SDA_PIN = 3 # labeled SDI(MOSI) on the back of the display
SPI_RESET_PIN = 4 # Reset
SPI_DC_PIN = 5 # Data/command
SPI_CS_PIN = 6 # Chip Select

# Screen Dimensions
DISPLAY_WIDTH=160
DISPLAY_HEIGHT=128
DISPLAY_ROTATION = 1

# Use builtin pull ups
MODE_PIN = 14 # one up from lower-left corner
INCREMENT_PIN = 15 # lower left corner with USB on top
DECREMENT_PIN = 16 # lower left corner with USB on top
```