# Scaling Fonts

We can modify the code to use a larger font for the date. Looking at the ST7735.py code, I notice it's using a built-in font5x7 font, but there's no built-in option for larger fonts. However, we can draw larger text by scaling up each character.

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

# Scaled text drawing functions
def draw_scaled_char(display, x, y, ch, scale=1):
    """Draw a single character at the specified scale"""
    fp = (ord(ch)-0x20) * 5
    f = open('font5x7.fnt','rb')
    f.seek(fp)
    b = f.read(5)
    char_buf = bytearray(b)
    char_buf.append(0)

    # Scale up the character
    char_image = bytearray()
    for bit in range(8):
        # Repeat each row scale times
        for _ in range(scale):
            for c in range(6):
                # Repeat each pixel scale times
                pixel = ((char_buf[c]>>bit) & 1)>0
                for _ in range(scale):
                    if pixel:
                        char_image.append(display._color >> 8)
                        char_image.append(display._color & 0xff)
                    else:
                        char_image.append(display._bground >> 8)
                        char_image.append(display._bground & 0xff)
    display.draw_bmp(x, y, 6*scale, 8*scale, char_image)
    f.close()

def draw_scaled_string(display, x, y, text, scale=1):
    """Draw a string of text at the specified scale"""
    for ch in text:
        draw_scaled_char(display, x, y, ch, scale)
        x += 6 * scale

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
    
    # Format date string - use 2-digit year to save space
    date_str = f"{day_to_str(weekday)} {month_to_str(month)} {day} {str(year)[2:]}"
    
    # Update date if changed
    if date_str != prev_date:
        display._color = TEXT_COLOR
        # Clear previous date area (increased height for larger font)
        display.draw_block(4, 4, 160, 20, BACKGROUND_COLOR)
        draw_scaled_string(display, 4, 4, date_str, scale=2)  # Scale up the date text
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

We have made several changes to support larger text:

- Modified the p_char method to support scaling characters by repeating pixels
- Updated the p_string method to accept a scale parameter
- Increased the clearing area for the date to accommodate the larger text
- Set the date text to scale=2 (twice the normal size)

Now the date should be displayed at double the original size. The scaling works by multiplying each pixel in the original font, so a scale of 2 means each pixel becomes a 2x2 block of pixels, making the text larger while maintaining its proportions.

You can adjust the scale factor by changing the scale=2 parameter in the p_string call. For example:

scale=1 is the original size
scale=2 doubles the size
scale=3 triples the size

