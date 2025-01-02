from machine import Pin, I2C
from sh1106 import SH1106_I2C
from utime import sleep

# OLED and RTC share I2C bus 0
OLED_SH11306_SDA_PIN = 0
OLED_SH11306_SCL_PIN = 1
DS3231_ADDR = 0x68

sda = Pin(OLED_SH11306_SDA_PIN, Pin.OUT)
scl = Pin(OLED_SH11306_SCL_PIN, Pin.OUT)

# freq=3000000 (3M) for safe I2C operation with both devices
i2c = I2C(0, scl=scl, sda=sda, freq=3000000)

# Initialize display and RTC
oled = SH1106_I2C(128, 64, i2c)
oled.rotate(180)

def bcd2dec(bcd):
    """Convert binary coded decimal to decimal."""
    return (((bcd & 0xf0) >> 4) * 10 + (bcd & 0x0f))

def read_ds3231():
    """Read time from DS3231 RTC."""
    data = i2c.readfrom_mem(DS3231_ADDR, 0x00, 7)
    second = bcd2dec(data[0])
    minute = bcd2dec(data[1])
    hour = bcd2dec(data[2] & 0x3f)  # 24 hour mode
    day = bcd2dec(data[4])
    month = bcd2dec(data[5] & 0x1f)
    year = bcd2dec(data[6]) + 2000
    return (year, month, day, hour, minute, second)

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
    if digit < 0:
        return
    segmentOn = segmentMapping[digit]

    # Draw horizontal segments
    for i in [0, 3, 6]:
        if segmentOn[i]:
            if i == 0:  # top
                yOffset = 0
            elif i == 3:  # bottom
                yOffset = height - thickness
            else:  # middle
                yOffset = height // 2 - thickness // 2
            oled.fill_rect(x, y+yOffset, width, thickness, color)

    # Draw vertical segments
    for i in [1, 2, 4, 5]:
        if segmentOn[i]:
            if i == 1 or i == 5:  # upper segments
                startY = y
                endY = y + height // 2
            else:  # lower segments
                startY = y + height // 2
                endY = y + height
            xOffset = 0 if (i == 4 or i == 5) else width-thickness
            oled.fill_rect(x+xOffset, startY, thickness, endY-startY, color)

def draw_colon(x, y):
    oled.fill_rect(x, y, 3, 3, 1)
    oled.fill_rect(x, y+14, 3, 3, 1)

def update_screen(year, month, day, hour, minute, am_pm, colon_on):
    left_margin = -28
    y_offset = 11
    digit_width = 33
    digit_height = 40
    digit_spacing = 41
    digit_thickness = 5

    oled.fill(0)
    date_str = f"{month}/{day}/{year}"
    oled.text(date_str, 0, 0, 1)

    # Convert 24-hour to 12-hour format
    display_hour = hour if hour <= 12 else hour - 12
    if display_hour == 0:
        display_hour = 12

    hour_ten = display_hour // 10 if display_hour >= 10 else -1
    hour_right = display_hour % 10
    minute_ten = minute // 10
    minute_right = minute % 10

    drawDigit(hour_ten, left_margin, y_offset, digit_width, digit_height, digit_thickness, 1)
    drawDigit(hour_right, left_margin + digit_spacing-2, y_offset, digit_width, digit_height, digit_thickness, 1)
    drawDigit(minute_ten, left_margin + 2*digit_spacing, y_offset, digit_width, digit_height, digit_thickness, 1)
    drawDigit(minute_right, left_margin + 3*digit_spacing, y_offset, digit_width, digit_height, digit_thickness, 1)

    if colon_on:
        draw_colon(47, 20)

    oled.text(am_pm, 106, 55, 1)
    oled.show()

counter = 0
while True:
    now = read_ds3231()
    year, month, day, hour, minute, second = now
    am_pm = "PM" if hour >= 12 else "AM"

    update_screen(year, month, day, hour, minute, am_pm, True)
    sleep(1)
    update_screen(year, month, day, hour, minute, am_pm, False)
    sleep(1)
    counter += 1
    if counter > 9:
        counter = 0