# Dirty Drawing

We need to modify the clock program to minimize flicker by only updating the parts of the display that change. This requires tracking the previous state and only redrawing digits that have changed. Here's how we can improve it:

The key improvements in this version include:

1. State Tracking: Added global variables to track the previous state of all display elements (digits, date, AM/PM, etc.)

2. Selective Updates: Only redraws elements that have changed since the last update:
   - Digits are only redrawn when their values change
   - The date is only updated when it changes
   - AM/PM indicator only updates when switching between AM and PM
   - The colon blinks by only updating its small area

3. Localized Clearing: Instead of clearing the entire screen:
   - Each digit area is cleared individually before redrawing
   - Text areas are cleared in their specific regions before updating

4. Initialization Handling: Added a `screen_initialized` flag to ensure the background is only drawn once at startup

5. Improved Update Rate: Reduced the sleep time to 0.1 seconds for smoother updates while still maintaining efficiency

These changes should significantly reduce the flicker since we're only updating the parts of the screen that actually change. The blue background will now only be drawn once at startup, and subsequent updates will be localized to the specific areas that need to change.

To use this improved version, simply replace the contents of your existing clock-main-with-flicker.py with this new code. The functionality remains the same, but the display should be much more stable with minimal flicker.

this is a great example of how selective updates can make a big difference in display quality. Instead of redrawing the entire screen 10 times per second, we're now only updating the specific segments that change.
For example, when displaying "12:59", only the ":59" portion will update frequently. The "12" will stay static until it changes to "1:00". The colons blink by just toggling those few pixels rather than redrawing everything.

This technique (known as "dirty rectangle" updating in graphics programming) is especially important for displays like the ST7735 where each pixel update takes a non-trivial amount of time. By minimizing the number of pixels we need to update, we get both better performance and a cleaner visual result.

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

# Previous state tracking
prev_date = ""
prev_hour_ten = -1
prev_hour_right = -1
prev_minute_ten = -1
prev_minute_right = -1
prev_second = -1
prev_am_pm = ""
screen_initialized = False

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

def clear_digit_area(x, y, width, height, color):
    """Clear the area where a digit was previously drawn."""
    display.draw_block(x, y, width, height, color)

def drawDigit(digit, x, y, width, height, thickness, color):
    """Draw a seven-segment digit on the display."""
    if digit < 0:
        return
        
    # Clear the area first
    clear_digit_area(x, y, width, height, BACKGROUND_COLOR)
    
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
    """Update only the changing parts of the display."""
    global prev_date, prev_hour_ten, prev_hour_right, prev_minute_ten
    global prev_minute_right, prev_second, prev_am_pm, screen_initialized
    
    # Initialize screen on first run
    if not screen_initialized:
        display.fill_screen(BACKGROUND_COLOR)
        screen_initialized = True
    
    # Calculate positions
    left_margin = -15
    y_offset = 30
    digit_width = 32
    digit_height = 50
    digit_spacing = 42
    digit_thickness = 6
    
    # Convert 24-hour to 12-hour format
    display_hour = hour if hour <= 12 else hour - 12
    if display_hour == 0:
        display_hour = 12
    
    # Format date string
    date_str = f"{day_to_str(weekday)} {month_to_str(month)} {day} {year}"
    
    # Update date if changed
    if date_str != prev_date:
        display._color = TEXT_COLOR
        # Clear previous date area
        display.draw_block(4, 4, 160, 10, BACKGROUND_COLOR)
        display.p_string(4, 4, date_str)
        prev_date = date_str
    
    # Split time into digits
    hour_ten = display_hour // 10 if display_hour >= 10 else -1
    hour_right = display_hour % 10
    minute_ten = minute // 10
    minute_right = minute % 10
    
    # Update digits only if they've changed
    if hour_ten != prev_hour_ten:
        drawDigit(hour_ten, left_margin, y_offset, digit_width, digit_height, digit_thickness, DIGIT_COLOR)
        prev_hour_ten = hour_ten
        
    if hour_right != prev_hour_right:
        drawDigit(hour_right, left_margin + digit_spacing, y_offset, digit_width, digit_height, digit_thickness, DIGIT_COLOR)
        prev_hour_right = hour_right
        
    if minute_ten != prev_minute_ten:
        drawDigit(minute_ten, left_margin + 2*digit_spacing+10, y_offset, digit_width, digit_height, digit_thickness, DIGIT_COLOR)
        prev_minute_ten = minute_ten
        
    if minute_right != prev_minute_right:
        drawDigit(minute_right, left_margin + 3*digit_spacing+10, y_offset, digit_width, digit_height, digit_thickness, DIGIT_COLOR)
        prev_minute_right = minute_right

    # Handle colon blinking - clear and redraw based on seconds
    colon_x = left_margin + digit_spacing + digit_width + 8
    colon_y = y_offset + 15
    if second % 2:
        draw_colon(colon_x, colon_y, DIGIT_COLOR)
    else:
        draw_colon(colon_x, colon_y, BACKGROUND_COLOR)

    # Update AM/PM indicator if needed
    am_pm_str = "PM" if hour >= 12 else "AM"
    if am_pm_str != prev_am_pm:
        display._color = TEXT_COLOR
        display.draw_block(left_margin + 3*digit_spacing + digit_width, y_offset + 60, 20, 10, BACKGROUND_COLOR)
        display.p_string(left_margin + 3*digit_spacing + digit_width, y_offset + 60, am_pm_str)
        prev_am_pm = am_pm_str
    
    # Update seconds display if changed
    if second != prev_second:
        display._color = TEXT_COLOR
        display.draw_block(4, y_offset + digit_height + 10, 20, 10, BACKGROUND_COLOR)
        display.p_string(4, y_offset + digit_height + 10, f"{second:02d}")
        prev_second = second

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
    sleep(0.1)  # Shorter sleep for more responsive updates
```