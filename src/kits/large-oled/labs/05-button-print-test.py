from utime import sleep
from machine import Pin

# Sample Raspberry Pi Pico MicroPython button press example with a debounce delay value of 200ms in the interrupt handler

# Buttons
BUTTON_1_PIN = 13

button_1_pin = Pin(BUTTON_1_PIN, Pin.IN, Pin.PULL_UP)

# This function gets called every time the button is pressed.  The parameter "pin" is not used.
def button_1_pressed(pin):
    print('Button 1 pressed')

# now we register the button handler function using the irq setter method for this pin
button_1_pin.irq(trigger=Pin.IRQ_FALLING, handler = button_1_pressed)

while True:
    sleep(1)