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

# mosi=Pin(23)
# miso=Pin(MISO_PIN)
spi = SPI(0, baudrate=40000000, sck=Pin(SCK_PIN), mosi=Pin(MISO_PIN))
display = Display(spi, dc=Pin(DC_PIN), cs=Pin(CS_PIN), rst=Pin(RESET_PIN), width=WIDTH, height=HEIGHT, rotation=ROTATION)

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

while True:

    display.draw_text(0, 0, 'Arcade Pix 9x11', arcadepix, color565(255, 0, 0))
    display.draw_text(0, 22, 'Bally 7x9', bally, color565(0, 255, 0))
    display.draw_text(0, 43, 'Broadway 17x15', broadway, color565(0, 0, 255))
    display.draw_text(0, 66, 'Espresso Dolce 18x24', espresso_dolce,
                      color565(0, 255, 255))
    display.draw_text(0, 104, 'Fixed Font 5x8', fixed_font,
                      color565(255, 0, 255))
    display.draw_text(0, 125, 'Neato 5x7', neato, color565(255, 255, 0))
    display.draw_text(0, 155, 'ROBOTRON 13X21', robotron,
                      color565(255, 255, 255))
    display.draw_text(0, 190, 'Unispace 12x24', unispace,
                      color565(255, 128, 0))
    display.draw_text(0, 220, 'Wendy 7x8', wendy, color565(255, 0, 128))

    sleep(9)
    display.clear()

    display.draw_text(100, 100, 'Arcade Pix 9x11', arcadepix,
                      color565(255, 0, 0),
                      landscape=True)
    """
    #display.draw_text(22, 255, 'Bally 7x9', bally, color565(0, 255, 0),
                      landscape=True)
    #display.draw_text(43, 255, 'Broadway 17x15', broadway, color565(0, 0, 255),
                      landscape=True)
    #display.draw_text(66, 255, 'Espresso Dolce 18x24', espresso_dolce,
                      color565(0, 255, 255), landscape=True)
    #display.draw_text(104, 255, 'Fixed Font 5x8', fixed_font,
                      color565(255, 0, 255), landscape=True)
    #display.draw_text(125, 255, 'Neato 5x7', neato, color565(255, 255, 0),
                      landscape=True)
    #display.draw_text(155, 255, 'ROBOTRON 13X21', robotron,
                      color565(255, 255, 255),
                      landscape=True)
    display.draw_text(190, 255, 'Unispace 12x24', unispace,
                      color565(255, 128, 0),
                      landscape=True)
    display.draw_text(220, 255, 'Wendy 7x8', wendy, color565(255, 0, 128),
                      landscape=True)
    """
    sleep(9)
    display.clear()

    display.draw_text(0, 0, 'Arcade Pix 9x11', arcadepix, color565(255, 0, 0),
                      background=color565(0, 255, 255))
    display.draw_text(0, 22, 'Bally 7x9', bally, color565(0, 255, 0),
                      background=color565(0, 0, 128))
    display.draw_text(0, 43, 'Broadway', broadway, color565(0, 0, 255),
                      background=color565(255, 255, 0))
    display.draw_text(0, 66, 'Espresso', espresso_dolce,
                      color565(0, 255, 255), background=color565(255, 0, 0))
    display.draw_text(0, 104, 'Fixed Font 5x8', fixed_font,
                      color565(255, 0, 255), background=color565(0, 128, 0))
    display.draw_text(0, 125, 'Neato 5x7', neato, color565(255, 255, 0),
                      background=color565(0, 0, 255))
    display.draw_text(0, 155, 'ROBOTRON 13X21', robotron,
                      color565(255, 255, 255),
                      background=color565(128, 128, 128))
    display.draw_text(0, 190, 'Unispace', unispace, color565(255, 128, 0),
                      background=color565(0, 128, 255))
    display.draw_text(0, 220, 'Wendy 7x8', wendy, color565(255, 0, 128),
                      background=color565(255, 255, 255))

    sleep(9)
