"""ILI9341 demo (shapes)."""
from ili9341 import Display, color565
from machine import Pin, SPI
from utime import sleep
import config
import colors

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

# this makes our code a little more readable
white = colors.WHITE
red = colors.RED
orange = colors.ORANGE
yellow = colors.YELLOW
green = colors.GREEN
blue = colors.BLUE
cyan = colors.CYAN
purple = colors.PURPLE

while True:

    display.clear()
    print('drawing lines and rects')
    
    print('drawing a horizontal line from (50,50) that is 200 wide')
    display.draw_hline(50, 50, 200, green)
    sleep(.5)

    print('drawing a vertical line from (100,100) that is 150 down')
    display.draw_vline(50, 50, 150, red)
    sleep(.5)

    print('drawing a yellow diagnle line from (150,150) to (200,200)')
    display.draw_line(50, 50, 200, 200, yellow)
    sleep(.5)
    
    print('drawing a filled orange hrect at (50,50) that is 25 wide and 75 hight')
    display.fill_rectangle(100, 100, 50, 50, orange)
    sleep(.5)
    
    # this one is not working
    print('drawing a purple rect at (200,200) that is 25 wide and 50 height')
    display.draw_rectangle(150, 150, 50, 50, white)
    sleep(3)

    display.clear()

    print('circles and ellipse')
    display.fill_circle(75, 75, 50, red)
    sleep(.5)

    display.draw_circle(150, 150, 50, orange)
    sleep(.5)

    display.fill_ellipse(150, 200, 100, 16, yellow)
    sleep(.5)

    display.draw_ellipse(250, 100, 20, 100, blue)
    sleep(5)
 
    print('drawing polygons')
    print('drawing lines to points')
    coords = [[50, 63], [78, 80], [122, 92], [50, 50], [78, 15], [0, 63]]
    display.draw_lines(coords, purple)
    sleep(1)

    # display.clear()
    print('drawing filled polygon')
    display.fill_polygon(7, 120, 120, 50, green)
    sleep(1)

    # display.clear()

    print('blue polygon outline')
    # num_sides
    display.draw_polygon(7, 180, 100, 30, blue, rotate=15)
    sleep(3)

   # display.cleanup()