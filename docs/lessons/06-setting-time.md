# Manually Setting Time

We need a program that will use three buttons to set the time.

## The Mode Button

The first button is called the "mode" button.  It
will cycle through four internal "states" of our clock.
Here are the modes:

1. Mode 0: Clock Running - this is the normal mode of operation
2. Mode 1: Setting the Hour
3. Mode 2: Setting the Minute
4. Mode 3: Setting AM/PM

Here is a walkthrough of the ```button-mode-test.py``` program,
breaking it down into clear, digestible concepts for everyone new to MicroPython.

## Code Walkthrough

### 1. Basic Setup and Imports

```python
from mp_button import Button
from time import localtime, sleep
from machine import Pin
```

Let's understand what these lines do:
- These are import statements that bring in code we need to use
- `Button` is a special module that helps us work with physical buttons
- `localtime` and `sleep` are time-related functions
- `Pin` lets us work with the physical pins on our Raspberry Pi Pico

### 2. Setting Up the Pins

```python
mode_pin = Pin(16, Pin.IN, Pin.PULL_UP)
next_pin = Pin(17, Pin.IN, Pin.PULL_UP)
previous_pin = Pin(18, Pin.IN, Pin.PULL_UP)
```

Here's what's happening:
- We're setting up three different pins (16, 17, and 18) on the Pico
- Each pin is set as an input (`Pin.IN`) - meaning it receives signals rather than sends them
- `Pin.PULL_UP` means the pin is naturally "high" (1) until a button press makes it "low" (0)
- Think of it like a light switch that's normally on, and pressing the button turns it off

### 3. Global Variables

```python
counter_pressed = 0
counter_released = 0
mode = 0  # default clock running
mode_names = ["run","set hour","set minute","set AM/PM"]
mode_count = len(mode_names)
now = localtime()
hours = now[3]
minutes = now[4]
am_pm = 0
```

These are our program's variables:
- `counter_pressed` and `counter_released` keep track of button presses
- `mode` tells us which setting we're currently adjusting (starts at 0)
- `mode_names` is a list of the different modes our clock can be in
- `mode_count` is how many modes we have (4 in this case)
- `now` gets the current time from the Pico
- `hours` and `minutes` store the current time values
- `am_pm` keeps track of whether it's morning (0) or afternoon (1)

### 4. Button Handler Functions

```python
def button_mode_irq(button, event):
    global mode, hours, minutes
    if event == Button.PRESSED:
        mode += 1
        mode = mode % mode_count
        print('new mode:', mode, mode_names[mode])
```

This is our mode button handler:
- `global` tells Python we want to change variables outside this function
- When the button is pressed, we increase the mode by 1
- The `%` (modulo) operator helps us cycle back to 0 after reaching the last mode
- For example: if mode is 3 and we add 1, `4 % 4 = 0`, so we go back to the first mode

### 5. Next and Previous Button Handlers

```python
def button_next_irq(button, event):
    global mode, hours, minutes, am_pm
    if event == Button.PRESSED:
        if mode == 1:
            hours += 1
        if mode == 2:
            minutes += 1
        if mode == 3:
            am_pm = 1 if am_pm == 0 else 0
```

The next/previous buttons:
- They only work when we're in a setting mode (not mode 0)
- Mode 1: adjust hours
- Mode 2: adjust minutes
- Mode 3: toggle between AM and PM
- The previous button does the same thing but decreases values

### 6. Creating Button Objects

```python
button_mode = Button(16, False, button_mode_irq, internal_pullup = True, debounce_time = 100)
button_next = Button(17, False, button_next_irq, internal_pullup = True, debounce_time = 100)
button_previous = Button(18, False, button_previous_irq, internal_pullup = True, debounce_time = 100)
```

Here we create our button objects:
- Each button gets a pin number (16, 17, or 18)
- We tell it which function to call when pressed (the `_irq` functions)
- `debounce_time = 100` prevents multiple triggers from one press
- Think of debouncing like waiting a moment to make sure someone really pressed the button once

### 7. Main Loop

```python
while(True):
    button_mode.update()
    button_next.update()
    button_previous.update()
```

This is our main program loop:
- It runs forever (that's what `while True` means)
- Each time through the loop, we check if any buttons were pressed
- The `update()` function handles all the button checking for us

## Full Program Listing

```python
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
```

## The Decrement Time

The following line need some explanation:

```python
hour = ((hour - 2) % 12) + 1
```
Let me break down that line, which handles decrementing hours 
while staying within the 1-12 range:

Let's walk through it step by step:

1. First, we subtract 2 from the current hour: `(hour - 2)`
   - We subtract 2 (not 1) because we'll add 1 back at the end
   - This shift is necessary because we want to work with 0-11 for the modulo operation

2. Then we take modulo 12: `% 12`
   - This ensures our number wraps around within 0-11
   - For example, if hour was 1, then (1-2) = -1, and -1 % 12 = 11

3. Finally, we add 1: `+ 1`
   - This shifts our range from 0-11 back to 1-12

Here's an example sequence to show how it works:
- Starting at hour = 1:
  - (1 - 2) = -1
  - -1 % 12 = 11
  - 11 + 1 = 12
- Starting at hour = 12:
  - (12 - 2) = 10
  - 10 % 12 = 10
  - 10 + 1 = 11

This gives us the desired behavior of decrementing through the 
sequence: 12 → 11 → 10 → ... → 1 → 12

## Updating the Display

```python
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
# LED value 0 indicates AM, value 1 indicates PM
pm_pin = Pin(PM_PIN, Pin.OUT)

# Time state
now = localtime()
hour = now[3]
minute = now[4]
second = now[5]

tm = tm1637.TM1637(clk=Pin(CLK_PIN), dio=Pin(DST_PIN))

mode = 0
mode_names = ["run", "set hour", "set minute", "set AM/PM"]
mode_count = len(mode_names)

# Debounce state
last_mode_press = 0
last_next_press = 0
last_prev_press = 0
DEBOUNCE_MS = 100

def format_time():
    return f"{hour:d}:{minute:02d}:{second:02d} {'PM' if is_pm else 'AM'}"

def set_pm():
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
    
# Set up interrupts
mode_pin.irq(trigger=Pin.IRQ_FALLING, handler=handle_mode)
next_pin.irq(trigger=Pin.IRQ_FALLING, handler=handle_next)
previous_pin.irq(trigger=Pin.IRQ_FALLING, handler=handle_previous)

# Main loop
print("Clock started. Press mode button to change settings.")

while True:
    second = localtime()[5]
    if mode == 0:  # Only update display in run mode
        print(format_time())
        # flash the colon on and off every second
        if (second % 2): # modulo 2 will be true for odd numbers
            numbers_nlz(hour, minute, True)
        else:
            numbers_nlz(hour, minute, False)
        set_pm()
        sleep(1)

```