from mp_button import Button
from machine import Pin

# lower right corner - button closes path to GND
STOPWATCH_START_STOP_PIN = 14
STOPWATCH_RESET_PIN = 15

# we create two counters to cound presses down and released
counter_pressed = 0
counter_released = 0

# the following function will be invoked
# when the button changes state
# the Button module expects a callback to handle 
# - pin number
# - event (Button.PRESSED | Button.RELEASED)
# the event contains a string 'pressed' or 'released'
# which can be used in your code to act upon
def button_change(button, event):
    global counter_pressed, counter_released
    print(f'button {button} has been {event}')
    if event == Button.PRESSED:
        counter_pressed += 1
    if event == Button.RELEASED:
        counter_released += 1
    print(f'pressed {counter_pressed} times')
    print(f'released {counter_released} times')


# we define a variable which holds a Button
# this Button object will be created using:
# - a pin number (GPIOx)
# - the state at rest (value() is False by default)
# - a callback to invoke when the button changes state (see above)
button_one = Button(STOPWATCH_START_STOP_PIN, False, button_change, internal_pullup = True)
button_two = Button(STOPWATCH_RESET_PIN, False, button_change, internal_pullup = True)

# during our loop we keep checking the button(s)
while(True):
    button_one.update()
    button_two.update()