# Buttons

Our standard watch kit places two buttons on the breadboard.
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
ifrom utime import sleep, ticks_ms
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

