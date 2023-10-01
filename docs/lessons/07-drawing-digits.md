# Drawing Clock Digits

## The Seven Segments of a Numeric Digit

Since the early history of computing, numeric displays used a grouping
of seven individaul lights to display a single digit.  This is shown in
the image below:

![Seven Segment Display](../../img/seven-segment-display.png)

The segments are labeled "a" through "g" starting at the top and
going around in a clockwise direction.  The center element is
the "g" element.

Technically, many displays have an 8th segment for the decimal point (DP).  To keep
things simple we will just focus on the seven segments in this lesson.

Clocks also usually have a colon that separates the hours and minutes
and an AM/PM indicator for 12-hour displays.  We will be treating
these and independant drawing components in this lab.  Many digital
clocks have the colon flash on and off every second.

## The Segment Map

For any digit, is the segment on or off?

We can create an array of the segments like this:

```py
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
```

## Drawing Horizontal Lines

```py
# Horizontal segments
  for i in [0, 3, 6]:
    if (segmentOn[i]):
      if (i==0): yOffset = 0 # top
      if (i==3): yOffset = size*2 # bottom element
      if (i==6): yOffset = size # middle
      # oled.line(x - size, y+yOffset-size, x + size, y+yOffset-size, 1);
      drawThickHorizLine(x - size, x + size, y+yOffset-size, width)
```
## Drawing the Vertical Segments

```py
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
      drawThickVertLine(startY, endY, xpos, width)```

```py
# clock digits
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

def drawThickHorizLine(x1, x2, y, width):
    oled.line(x1, y, x2, y, 1);
    if width > 1:
        oled.line(x1, y+1, x2, y+1, 1);
    if width > 2:
        oled.line(x1, y-1, x2, y-1, 1);
    if width > 3:
        oled.line(x1, y+2, x2, y+2, 1);
    if width > 4:
        oled.line(x1, y-2, x2, y-2, 1);

def drawThickVertLine(y1, y2, x, width):
    oled.line(x, y1, x, y2, 1);
    if width > 1:
        oled.line(x+1, y1, x+1, y2, 1);
    if width > 2:
        oled.line(x-1, y1, x-1, y2, 1);
    if width > 3:
        oled.line(x+2, y1, x+2, y2, 1);
    if width > 4:
        oled.line(x-2, y1, x-2, y2, 1);
        
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
    oled.text('Clock Digit Lab', 0, 0, 1)
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

counter = 0
while True:
    update_screen(counter)
    sleep(1)
    counter += 1
    if counter > 9:
        counter = 0

```