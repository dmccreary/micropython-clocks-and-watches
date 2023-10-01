# clock digits
from ili9341 import Display, color565
from machine import Pin, SPI
from utime import sleep, localtime
import config
import colors

# Shorthands for the configuration information
SCK_PIN = config.SCK_PIN
MISO_PIN = config.MISO_PIN # labeled SDI(MOSI) on the back of the display
DC_PIN = config.DC_PIN
RESET_PIN = config.RESET_PIN
CS_PIN = config.CS_PIN

WIDTH=config.WIDTH
HEIGHT=config.HEIGHT
ROTATION=config.ROTATION

# for portability and smaller code
BLUE = colors.BLUE
BLACK = colors.BLACK
WHITE = colors.WHITE

# mosi=Pin(23)
# miso=Pin(MISO_PIN)
spi = SPI(0, baudrate=40000000, sck=Pin(SCK_PIN), mosi=Pin(MISO_PIN))
display = Display(spi, dc=Pin(DC_PIN), cs=Pin(CS_PIN), rst=Pin(RESET_PIN), width=WIDTH, height=HEIGHT, rotation=ROTATION)

# display.fill_rectangle(0,0, 50,HEIGHT, colors.RED)
# display.fill_rectangle(50,0, 50,HEIGHT, colors.ORANGE)
# display.fill_rectangle(100,0, 50,HEIGHT, colors.YELLOW)
# display.fill_rectangle(150,0, 50,HEIGHT, colors.GREEN)
# display.fill_rectangle(200,0, 50,HEIGHT, colors.BLUE)
# display.fill_rectangle(250,0, 50,HEIGHT, colors.PURPLE)
# display.fill_rectangle(300,0, 20,HEIGHT, WHITE)


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

# for portability with other MicroPython drawing libraries that use framebuf
def line(x1,y1,x2,y2,color):
    display.draw_line(x1,y1,x2,y2,color)

def fill(color):
    display.fill_rectangle(0, 0, WIDTH, HEIGHT, color)

def fill_rect(x,y,w,h,color):
    display.fill_rectangle(x, y, w, h, color)

def drawThickHorizLine(x1, x2, y, width, color):
    fill_rect(x1, y, x2-x1, width, color)

def drawThickVertLine(y1, y2, x, width, color):
    fill_rect(x, y1, width, y2-y1, color)
        
# x and y are the center of the digit, size is the center to edge
def drawDigit(digit, x, y, size, width, color):
  segmentOn = segmentMapping[digit];
  
  # Horizontal segments
  for i in [0, 3, 6]:
    if (segmentOn[i]):
      if (i==0): yOffset = 0 # top
      if (i==3): yOffset = size*2 # bottom element
      if (i==6): yOffset = size # middle
      # oled.line(x - size, y+yOffset-size, x + size, y+yOffset-size, 1);
      # added the width of the line to the 2nd x point
      drawThickHorizLine(x - size, x + size + width, y+yOffset-size, width, color)

  # Vertical segments
  for i in [1, 2, 4, 5]:
    if (segmentOn[i]) :
      if (i==1 or i==5):
          startY = y-size
          # added the width do draw down to
          endY = y
      if (i==2 or i==4):
          startY = y
          endY = y + size
      if (i==4 or i==5): xOffset = -size
      if (i==1 or i==2): xOffset = +size
      xpos = x + xOffset
      # oled.line(xpos, startY, xpos, endY, 1)
      drawThickVertLine(startY, endY+width, xpos, width, color)

