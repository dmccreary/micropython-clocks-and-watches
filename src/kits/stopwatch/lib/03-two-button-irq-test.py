from mp_button import Button
from machine import Pin
from utime import sleep, ticks_ms, ticks_diff

# lower right corner - button closes path to GND
STOPWATCH_START_STOP_PIN = 14
STOPWATCH_RESET_PIN = 15

# configure the pins
start_stop_pin = Pin(STOPWATCH_START_STOP_PIN, Pin.IN, Pin.PULL_UP)
reset_pin = Pin(STOPWATCH_RESET_PIN, Pin.IN, Pin.PULL_UP)

# we create two counters to cound presses down and released
# global variables
STOPPED = const(0)
RUNNING = const(1)
# set the initial state to be stopped
stopwatch_state = STOPPED
stopwatch_starttime = 0
stopwatch_resume_time = 0

# Debounce state
last_start_stop_press = 0
last_reset_press = 0
DEBOUNCE_MS = 250

def start_stop_irq(pin):
    global last_start_stop_press, stopwatch_state, stopwatch_starttime, stopwatch_resume_time
    current_time = ticks_ms()
    if ticks_diff(current_time, last_start_stop_press) > DEBOUNCE_MS:
        last_start_stop_press = current_time
        # toggle the running state
        if stopwatch_state == STOPPED:
            stopwatch_state = RUNNING
            stopwatch_starttime = ticks_ms()
        else:
            # collect the time since last
            stopwatch_resume_time += (ticks_ms() - stopwatch_starttime) + stopwatch_resume_time 
            stopwatch_state = STOPPED
        # print('start/stop pressed')

def reset_irq(pin):
    global last_reset_press, stopwatch_state, stopwatch_milliseconds, stopwatch_resume_time
    current_time = ticks_ms()
    if ticks_diff(current_time, last_reset_press) > DEBOUNCE_MS:
        last_reset_press = current_time
        stopwatch_state = STOPPED
        stopwatch_resume_time = 0
        # print('reset butto pressed')

# Here are the Interupt handlers
start_stop_pin.irq(trigger=Pin.IRQ_RISING, handler=start_stop_irq)
reset_pin.irq(trigger=Pin.IRQ_FALLING, handler=reset_irq)

# during our loop we keep checking the button(s)
counter = 0
while(True):
    counter += 1
    print("state:", stopwatch_state, stopwatch_resume_time//1000, ":", stopwatch_resume_time%1000)
    sleep(.5)