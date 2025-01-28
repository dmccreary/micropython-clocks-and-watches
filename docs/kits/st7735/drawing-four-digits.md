# Drawing Digits

Let's now draw four digits on the screen.
This will have a lot of flicker which we will clean up in the next version.

```python
from machine import Pin, SPI
from utime import sleep, localtime
import ST7735
import config

# Initialize SPI and display
spi = machine.SPI(config.SPI_BUS, 
                  sck=Pin(config.SPI_SCL_PIN),
                  mosi=Pin(config.SPI_SDA_PIN),
                  baudrate=8000000)

display = ST7735.ST7735(spi, 
                        rst=config.SPI_RESET_PIN,
                        ce=config.SPI_CS_PIN,
                        dc=config.SPI_DC_PIN)
display.reset()
display.begin()
display.set_rotation(config.DISPLAY_ROTATION)

# Define colors using RGB565 format
BACKGROUND_COLOR = display.rgb_to_565(0, 0, 255)  # Blue background
DIGIT_COLOR = display.rgb_to_565(255, 255, 255)   # White for digits
TEXT_COLOR = display.rgb_to_565(255, 255, 0)      # Yellow for text

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

def day_to_str(day_num):
    """Convert a day number (0-6) to a three-letter day abbreviation."""
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    if not 0 <= day_num <= 6:
        raise ValueError("Day number must be between 0 and 6")
    return days[day_num]

def month_to_str(month_num):
    """Convert a month number (1-12) to a three-letter month abbreviation."""
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
             'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    if not 1 <= month_num <= 12:
        raise ValueError("Month number must be between 1 and 12")
    return months[month_num - 1]

def drawDigit(digit, x, y, width, height, thickness, color):
    """Draw a seven-segment digit on the display."""
    if digit < 0:
        return
    segmentOn = segmentMapping[digit]

    # Draw horizontal segments (top, middle, bottom)
    for i in [0, 3, 6]:
        if segmentOn[i]:
            if i == 0:  # top
                yOffset = 0
            elif i == 3:  # bottom
                yOffset = height - thickness
            else:  # middle
                yOffset = height // 2 - thickness // 2
            display.draw_block(x, y + yOffset, width, thickness, color)

    # Draw vertical segments
    for i in [1, 2, 4, 5]:
        if segmentOn[i]:
            if i == 1 or i == 5:  # upper segments
                startY = y
                endY = y + height // 2
            else:  # lower segments
                startY = y + height // 2
                endY = y + height
            xOffset = 0 if (i == 4 or i == 5) else width - thickness
            display.draw_block(x + xOffset, startY, thickness, endY - startY, color)

def draw_colon(x, y, color):
    """Draw the blinking colon between hours and minutes."""
    display.draw_block(x, y, 4, 4, color)
    display.draw_block(x, y + 14, 4, 4, color)

def update_screen(year, month, day, hour, minute, second, weekday):
    """Update the entire display with the current time and date."""
    # Clear screen with background color
    display.fill_screen(BACKGROUND_COLOR)
    
    # Set text color for the date
    display._color = TEXT_COLOR
    
    # Display the date at the top
    date_str = f"{day_to_str(weekday)} {month_to_str(month)} {day} {year}"
    display.p_string(4, 4, date_str)

    # Convert 24-hour to 12-hour format
    display_hour = hour if hour <= 12 else hour - 12
    if display_hour == 0:
        display_hour = 12

    # Calculate digit positions
    left_margin = -15
    y_offset = 30
    digit_width = 32
    digit_height = 50
    digit_spacing = 42
    digit_thickness = 6

    # Split hours and minutes into digits
    hour_ten = display_hour // 10 if display_hour >= 10 else -1
    hour_right = display_hour % 10
    minute_ten = minute // 10
    minute_right = minute % 10

    # Draw all digits
    drawDigit(hour_ten, left_margin, y_offset, digit_width, digit_height, digit_thickness, DIGIT_COLOR)
    drawDigit(hour_right, left_margin + digit_spacing, y_offset, digit_width, digit_height, digit_thickness, DIGIT_COLOR)
    drawDigit(minute_ten, left_margin + 2*digit_spacing+10, y_offset, digit_width, digit_height, digit_thickness, DIGIT_COLOR)
    drawDigit(minute_right, left_margin + 3*digit_spacing+10, y_offset, digit_width, digit_height, digit_thickness, DIGIT_COLOR)

    # Draw the colon if it's an even second (for blinking effect)
    if second % 2:
        draw_colon(left_margin + digit_spacing + digit_width + 8, y_offset + 15, DIGIT_COLOR)

    # Display AM/PM indicator
    display._color = TEXT_COLOR
    am_pm_str = "PM" if hour >= 12 else "AM"
    display.p_string(left_margin + 3*digit_spacing + digit_width, y_offset + 60, am_pm_str)
    
    # Display seconds
    display.p_string(4, y_offset + digit_height + 10, f"{second}")

# Main loop
while True:
    now = localtime()
    year = now[0]
    month = now[1]
    day = now[2]
    hour = now[3]
    minute = now[4]
    second = now[5]
    weekday = now[6]
    
    update_screen(year, month, day, hour, minute, second, weekday)
    sleep(1)
```