def update_screen(digit_val, color):
    # display.fill(BLACK)
    # display.text('Clock Digit Lab', 0, 0, 1)
    dr = 28 # digit radius
    dch = 120 # digit center hight
    lm = 5 # left margin for all 4-digits
    dw = 84 # digit width (2*dr + spacing between digits
    cm = 8 # colon left margin
    width = 8
    seconds = localtime()[5]
    
    # draw the hour digits
    hour = localtime()[3]
    if hour > 12:
        hour = hour - 12
        am_pm = 'pm'
    else:
        am_pm = 'am'
    if hour < 10:
        # just draw the second digit
        drawDigit(hour, lm+dw, dch, dr, width, color)
    else:
        # we have 10, 11 or 12 so the first digit is 1
        drawDigit(1, lm, dch, dr, width, color)
        # subtract 10 from the second digit
        drawDigit(hour-10, lm+dw, dch, dr, width, color)
       
    # draw the colon white every odd second alternating color
    if seconds % 2:
        draw_colon(lm+dw*2+cm-43, dch-15, 10, WHITE)
    else:
        draw_colon(lm+dw*2+cm-43, dch-15, 10, BLACK)
    
    # draw the minute digits
    minutes = localtime()[4]
    # value, x, y, size
    # left minute digit after the colon
    drawDigit(minutes // 10, lm+dw*2+cm, dch, dr, width, color)
    # right minute digit
    drawDigit(minutes % 10, lm+dw*3+cm+2, dch, dr, width, color)
    
    # draw the AM/PM
    #display.text(am_pm, lm+dw*4+cm-8, dch+3, 1)
    
    #oled.text(timeStrFmt(), 0, 46, 1)
    # display.text(str(localtime()[5]), 0, 54)
    ##oled.text(str(digit_val), 0, 54, 1)


def draw_colon(x,y, size, color):
    fill_rect(x, y, size, size, color)
    # drop down 3x the size
    fill_rect(x, y+size*3, size, size, color)

def timeStrFmt():
    hour = localtime()[3]
    if hour > 12:
        hour = hour - 12
        am_pm = ' pm'
    else: am_pm = ' am'
    # format minutes and seconds with leading zeros
    minutes = "{:02d}".format(localtime()[4])
    return str(hour) + ':' + minutes + am_pm

fill(BLUE)
minutes = localtime()[4]
while True: 
    update_screen(minutes, WHITE)
    sleep(1)
    minutes += 1
    if minutes > 59:
        fill(BLUE)
        minutes = 0


# clock digits
from ili9341 import Display, color565
from machine import Pin, SPI
from utime import sleep, localtime
import config
import colors

# Shorthands for the configuration information
SCK_PIN = config.SCK_PIN
MISO_PIN = config.MISO_PIN # labeled SDI(MOSI) on the back of the display
DC_PIN = config.DC_PIN
RESET_PIN = config.RESET_PIN
CS_PIN = config.CS_PIN

WIDTH=config.WIDTH
HEIGHT=config.HEIGHT
ROTATION=config.ROTATION

# for portability and smaller code
BLUE = colors.BLUE
BLACK = colors.BLACK
WHITE = colors.WHITE

# mosi=Pin(23)
# miso=Pin(MISO_PIN)
spi = SPI(0, baudrate=40000000, sck=Pin(SCK_PIN), mosi=Pin(MISO_PIN))
display = Display(spi, dc=Pin(DC_PIN), cs=Pin(CS_PIN), rst=Pin(RESET_PIN), width=WIDTH, height=HEIGHT, rotation=ROTATION)

# display.fill_rectangle(0,0, 50,HEIGHT, colors.RED)
# display.fill_rectangle(50,0, 50,HEIGHT, colors.ORANGE)
# display.fill_rectangle(100,0, 50,HEIGHT, colors.YELLOW)
# display.fill_rectangle(150,0, 50,HEIGHT, colors.GREEN)
# display.fill_rectangle(200,0, 50,HEIGHT, colors.BLUE)
# display.fill_rectangle(250,0, 50,HEIGHT, colors.PURPLE)
# display.fill_rectangle(300,0, 20,HEIGHT, WHITE)


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

# for portability with other MicroPython drawing libraries that use framebuf
def line(x1,y1,x2,y2,color):
    display.draw_line(x1,y1,x2,y2,color)

def fill(color):
    display.fill_rectangle(0, 0, WIDTH, HEIGHT, color)

def fill_rect(x,y,w,h,color):
    display.fill_rectangle(x, y, w, h, color)

def drawThickHorizLine(x1, x2, y, width, color):
    fill_rect(x1, y, x2-x1, width, color)

def drawThickVertLine(y1, y2, x, width, color):
    fill_rect(x, y1, width, y2-y1, color)
        
# x and y are the center of the digit, size is the center to edge
def drawDigit(digit, x, y, size, width, color):
  segmentOn = segmentMapping[digit];
  
  # Horizontal segments
  for i in [0, 3, 6]:
    if (segmentOn[i]):
      if (i==0): yOffset = 0 # top
      if (i==3): yOffset = size*2 # bottom element
      if (i==6): yOffset = size # middle
      # oled.line(x - size, y+yOffset-size, x + size, y+yOffset-size, 1);
      # added the width of the line to the 2nd x point
      drawThickHorizLine(x - size, x + size + width, y+yOffset-size, width, color)

  # Vertical segments
  for i in [1, 2, 4, 5]:
    if (segmentOn[i]) :
      if (i==1 or i==5):
          startY = y-size
          # added the width do draw down to
          endY = y
      if (i==2 or i==4):
          startY = y
          endY = y + size
      if (i==4 or i==5): xOffset = -size
      if (i==1 or i==2): xOffset = +size
      xpos = x + xOffset
      # oled.line(xpos, startY, xpos, endY, 1)
      drawThickVertLine(startY, endY+width, xpos, width, color)

def update_screen(digit_val, color):
    # display.fill(BLACK)
    # display.text('Clock Digit Lab', 0, 0, 1)
    dr = 28 # digit radius
    dch = 120 # digit center hight
    lm = 5 # left margin for all 4-digits
    dw = 84 # digit width (2*dr + spacing between digits
    cm = 8 # colon left margin
    width = 8
    seconds = localtime()[5]
    
    # draw the hour digits
    hour = localtime()[3]
    if hour > 12:
        hour = hour - 12
        am_pm = 'pm'
    else:
        am_pm = 'am'
    if hour < 10:
        # just draw the second digit
        drawDigit(hour, lm+dw, dch, dr, width, color)
    else:
        # we have 10, 11 or 12 so the first digit is 1
        drawDigit(1, lm, dch, dr, width, color)
        # subtract 10 from the second digit
        drawDigit(hour-10, lm+dw, dch, dr, width, color)
       
    # draw the colon white every odd second alternating color
    if seconds % 2:
        draw_colon(lm+dw*2+cm-43, dch-15, 10, WHITE)
    else:
        draw_colon(lm+dw*2+cm-43, dch-15, 10, BLACK)
    
    # draw the minute digits
    minutes = localtime()[4]
    # value, x, y, size
    # left minute digit after the colon
    drawDigit(minutes // 10, lm+dw*2+cm, dch, dr, width, color)
    # right minute digit
    drawDigit(minutes % 10, lm+dw*3+cm+2, dch, dr, width, color)
    
    # draw the AM/PM
    #display.text(am_pm, lm+dw*4+cm-8, dch+3, 1)
    
    #oled.text(timeStrFmt(), 0, 46, 1)
    # display.text(str(localtime()[5]), 0, 54)
    ##oled.text(str(digit_val), 0, 54, 1)


def draw_colon(x,y, size, color):
    fill_rect(x, y, size, size, color)
    # drop down 3x the size
    fill_rect(x, y+size*3, size, size, color)

def timeStrFmt():
    hour = localtime()[3]
    if hour > 12:
        hour = hour - 12
        am_pm = ' pm'
    else: am_pm = ' am'
    # format minutes and seconds with leading zeros
    minutes = "{:02d}".format(localtime()[4])
    return str(hour) + ':' + minutes + am_pm

fill(BLUE)
minutes = localtime()[4]
while True: 
    update_screen(minutes, WHITE)
    sleep(1)
    minutes += 1
    if minutes > 59:
        fill(BLUE)
        minutes = 0


