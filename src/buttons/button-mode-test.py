from machine import Pin
from utime import localtime, sleep, ticks_ms, ticks_diff

# Pin setup
mode_pin = Pin(16, Pin.IN, Pin.PULL_UP)
next_pin = Pin(17, Pin.IN, Pin.PULL_UP)
previous_pin = Pin(18, Pin.IN, Pin.PULL_UP)

# Time state
now = localtime()
hour = now[3]
minute = now[4]
if hour < 12:
    is_pm = False
else:
    is_pm = True
mode = 0
mode_names = ["run", "set hour", "set minute", "set AM/PM"]
mode_count = len(mode_names)

# Debounce state
last_mode_press = 0
last_next_press = 0
last_prev_press = 0
DEBOUNCE_MS = 200

def format_time():
    return f"{hour:d}:{minute:02d} {'PM' if is_pm else 'AM'}"

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
        
        if mode != 0:
            print(format_time())
        last_prev_press = current_time

# Set up interrupts
mode_pin.irq(trigger=Pin.IRQ_FALLING, handler=handle_mode)
next_pin.irq(trigger=Pin.IRQ_FALLING, handler=handle_next)
previous_pin.irq(trigger=Pin.IRQ_FALLING, handler=handle_previous)

# Main loop
print("Clock started. Press mode button to change settings.")
while True:
    if mode == 0:  # Only update display in run mode
        print(format_time())
        sleep(1)