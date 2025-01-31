from machine import Pin, I2C, SPI
from utime import sleep, ticks_ms, ticks_diff
from ds3231 import DS3231
import ssd1306
import config

# Display setup
SCL = Pin(config.SPI_SCL_PIN)
SDA = Pin(config.SPI_SDA_PIN)
DC = Pin(config.SPI_DC_PIN)
RES = Pin(config.SPI_RESET_PIN)
CS = Pin(config.SPI_CS_PIN)
spi = SPI(config.SPI_BUS, sck=SCL, mosi=SDA, baudrate=1000000)
oled = ssd1306.SSD1306_SPI(config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT, spi, DC, RES, CS)

# RTC setup
i2c = I2C(config.I2C_BUS, sda=Pin(config.I2C_SDA_PIN), scl=Pin(config.I2C_SCL_PIN))
rtc = DS3231(i2c)

# Button setup
mode_button = Pin(config.BUTTON_MODE_PIN, Pin.IN, Pin.PULL_UP)
increment_button = Pin(config.BUTTON_INCREMENT_PIN, Pin.IN, Pin.PULL_UP)
decrement_button = Pin(config.BUTTON_DECREMENT_PIN, Pin.IN, Pin.PULL_UP)

# Global variables
mode = 0  # 0=run, 1=set hour, 2=set minute, 3=set AM/PM
last_mode_press = 0
last_increment_press = 0
last_decrement_press = 0
DEBOUNCE_TIME_MS = 250
mode_names = ['run', 'set hour', 'set minute', 'set AM/PM']
flash_state = False
last_flash_toggle = 0
FLASH_INTERVAL_MS = 500

# Seven segment display configuration
segment_mapping = [
    [1, 1, 1, 1, 1, 1, 0],  # 0
    [0, 1, 1, 0, 0, 0, 0],  # 1
    [1, 1, 0, 1, 1, 0, 1],  # 2
    [1, 1, 1, 1, 0, 0, 1],  # 3
    [0, 1, 1, 0, 0, 1, 1],  # 4
    [1, 0, 1, 1, 0, 1, 1],  # 5
    [1, 0, 1, 1, 1, 1, 1],  # 6
    [1, 1, 1, 0, 0, 0, 0],  # 7
    [1, 1, 1, 1, 1, 1, 1],  # 8
    [1, 1, 1, 1, 0, 1, 1]   # 9
]

def draw_digit(digit, x, y, width, height, thickness, color):
    if digit < 0:
        return
    segment_on = segment_mapping[digit]

    # Horizontal segments
    for i in [0, 3, 6]:
        if segment_on[i]:
            if i == 0:  # top
                y_offset = 0
            elif i == 3:  # bottom
                y_offset = height - thickness
            else:  # middle
                y_offset = height // 2 - thickness // 2
            oled.fill_rect(x, y + y_offset, width, thickness, color)

    # Vertical segments
    for i in [1, 2, 4, 5]:
        if segment_on[i]:
            if i == 1 or i == 5:  # upper
                start_y = y
                end_y = y + height // 2
            else:  # lower
                start_y = y + height // 2
                end_y = y + height
            x_offset = 0 if (i == 4 or i == 5) else width - thickness
            oled.fill_rect(x + x_offset, start_y, thickness, end_y - start_y, color)

def draw_colon(x, y):
    oled.fill_rect(x, y, 3, 3, 1)
    oled.fill_rect(x, y + 14, 3, 3, 1)

