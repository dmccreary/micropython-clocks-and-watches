from mp_button import Button
from time import localtime, sleep
from machine import Pin

mode_pin = Pin(16, Pin.IN, Pin.PULL_UP)
next_pin = Pin(17, Pin.IN, Pin.PULL_UP)
previous_pin = Pin(18, Pin.IN, Pin.PULL_UP)

# we create a counter to increment as we press
# and one to increment as we release
counter_pressed = 0
counter_released = 0
mode = 0 # default clock running
mode_names = ["run","set hour","set minute","set AM/PM"]
mode_count = len(mode_names)
now = localtime()
hours = now[3]
minutes = now[4]
am_pm = 0

# the following method (function) will be invoked
# when the button changes state
# the Button module expects a callback to handle 
# - pin number
# - event (Button.PRESSED | Button.RELEASED)
# the event contains a string 'pressed' or 'released'
# which can be used in your code to act upon
def button_mode_irq(button, event):
    global mode, hours, minutes
    if event == Button.PRESSED:
        mode +=1
        # cycle back to zero if greater than mode_count
        mode =  mode % mode_count
        print('new mode:', mode, mode_names[mode])

def button_next_irq(button, event):
    global mode, hours, minutes, am_pm
    if event == Button.PRESSED:
        if mode == 1:
            hours += 1
        if mode == 2:
            minutes += 1
        if mode == 3:
            if am_pm == 0:
                am_pm = 1
            else:
                am_pm = 0
        print('next button:', hours, minutes, am_pm)
            
def button_previous_irq(button, event):
    global mode, hours, minutes, am_pm
    if event == Button.PRESSED:
        if mode == 1:
            hours -= 1
        if mode == 2:
            minutes -= 1
        if mode == 3:
            if am_pm == 0:
                am_pm = 1
            else:
                am_pm = 0
        print('prev button:', hours, minutes, am_pm)

button_mode = Button(16, False, button_mode_irq, internal_pullup = True, debounce_time = 100)
button_next = Button(17, False, button_next_irq, internal_pullup = True, debounce_time = 100)
button_previous = Button(18, False, button_previous_irq, internal_pullup = True, debounce_time = 100)

print("year:", now[0], "month:", now[1], "day-of-month:", now[2], "hours", now[3], "minutes:", now[4])
while(True):
    button_mode.update()
    button_next.update()
    button_previous.update()