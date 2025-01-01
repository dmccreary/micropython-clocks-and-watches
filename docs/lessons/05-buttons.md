# Buttons

![Set buttons on breadboard](../img/set-buttons-on-breadboard.png)

Our standard watch kits places two or three buttons on the breadboard.
You can use these buttons to set the time.

The buttons are connected to the lower-left corner of the pico
using GPIO 14 and GPIO 15.

Instructions on how to use these buttons are covered in our
MicroPython class:

[Using Buttons in MicroPython](https://www.coderdojotc.org/micropython/basics/03-button/)

We suggest using the top blue button to change the mode of operation.  As you
press this you cycle through various modes of your clock or watch.  Here
are some sample modes for a clock:

1. Run mode
2. Set current time hour
3. Set current time minute
4. Set alarm hour
5. Set alarm minute

After you are in a given mode, the bottom button can be used to cycle through the options.
Remember to get the current value for the cycle for each mode.  So if you are
adjusting the hour you have to make sure the cycle value starts at the current hour.

## Sample Button Mode Code

```py
from utime import sleep, ticks_ms
from machine import Pin

# Sample Raspberry Pi Pico MicroPython button press example with a debounce delay value of 200ms in the interrupt handler

# Config
MODE_BUTTON_PIN = 14
CYCLE_BUTTON_PIN = 15
mode = 0 # the count of times the button has been pressed
cycle = 0
last_time = 0 # the last time we pressed the button

builtin_led = machine.Pin(25, Pin.OUT)
# The lower left corner of the Pico has a wire that goes through the buttons upper left and the lower right goes to the 3.3 rail
mode_pin = machine.Pin(MODE_BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
cycle_pin = machine.Pin(CYCLE_BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_UP)

# This function gets called every time the button is pressed.  The parameter "pin" is not used.
def button_pressed_handler(pin):
    global mode, cycle, last_time
    new_time = ticks_ms()
    # if it has been more that 1/5 of a second since the last event, we have a new event
    if (new_time - last_time) > 200:
        # this should be pin.id but it does not work
        if '14' in str(pin):
            mode +=1
        else:
            cycle +=1
        # last, we update the last time we got an ISR here
        last_time = new_time


# now we register the handler function when the button is pressed
mode_pin.irq(trigger=machine.Pin.IRQ_FALLING, handler = button_pressed_handler)
cycle_pin.irq(trigger=machine.Pin.IRQ_FALLING, handler = button_pressed_handler)

# This is for only printing when a new button press count value happens
old_mode = 0
old_cycle = 0 

while True:
    # only print on change in the button_presses value
    if mode != old_mode:
        print('New Mode:', mode)
        builtin_led.toggle()
        old_mode = mode
    if cycle != old_cycle:
        print('New Cycle:', cycle)
        builtin_led.toggle()
        old_cycle = cycle
    sleep(.1)
```

## Three Button Set

```python
from machine import Pin
import time

# Pin setup
mode_pin = Pin(16, Pin.IN, Pin.PULL_UP)
next_pin = Pin(17, Pin.IN, Pin.PULL_UP)
previous_pin = Pin(18, Pin.IN, Pin.PULL_UP)

# Time state
hour = 12
minute = 0
is_pm = False
mode = 0
mode_names = ["run", "set hour", "set minute", "set AM/PM"]
mode_count = len(mode_names)

# Debounce state
last_mode_press = 0
last_next_press = 0
last_prev_press = 0
DEBOUNCE_MS = 200

def format_time():
    return f"{hour:02d}:{minute:02d} {'PM' if is_pm else 'AM'}"

def handle_mode(pin):
    global mode, last_mode_press
    current_time = time.ticks_ms()
    if time.ticks_diff(current_time, last_mode_press) > DEBOUNCE_MS:
        mode = (mode + 1) % mode_count
        print(f"Mode: {mode_names[mode]}")
        last_mode_press = current_time

def handle_next(pin):
    global hour, minute, is_pm, last_next_press
    current_time = time.ticks_ms()
    if time.ticks_diff(current_time, last_next_press) > DEBOUNCE_MS:
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
    current_time = time.ticks_ms()
    if time.ticks_diff(current_time, last_prev_press) > DEBOUNCE_MS:
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
        time.sleep(1)
```
