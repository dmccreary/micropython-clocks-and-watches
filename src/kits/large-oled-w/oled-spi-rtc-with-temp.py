from machine import Pin, I2C
import utime
import ssd1306
from utime import sleep, localtime
led = machine.Pin(25, machine.Pin.OUT)

SCL = machine.Pin(2)  # SPI CLock
SDA = machine.Pin(3)  # SPI Data
spi = machine.SPI(0, sck=SCL, mosi=SDA, baudrate=100000)

RES = machine.Pin(4)
DC = machine.Pin(5)
CS = machine.Pin(6)

oled = ssd1306.SSD1306_SPI(128, 64, spi, DC, RES, CS)
DS3231_ADDR = 0x68

i2c = I2C(0, sda=Pin(0), scl=Pin(1))

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

def read_temperature():
    """Read temperature from DS3231 RTC."""
    # Read temperature registers
    i2c.writeto(DS3231_ADDR, b'\x11')
    temp_data = i2c.readfrom(DS3231_ADDR, 2)
    temp_msb = temp_data[0]
    temp_lsb = temp_data[1]
    
    # Get raw temp value (ignoring sign bit)
    raw_temp = temp_msb & 0x7F  # Strip off sign bit
    
    # 0xD7 & 0x7F = 0x57 = 87 decimal (original value minus sign bit)
    # If sign bit was set, make it negative
    if temp_msb & 0x80:
        raw_temp = raw_temp ^ 0x7F  # Invert the bits
        raw_temp = -(raw_temp + 1)  # Two's complement
    
    # Add fraction from LSB
    frac = (temp_lsb >> 6) * 0.25
    temp_c = raw_temp + frac
    
    # Convert to Fahrenheit
    temp_f = (temp_c * 9.0 / 5.0) + 32.0
    
    print(f"Raw temp (after sign bit removal): {raw_temp}")
    print(f"Temperature: {temp_c}°C = {temp_f}°F")
    
    return temp_f

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

def update_screen(year, month, day, hour, minute, am_pm, colon_on, temp_f):
    left_margin = -28
    y_offset = 11
    digit_width = 33
    digit_height = 40
    digit_spacing = 41
    digit_thickness = 5

    oled.fill(0)
    
    # Draw date at top
    date_str = f"{month}/{day}/{year}"
    oled.text(date_str, 0, 0, 1)

    # Draw temperature at top right (both C and F)
    temp_str = f"{temp_f:.1f}F"
    oled.text(temp_str, 0, 54, 1)

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
    
    # Read temperature from RTC
    temp_f = read_temperature()

    update_screen(year, month, day, hour, minute, am_pm, True, temp_f)
    sleep(1)
    update_screen(year, month, day, hour, minute, am_pm, False, temp_f)
    sleep(1)
    counter += 1
    if counter > 9:
        counter = 0