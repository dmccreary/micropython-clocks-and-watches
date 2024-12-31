# Adjusting the Clock Digit Layout

You have the ability to adjust the clock digit layouts
by changing the following parameters:

1. **left_margin** - were the left-most digit drawing starts
2. **y_offset** - how far down the screen to begin to draw the top line of the digits
3. **digit_width** - how wide each digit is
4. **digit_height** - how high each digit is
5. **digit_spacing** - the spacing between the left edges of each digit - not the space between the digits
6. **digit_thickness** - how wide each bar of each segment is

In addition you can change the placement of the colon and the AM/PM indicator.

```python
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from utime import localtime, sleep

# OLED DATA Pin on GPIO 0
OLED_SSD1306_SDA_PIN = 0
# OLED Clock Pin on GPIO 1
OLED_SSD1306_SCL_PIN = 1

sda=Pin(OLED_SSD1306_SDA_PIN, Pin.OUT)
scl=Pin(OLED_SSD1306_SCL_PIN, Pin.OUT)

# freq=198000 to 3600000 seem to work.  Use 3000000 as a safe option.
i2c = I2C(0, scl=scl, sda=sda, freq=3000000)

# Initialize display (128x64 pixels)
oled = SSD1306_I2C(128, 64, i2c)

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


# x and y are upper-left-corner
# width and height are the dimensions of the digit
# thinkness is the width of the line segments
# color is 1 for white and 0 for black
def drawDigit(digit, x, y, width, height, thinkness, color):
  # get a list of the segments that are on for this digit
  segmentOn = segmentMapping[digit];
  
  # Draw the horizontal segments: top, bottem, middle
  for i in [0, 3, 6]:
    if (segmentOn[i]):
      if (i==0): # top
          yOffset = 0 
      if (i==3):
          yOffset = height - thinkness # bottem element
      if (i==6):
          yOffset = height // 2 - thinkness // 2# bottum
      # oled.line(x - size, y+yOffset-size, x + size, y+yOffset-size, 1);
      oled.fill_rect(x, y+yOffset, width, thinkness, color)

  # Draw the vertical segments ur, lr, ll, ul
  for i in [1, 2, 4, 5]:
    if (segmentOn[i]) :
      # upper vertical lines
      if (i==1 or i==5):
          startY = y
          endY = y + height // 2
      # lower two vertical lines (2=lower right and 4=lower left)
      if (i==2 or i==4):
          startY = y + height // 2
          endY = y + height
      if (i==4 or i==5): xOffset = 0
      if (i==1 or i==2): xOffset = width-thinkness

      oled.fill_rect(x+xOffset, startY, thinkness, endY-startY, color)

def update_screen(digit_val):
    global counter
    
    ## Adjust these to fit the display
    left_margin = -15
    y_offset = 16
    digit_width = 30
    digit_height = 37
    digit_spacing = 36
    digit_thickness = 6
    oled.fill(0)
    oled.text('Clock Digits Lab', 0, 0, 1)
    
    # left digit will be 1 or blank
    drawDigit(1, left_margin,  y_offset, digit_width, digit_height, digit_thinkness, 1)
    drawDigit(digit_val, left_margin + 1*digit_spacing,  y_offset, digit_width, digit_height, digit_thickness, 1)
    drawDigit(digit_val, left_margin + 2*digit_spacing,  y_offset, digit_width, digit_height, digit_thickness, 1)
    drawDigit(digit_val, left_margin + 3*digit_spacing, y_offset, digit_width, digit_height, digit_thickness, 1)
    
    draw_colon(53,26)
    
    pm_xoffset = 103
    pm_yoffset = 55
    if (counter % 2):
        # 112 is the max right for the am/pm text
        oled.text("am", pm_xoffset, pm_yoffset, 1)
        
    else:
        oled.text("pm", pm_xoffset, pm_yoffset, 1)
    oled.text(str(digit_val), 0, 54, 1)
    
    oled.show()

def draw_colon(x,y):
    oled.fill_rect(x, y, 2, 2,1)
    oled.fill_rect(x, y+8, 2, 2,1)

counter = 0
while True:
    update_screen(counter)
    sleep(1)
    counter += 1
    if counter > 9:
        counter = 0
```