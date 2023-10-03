import machine
import ssd1306

SCL=machine.Pin(2) # SPI CLock
SDA=machine.Pin(3) # SPI Data

RES = machine.Pin(4) # Reset
DC = machine.Pin(5) # Data/command
CS = machine.Pin(6) # Chip Select

spi=machine.SPI(0, sck=SCL, mosi=SDA, baudrate=100000)
oled = ssd1306.SSD1306_SPI(128, 64, spi, DC, RES, CS)

# place a hello message at point (0,0) in white
oled.text("Hello world!", 0, 0, 1)
oled.show()