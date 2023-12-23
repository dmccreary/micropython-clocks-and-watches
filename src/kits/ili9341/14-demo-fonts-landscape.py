"""ILI9341 demo (fonts)."""
from ili9341 import Display, color565
from machine import Pin, SPI
from time import sleep
import config
import colors
from xglcd_font import XglcdFont

# Use these PIN definitions.  SCK must be on 2 and data (SDL) on 3
SCK_PIN = config.SCK_PIN
MISO_PIN = config.MISO_PIN # labeled SDI(MOSI) on the back of the display
DC_PIN = config.DC_PIN
RESET_PIN = config.RESET_PIN
CS_PIN = config.CS_PIN

WIDTH=config.WIDTH
HEIGHT=config.HEIGHT
ROTATION=config.ROTATION

# this makes our code a little more readable
white = colors.WHITE
red = colors.RED
orange = colors.ORANGE
yellow = colors.YELLOW
green = colors.GREEN
blue = colors.BLUE
cyan = colors.CYAN
purple = colors.PURPLE

spi = SPI(0, baudrate=40000000, sck=Pin(SCK_PIN), mosi=Pin(MISO_PIN))
d = Display(spi, dc=Pin(DC_PIN), cs=Pin(CS_PIN), rst=Pin(RESET_PIN), width=WIDTH, height=HEIGHT, rotation=ROTATION)

print('Loading fonts...')
print('Loading arcadepix')
arcadepix = XglcdFont('fonts/ArcadePix9x11.c', 9, 11)

print('Loading bally')
bally = XglcdFont('fonts/Bally7x9.c', 7, 9)

print('Loading broadway')
broadway = XglcdFont('fonts/Broadway17x15.c', 17, 15)

print('Loading espresso_dolce')
espresso_dolce = XglcdFont('fonts/EspressoDolce18x24.c', 18, 24)

print('Loading fixed_font')
fixed_font = XglcdFont('fonts/FixedFont5x8.c', 5, 8)

print('Loading neato')
neato = XglcdFont('fonts/Neato5x7.c', 5, 7, letter_count=223)

print('Loading robotron')
robotron = XglcdFont('fonts/Robotron13x21.c', 13, 21)

print('Loading unispace')
unispace = XglcdFont('fonts/Unispace12x24.c', 12, 24)

print('Loading wendy')
wendy = XglcdFont('fonts/Wendy7x8.c', 7, 8)

print('Fonts loaded.')

counter = 0
while True:

    d.draw_text(15, 230, 'Arcade Pix 9x11', arcadepix, red, landscape=True)
    
    d.draw_text(30, 230, 'Bally 7x9', bally, green, landscape=True)
    
    d.draw_text(50, 230, 'Espresso Dolce 18x24', espresso_dolce, cyan, landscape=True)
    
    d.draw_text(80, 230, 'Fixed Font 5x8', fixed_font, yellow, landscape=True)
    d.draw_text(100, 230, 'Neato 5x7', neato, orange, landscape=True)
    d.draw_text(120, 230, 'ROBOTRON 13X21', robotron, white, landscape=True)
    d.draw_text(150, 230, 'Unispace 12x24', unispace, color565(255, 128, 0), landscape=True)
    d.draw_text(180, 230, 'Wendy 7x8', wendy, color565(255, 0, 128), landscape=True)

