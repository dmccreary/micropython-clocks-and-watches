from machine import Pin
from utime import localtime, sleep, ticks_ms, ticks_diff
import tm1637

# Pin setup
CLK_PIN = 0
DST_PIN = 1
PM_PIN = 25
mode_pin = Pin(16, Pin.IN, Pin.PULL_UP)
next_pin = Pin(17, Pin.IN, Pin.PULL_UP)
previous_pin = Pin(18, Pin.IN, Pin.PULL_UP)
pm_pin = Pin(PM_PIN, Pin.OUT)

# Time state
now = localtime()
hour = now[3]
minute = now[4]
second = now[5]
is_pm = hour >= 12  # Initialize is_pm based on current hour
tm = tm1637.TM1637(clk=Pin(CLK_PIN), dio=Pin(DST_PIN))
mode = 0
mode_names = ["run", "set hour", "set minute", "set AM/PM"]
mode_count = len(mode_names)

# Debounce state
last_mode_press = 0
last_next_press = 0
last_prev_press = 0
DEBOUNCE_MS = 300
last_flash = 0
FLASH_INTERVAL_MS = 500  # 1/2 second flash interval

def format_time():
    return f"{hour:d}:{minute:02d}:{second:02d} {'PM' if is_pm else 'AM'}"

def set_pm():
    global is_pm
    if hour < 12:
        is_pm = False
        pm_pin.value(0)
    else:
        is_pm = True
        pm_pin.value(1)

def handle_mode(pin):
    global mode, last_mode_press
    current_time = ticks_ms()
    if ticks_diff(current_time, last_mode_press) > DEBOUNCE_MS:
        mode = (mode + 1) % mode_count
        print(f"Mode: {mode_names[mode]}")
        last_mode_press = current_time

def handle_next(pin):
    global hour, minute, is_pm, last_next_press
    current_time = ticks_ms()
    if ticks_diff(current_time, last_next_press) > DEBOUNCE_MS:
        if mode == 1:  # Set hour
            hour = (hour % 12) + 1
        elif mode == 2:  # Set minute
            minute = (minute + 1) % 60
        elif mode == 3:  # Toggle AM/PM
            is_pm = not is_pm
            pm_pin.value(1 if is_pm else 0)
        
        if mode != 0:
            print(format_time())
        last_next_press = current_time

def handle_previous(pin):
    global hour, minute, is_pm, last_prev_press
    current_time = ticks_ms()
    if ticks_diff(current_time, last_prev_press) > DEBOUNCE_MS:
        if mode == 1:  # Set hour
            hour = ((hour - 2) % 12) + 1
        elif mode == 2:  # Set minute
            minute = (minute - 1) % 60
        elif mode == 3:  # Toggle AM/PM
            is_pm = not is_pm
            pm_pin.value(1 if is_pm else 0)
        
        if mode != 0:
            print(format_time())
        last_prev_press = current_time

def numbers_nlz(num1, num2, colon=True, flash_state=False, flash_mode=None):
    """Display two numeric values with flashing capability
    flash_mode can be 'hour', 'minute', or None"""
    num1 = max(-9, min(num1, 99))
    num2 = max(-9, min(num2, 99))
    prefix = ' ' if num1 < 10 else ''
    
    if flash_state and flash_mode == 'hour':
        # Flash only hour by using spaces for hour digits
        segments = tm.encode_string(f'  {num2:0>2d}')
    elif flash_state and flash_mode == 'minute':
        # Flash only minutes by using spaces for minute digits
        segments = tm.encode_string(f'{prefix}{num1:d}  ')
    else:
        # Normal display
        segments = tm.encode_string(f'{prefix}{num1:d}{num2:0>2d}')
    
    if colon:
        segments[1] |= 0x80  # colon on
    tm.write(segments)

# Set up interrupts
mode_pin.irq(trigger=Pin.IRQ_FALLING, handler=handle_mode)
next_pin.irq(trigger=Pin.IRQ_FALLING, handler=handle_next)
previous_pin.irq(trigger=Pin.IRQ_FALLING, handler=handle_previous)

# Main loop
print("Clock started. Press mode button to change settings.")
while True:
    current_time = ticks_ms()
    flash_state = (ticks_diff(current_time, last_flash) // FLASH_INTERVAL_MS) % 2
    
    if ticks_diff(current_time, last_flash) >= FLASH_INTERVAL_MS:
        last_flash = current_time
    
    second = localtime()[5]
    
    if mode == 0:  # Normal run mode
        numbers_nlz(hour, minute, second % 2)
        pm_pin.value(1 if is_pm else 0)
    elif mode == 1:  # Set hour mode
        numbers_nlz(hour, minute, True, flash_state, 'hour')
        pm_pin.value(1 if is_pm else 0)
    elif mode == 2:  # Set minute mode
        numbers_nlz(hour, minute, True, flash_state, 'minute')
        pm_pin.value(1 if is_pm else 0)
    elif mode == 3:  # Set AM/PM mode
        numbers_nlz(hour, minute, True)
        # Flash the PM LED
        pm_pin.value(0 if flash_state else (1 if is_pm else 0))
    
    sleep(0.1)  # Shorter sleep for more responsive flashing