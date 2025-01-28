from utime import sleep
from machine import Pin

# Sample Raspberry Pi Pico MicroPython three button press example

# Global Variable Default Settings
mode=0
hour=6
minute=30
pm_indicator = True
mode_names = ['run', 'set hour', 'set minute', 'set AM/PM']
mode_count = len(mode_names)

# Button Pin GPIO Configuration
CHANGE_MODE_PIN = 13
INCREMENT_PIN = 14
DECREMENT_PIN = 15

# Create 3 button objects as inputs with pullup resistors
change_mode_pin = Pin(CHANGE_MODE_PIN, Pin.IN, Pin.PULL_UP)
increment_pin = Pin(INCREMENT_PIN, Pin.IN, Pin.PULL_UP)
decrement_pin = Pin(DECREMENT_PIN, Pin.IN, Pin.PULL_UP)

# These functions gets called every time a button is pressed.
def mode_button_pressed(pin):
    global mode
    mode += 1
    mode = mode % mode_count
    
def increment_button_pressed(pin):
    global mode, hour, minute, pm_indicator
    if mode == 1:
        hour += 1
        # hour goes from 1 to 12
        hour = (hour % 12) + 1
    if mode == 2:
        minute += 1
        minute = minute % 12
    if mode == 3:
        pm_indicator = not pm_indicator

def decrement_button_pressed(pin):
    global mode, hour, minute, pm_indicator
    if mode == 1:
        hour -= 1
        # hour goes from 1 to 12
        hour = (hour % 12) + 1
    if mode == 2:
        minute -= 1
        minute = minute % 12
    if mode == 3:
        pm_indicator = not pm_indicator
    
# now we register the button handler functions using the irq setter method for each pin
change_mode_pin.irq(trigger=Pin.IRQ_FALLING, handler = mode_button_pressed)
increment_pin.irq(trigger=Pin.IRQ_FALLING, handler = increment_button_pressed)
decrement_pin.irq(trigger=Pin.IRQ_FALLING, handler = decrement_button_pressed)

# only print on change - these variables store the old values
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
        last_minute = minute
    sleep(.01)