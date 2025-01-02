from machine import Pin
import ssd1306
import config

SCL=Pin(config.SCL_PIN) # SPI CLock
SDA=Pin(config.SDA_PIN) # SPI Data

RES = Pin(config.RESET_PIN) # Reset
DC = Pin(config.DC_PIN) # Data/command
CS = Pin(config.CS_PIN) # Chip Select
WIDTH = config.WIDTH
HEIGHT = config.HEIGHT

spi=machine.SPI(config.SPI_BUS, sck=SCL, mosi=SDA, baudrate=100000)
oled = ssd1306.SSD1306_SPI(WIDTH, HEIGHT, spi, DC, RES, CS)

# place a hello message at point (0,0) in white
oled.text("Hello world!", 0, 0, 1)
oled.show()