# resizable clock digits
from machine import Pin, SPI
from utime import sleep, localtime
import random
import gc9a01
import vga1_bold_16x32 as font

# this uses the standard Dupont ribbon cable spanning rows 4-9 on our breadboard
SCK_PIN = 2 # row 4
SDA_PIN = 3
DC_PIN = 4
CS_PIN = 5
# GND is row 8
RST_PIN = 6

# define the SPI intrface
spi = SPI(0, baudrate=60000000, sck=Pin(SCK_PIN), mosi=Pin(SDA_PIN))
tft = gc9a01.GC9A01(spi, 240, 240, reset=Pin(RST_PIN, Pin.OUT),
    cs=Pin(CS_PIN, Pin.OUT), dc=Pin(DC_PIN, Pin.OUT), rotation=0)

segmentMapping = [
  #a, b, c, d, e, f, g
  [1, 1, 1, 1, 1, 1, 0], # 0
  [0, 1, 1, 0, 0, 0, 0], # 1
  [1, 1, 0, 1, 1, 0, 1], # 2
  [1, 1, 1, 1, 0, 0, 1], # 3
  [0, 1, 1, 0, 0, 1, 1], # 4
  [1, 0, 1, 1, 0, 1, 1], # 5
  [1, 0, 1, 1, 1, 1, 1], # 6
  [1, 1, 1, 0, 0, 0, 0], # 7
  [1, 1, 1, 1, 1, 1, 1], # 8
  [1, 1, 1, 1, 0, 1, 1]  # 9
];

WHITE = gc9a01.WHITE
BLACK = gc9a01.BLACK

def drawThickHorizLine(x1, x2, y, width):
    tft.line(x1, y, x2, y, 1);
    if width > 1:
        tft.line(x1, y+1, x2, y+1, gc9a01.WHITE);
    if width > 2:
        tft.line(x1, y-1, x2, y-1, gc9a01.WHITE);
    if width > 3:
        tft.line(x1, y+2, x2, y+2, gc9a01.WHITE);
    if width > 4:
        tft.line(x1, y-2, x2, y-2, gc9a01.WHITE);

def drawThickVertLine(y1, y2, x, width):
    tft.line(x, y1, x, y2, 1);
    if width > 1:
        tft.line(x+1, y1, x+1, y2, gc9a01.WHITE);
    if width > 2:
        tft.line(x-1, y1, x-1, y2, gc9a01.WHITE);
    if width > 3:
        tft.line(x+2, y1, x+2, y2, gc9a01.WHITE);
    if width > 4:
        tft.line(x-2, y1, x-2, y2, gc9a01.WHITE);
        
# x and y are the center of the digit, size is the center to edge
def drawDigit(digit, x, y, size, width):
  segmentOn = segmentMapping[digit];
  
  # Horizontal segments
  for i in [0, 3, 6]:
    if (segmentOn[i]):
      if (i==0): yOffset = 0 # top
      if (i==3): yOffset = size*2 # bottom element
      if (i==6): yOffset = size # middle
      # oled.line(x - size, y+yOffset-size, x + size, y+yOffset-size, 1);
      drawThickHorizLine(x - size, x + size, y+yOffset-size, width)

  # Vertical segments
  for i in [1, 2, 4, 5]:
    if (segmentOn[i]) :
      if (i==1 or i==5):
          startY = y-size
          endY = y
      if (i==2 or i==4):
          startY = y
          endY = y + size
      if (i==4 or i==5): xOffset = -size
      if (i==1 or i==2): xOffset = +size
      xpos = x + xOffset
      # oled.line(xpos, startY, xpos, endY, 1)
      drawThickVertLine(startY, endY, xpos, width)

def update_screen(digit_val):
    tft.fill(BLACK)
    tft.text(font, 'Clock Digit Lab', 20, 60, WHITE)
    dr = 10 # digit radius
    dch = 26 # digit center hight
    lm = 10 # left margin for all 4-digits
    dw = 24 # digit width (2*dr + spacing between digits
    cm = 8 # colon left margin
    width = 3
    
    # draw the hour digits
    hour = localtime()[3]
    if hour > 12:
        hour = hour - 12
        am_pm = 'pm'
    else:
        am_pm = 'am'
    if hour < 10:
        # just draw the second digit
        drawDigit(hour, lm+dw, dch, dr, width)
    else:
        # we have 10, 11 or 12 so the first digit is 1
        drawDigit(1, lm, dch, dr, width)
        # subtract 10 from the second digit
        drawDigit(hour-10, lm+dw, dch, dr, width)
       
    # draw the colon
    if localtime()[5] % 2:
        draw_colon(lm+dw*2+cm-16,dch-5)
    
    # draw the minutes
    minutes = localtime()[4]
    # value, x, y, size
    # left minute digit after the colon
    drawDigit(minutes // 10, lm+dw*2+cm, dch, dr, width)
    # right minute digit
    drawDigit(minutes % 10, lm+dw*3+cm+2, dch, dr, width)
    
    # draw the AM/PM
    tft.text(font, am_pm, lm+dw*4+cm-8, dch+3, WHITE)
    
    tft.text(font, str(localtime()[5]), 0, 54, WHITE)


def draw_colon(x,y):
    tft.fill_rect(x, y, 2, 2, WHITE)
    tft.fill_rect(x, y+8, 2, 2, WHITE)

def timeStrFmt():
    hour = localtime()[3]
    if hour > 12:
        hour = hour - 12
        am_pm = ' pm'
    else: am_pm = ' am'
    # format minutes and seconds with leading zeros
    minutes = "{:02d}".format(localtime()[4])
    return str(hour) + ':' + minutes + am_pm

counter = 0
tft.fill(BLACK)
while True:
    print(counter, timeStrFmt())
    tft.text(font, "Test", 50, 50, WHITE)
    sleep(1)
    update_screen(counter)
    sleep(1)
    counter += 1
    if counter > 9:
        counter = 0

