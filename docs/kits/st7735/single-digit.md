# Draw a Single Digit on the ST7735 LCD

![](./single-digit.jpg)

```python
# Draw a single digit on the ST7735 LCD
import machine
import ST7735
from utime import sleep

# Initialize SPI and display
spi = machine.SPI(0, baudrate=8000000)
d = ST7735.ST7735(spi, rst=4, ce=6, dc=5)
d.reset()
d.begin()
d.set_rotation(1)  # Rotate to landscape mode

# Define colors using RGB565 format
BLUE_BACKGROUND = d.rgb_to_565(0, 0, 255)  # Blue background
WHITE_DIGIT = d.rgb_to_565(255, 255, 255)  # White for digits

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
]

def drawDigit(digit, x, y, width, height, thickness, color):
    # Get segments that are on for this digit
    segmentOn = segmentMapping[digit]
    
    # Draw horizontal segments (top, bottom, middle)
    for i in [0, 3, 6]:
        if segmentOn[i]:
            if i == 0:  # top
                yOffset = 0
            elif i == 3:  # bottom
                yOffset = height - thickness
            else:  # middle
                yOffset = height // 2 - thickness // 2
                
            d.draw_block(x, y + yOffset, width, thickness, color)

    # Draw vertical segments (upper right, lower right, lower left, upper left)
    for i in [1, 2, 4, 5]:
        if segmentOn[i]:
            # Set vertical position
            if i == 1 or i == 5:  # upper segments
                startY = y
                endY = y + height // 2
            else:  # lower segments
                startY = y + height // 2
                endY = y + height
                
            # Set horizontal position
            if i == 4 or i == 5:  # left segments
                xOffset = 0
            else:  # right segments
                xOffset = width - thickness
                
            d.draw_block(x + xOffset, startY, thickness, endY - startY, color)

def update_screen(digit_val):
    # Clear screen with blue background
    d.fill_screen(BLUE_BACKGROUND)
    
    # Draw the digit in white
    drawDigit(digit_val, 50, 40, 40, 60, 8, WHITE_DIGIT)
    
    # Add text label
    d._color = WHITE_DIGIT  # Set text color to white
    d.p_string(10, 10, f'Digit: {digit_val}')

# Main loop
counter = 0
while True:
    update_screen(counter)
    sleep(1)
    counter = (counter + 1) % 10

```