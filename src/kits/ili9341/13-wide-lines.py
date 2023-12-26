# Clock Lab 13: Wide Lines
# this lab uses the fill_rect function to draw the segments
import machine
import utime
import ssd1306
from utime import sleep, localtime
led = machine.Pin(25, machine.Pin.OUT)

SCL=machine.Pin(2) # SPI CLock
SDA=machine.Pin(3) # SPI Data
spi=machine.SPI(0, sck=SCL, mosi=SDA, baudrate=100000)

RES = machine.Pin(4)
DC = machine.Pin(5)
CS = machine.Pin(6)

oled = ssd1306.SSD1306_SPI(128, 64, spi, DC, RES, CS)

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

# width is the thinkness of the horisontal line
def drawThickHorizLine(x1, x2, y, width):
    oled.fill_rect(x1, y, x2-x1+width, width, 1);

def drawThickVertLine(y1, y2, x, width):
    oled.fill_rect(x, y1, width, y2-y1, 1);
        
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
    oled.fill(0)
    oled.text('Lab 13: rect', 0, 0, 1)
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
    oled.text(am_pm, lm+dw*4+cm-8, dch+3, 1)
    
    #oled.text(timeStrFmt(), 0, 46, 1)
    oled.text(str(localtime()[5]), 0, 54)
    #oled.text(str(digit_val), 0, 54, 1)

    oled.show()

def draw_colon(x,y):
    oled.fill_rect(x, y, 2, 2,1)
    oled.fill_rect(x, y+8, 2, 2,1)

def timeStrFmt():
    hour = localtime()[3]
    if hour > 12:
        hour = hour - 12
        am_pm = ' pm'
    else: am_pm = ' am'
    # format minutes and seconds with leading zeros
    minutes = "{:02d}".format(localtime()[4])
    return str(hour) + ':' + minutes + am_pm

update_screen(0)


