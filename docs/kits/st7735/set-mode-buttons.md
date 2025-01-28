# Set the Mode Buttons

We need a way to monitor the Set/Mode, Increment and Decrement buttons
to manually set the time.  Here is a program that
will monitor the three buttons and change the mode.

```python
from utime import sleep, ticks_ms, ticks_diff
from machine import Pin

# Global Variable Default Settings
mode = 0
hour = 6
minute = 30
pm_indicator = True
mode_names = ['run', 'set hour', 'set minute', 'set AM/PM']
mode_count = len(mode_names)

# Button Pin GPIO Configuration
CHANGE_MODE_PIN = 13
INCREMENT_PIN = 14
DECREMENT_PIN = 15
DEBOUNCE_TIME_MS = 200

# Create 3 button objects as inputs with pullup resistors
change_mode_pin = Pin(CHANGE_MODE_PIN, Pin.IN, Pin.PULL_UP)
increment_pin = Pin(INCREMENT_PIN, Pin.IN, Pin.PULL_UP)
decrement_pin = Pin(DECREMENT_PIN, Pin.IN, Pin.PULL_UP)

# Variables to track last button press times for debouncing
last_mode_press = 0
last_increment_press = 0
last_decrement_press = 0

# These functions gets called every time a button is pressed
def mode_button_pressed(pin):
    global mode, last_mode_press
    current_time = ticks_ms()
    if ticks_diff(current_time, last_mode_press) > DEBOUNCE_TIME_MS:
        mode += 1
        mode = mode % mode_count
        last_mode_press = current_time
    
def increment_button_pressed(pin):
    global mode, hour, minute, pm_indicator, last_increment_press
    current_time = ticks_ms()
    if ticks_diff(current_time, last_increment_press) > DEBOUNCE_TIME_MS:
        if mode == 1:
            hour = (hour % 12) + 1  # Increment hour from 1-12 properly
        if mode == 2:
            minute += 1
            minute = minute % 60  # Fixed: minute should go from 0 to 59
        if mode == 3:
            pm_indicator = not pm_indicator
        last_increment_press = current_time

def decrement_button_pressed(pin):
    global mode, hour, minute, pm_indicator, last_decrement_press
    current_time = ticks_ms()
    if ticks_diff(current_time, last_decrement_press) > DEBOUNCE_TIME_MS:
        if mode == 1:
            hour -= 1
            if hour <= 0:  # Handle wrapping from 1 to 12
                hour = 12
        if mode == 2:
            minute -= 1
            if minute < 0:  # Handle wrapping from 0 to 59
                minute = 59
        if mode == 3:
            pm_indicator = not pm_indicator
        last_decrement_press = current_time
    
# Register the button handler functions using the irq setter method for each pin
change_mode_pin.irq(trigger=Pin.IRQ_FALLING, handler=mode_button_pressed)
increment_pin.irq(trigger=Pin.IRQ_FALLING, handler=increment_button_pressed)
decrement_pin.irq(trigger=Pin.IRQ_FALLING, handler=decrement_button_pressed)

# Only print on change - these variables store the old values
last_mode = mode
last_hour = hour
last_minute = minute
last_pm_indicator = pm_indicator
print("Default values: mode:", mode, "hour:", hour, "minute:", minute, "pm indicator:", pm_indicator)

while True:
    if mode != last_mode:
        print("new mode:", mode, mode_names[mode])
        last_mode = mode
    if hour != last_hour:
        print("new hour:", hour)
        last_hour = hour
    if minute != last_minute:
        print("new minute:", minute)
        last_minute = minute
    if pm_indicator != last_pm_indicator:
        print("new pm indicator:", pm_indicator)
        last_pm_indicator = pm_indicator
    # sleep(.01)
```