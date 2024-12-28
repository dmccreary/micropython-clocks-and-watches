from machine import Pin
from time import localtime, sleep
from mp_button import Button
import tm1637

CLK_PIN = 0
DST_PIN = 1

MODE_PIN = 16
NEXT_PIN = 17
PREVIOUS_PIN = 18

AM_PM_PIN = 25

mode_pin = Pin(MODE_PIN, Pin.IN, Pin.PULL_UP)
next_pin = Pin(NEXT_PIN, Pin.IN, Pin.PULL_UP)
previous_pin = Pin(PREVIOUS_PIN, Pin.IN, Pin.PULL_UP)
am_pm_pin = Pin(AM_PM_PIN, Pin.OUT)

tm = tm1637.TM1637(clk=Pin(0), dio=Pin(1))

mode = 0 # default clock running
mode_names = ["run","set hour","set minute","set AM/PM"]
mode_count = len(mode_names)
now = localtime()
hours = now[3]
minutes = now[4]
seconds = now[5]
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

# numbers modified to not dispaly the leading zero
def numbers_nlz(num1, num2, colon=True):
    """Display two numeric values -9 through 99, with a leading space before
    single-digit first numbers and separated by a colon."""
    num1 = max(-9, min(num1, 99))
    num2 = max(-9, min(num2, 99))
    prefix = ' ' if num1 < 10 else ''
    # print(f'"{prefix}{num1:d}{num2:0>2d}"')
    segments = tm.encode_string(f'{prefix}{num1:d}{num2:0>2d}')
    if colon:
        segments[1] |= 0x80  # colon on
    tm.write(segments)

counter = 0
while(True):
    button_mode.update()
    button_next.update()
    button_previous.update()
    if mode == 0:
        # flash the colon on and off every second
        if (seconds % 2): # modulo 2 will be true for odd numbers
            numbers_nlz(hours, minutes, True)
        else:
            numbers_nlz(hours, minutes, False)
        if hours > 12:
            am_pm_pin.value(1)
        else:
            am_pm_pin.value(0)
    elif mode == 1:
        # hours on and off every second
        if (seconds % 2): # modulo 2 will be true for odd numbers
            numbers_nlz(hours, minutes, True)
        else:
            numbers_nlz(None, minutes, False)
    elif mode == 2:
        # hours on and off every second
        if (seconds % 2): # modulo 2 will be true for odd numbers
            numbers_nlz(hour, minutes, True)
        else:
            numbers_nlz(hours, None, False)
    elif mode == 3:
        if (seconds % 2):
            am_pm_pin.value(1)
        else:
            am_pm_pin.value(0)
    print(counter, "m:", mode, hours, minutes, am_pm)
    sleep(1)
    counter += 1