import machine
import ssd1306
import config
from time import sleep, localtime
import math

SCL=machine.Pin(config.SCL_PIN) # SPI CLock
SDA=machine.Pin(config.SDA_PIN) # SPI Data

RES = machine.Pin(config.RESET_PIN) # Reset
DC = machine.Pin(config.DC_PIN) # Data/command
CS = machine.Pin(config.CS_PIN) # Chip Select

spi=machine.SPI(config.SPI_BUS, sck=SCL, mosi=SDA, baudrate=100000)
oled = ssd1306.SSD1306_SPI(config.WIDTH, config.HEIGHT, spi, DC, RES, CS)
TWO_PI = 3.14159 * 2

LENGTH = config.HEIGHT // 2
CENTER_X = config.WIDTH // 2
CENTER_Y = config.HEIGHT // 2

oled.fill(0)

# draw the digits
for i in range(0,4):
    radians = (i/4)*TWO_PI
    x = int(math.sin(radians)*LENGTH)
    y = -int(math.cos(radians)*LENGTH)
    # print(i, radians, x, y, x, y)
    
    # Adjustments for the placments of the digits
    if i == 0:
        digit_str = "12"
        x -= 7
        y += 4
    elif i == 1:
        x += 4
        y -= 2
    elif i == 2:
        y -= 9
        x -=  4
    elif i == 3:
        x -= 11
        y -= 2
    if i > 0:
        digit_str = str(i*3)
    
    oled.text(digit_str,CENTER_X + x, CENTER_Y + y, 1)
    
# draw center dot and outer circle
oled.ellipse(CENTER_X, CENTER_Y, 1, 1, 1)

oled.ellipse(CENTER_X, CENTER_Y, 32, 31, 1)
oled.show()
    