def update_screen(hour, minute, second):
    global flash_state, mode
    oled.fill(0)
    
    # Display settings
    left_margin = -28
    y_offset = 11
    digit_width = 33
    digit_height = 40
    digit_spacing = 41
    digit_thickness = 5
    
    # Convert to 12-hour format
    is_pm = hour >= 12
    display_hour = hour if hour <= 12 else hour - 12
    if display_hour == 0:
        display_hour = 12

    hour_ten = display_hour // 10 if display_hour >= 10 else -1
    hour_one = display_hour % 10
    minute_ten = minute // 10
    minute_one = minute % 10

    # Draw digits with flashing based on mode
    if mode != 1 or flash_state:
        draw_digit(hour_ten, left_margin, y_offset, digit_width, digit_height, digit_thickness, 1)
        draw_digit(hour_one, left_margin + digit_spacing - 2, y_offset, digit_width, digit_height, digit_thickness, 1)
    
    if mode != 2 or flash_state:
        draw_digit(minute_ten, left_margin + 2 * digit_spacing, y_offset, digit_width, digit_height, digit_thickness, 1)
        draw_digit(minute_one, left_margin + 3 * digit_spacing, y_offset, digit_width, digit_height, digit_thickness, 1)

    if second % 2:
        draw_colon(47, 20)

    # Draw AM/PM
    if mode != 3 or flash_state:
        oled.text("PM" if is_pm else "AM", 112, 55, 1)
    
    oled.text(str(second), 0, 54, 1)
    oled.show()

def mode_button_pressed(pin):
    global mode, last_mode_press
    current_time = ticks_ms()
    if ticks_diff(current_time, last_mode_press) > DEBOUNCE_TIME_MS:
        mode = (mode + 1) % len(mode_names)
        last_mode_press = current_time
        print(f"Mode button pressed - New mode: {mode_names[mode]}")

def increment_button_pressed(pin):
    global last_increment_press
    current_time = ticks_ms()
    if ticks_diff(current_time, last_increment_press) > DEBOUNCE_TIME_MS:
        print("Increment button pressed")
        if mode == 1:  # Hour
            current_time = list(rtc.datetime())
            hour = current_time[4]
            hour = (hour + 1) if hour < 23 else 0
            current_time[4] = hour
            rtc.datetime(tuple(current_time))
            print(f"Hour adjusted to: {hour}")
        elif mode == 2:  # Minute
            current_time = list(rtc.datetime())
            minute = current_time[5]
            minute = (minute + 1) if minute < 59 else 0
            current_time[5] = minute
            rtc.datetime(tuple(current_time))
            print(f"Minute adjusted to: {minute}")
        elif mode == 3:  # AM/PM
            current_time = list(rtc.datetime())
            hour = current_time[4]
            hour = (hour + 12) % 24
            current_time[4] = hour
            rtc.datetime(tuple(current_time))
            print(f"Hour adjusted to: {hour} ({('AM', 'PM')[hour >= 12]})")
        last_increment_press = current_time

def decrement_button_pressed(pin):
    global last_decrement_press
    current_time = ticks_ms()
    if ticks_diff(current_time, last_decrement_press) > DEBOUNCE_TIME_MS:
        print("Decrement button pressed")
        if mode == 1:  # Hour
            current_time = list(rtc.datetime())
            hour = current_time[4]
            hour = (hour - 1) if hour > 0 else 23
            current_time[4] = hour
            rtc.datetime(tuple(current_time))
            print(f"Hour adjusted to: {hour}")
        elif mode == 2:  # Minute
            current_time = list(rtc.datetime())
            minute = current_time[5]
            minute = (minute - 1) if minute > 0 else 59
            current_time[5] = minute
            rtc.datetime(tuple(current_time))
            print(f"Minute adjusted to: {minute}")
        elif mode == 3:  # AM/PM
            current_time = list(rtc.datetime())
            hour = current_time[4]
            hour = (hour + 12) % 24
            current_time[4] = hour
            rtc.datetime(tuple(current_time))
            print(f"Hour adjusted to: {hour} ({('AM', 'PM')[hour >= 12]})")
        last_decrement_press = current_time

# Setup button interrupts
mode_button.irq(trigger=Pin.IRQ_FALLING, handler=mode_button_pressed)
increment_button.irq(trigger=Pin.IRQ_FALLING, handler=increment_button_pressed)
decrement_button.irq(trigger=Pin.IRQ_FALLING, handler=decrement_button_pressed)

print("Clock started in mode: run")

# Main loop
while True:
    current_time = rtc.datetime()
    current_ms = ticks_ms()
    
    # Update flash state every FLASH_INTERVAL_MS
    if ticks_diff(current_ms, last_flash_toggle) >= FLASH_INTERVAL_MS:
        flash_state = not flash_state
        last_flash_toggle = current_ms
    
    # Update display
    update_screen(current_time[4], current_time[5], current_time[6])
    sleep(0.1)