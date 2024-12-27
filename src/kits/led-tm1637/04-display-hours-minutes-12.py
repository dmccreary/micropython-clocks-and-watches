# display hours and minutes on the TM1637 LED display
# make the colon go on and off every second
import tm1637
from machine import Pin
from utime import sleep, localtime
tm = tm1637.TM1637(clk=Pin(0), dio=Pin(1))

while True:
    now = localtime() # returns 8 inits for date and time
    hours = now[3]
    if hours > 12:
        hours = hours - 12
    minutes = now[4]
    seconds = now[5]
    print(hours, ":", minutes, ' ', seconds)
    # flash the colon on and off every second
    if (seconds % 2):
        tm.numbers(hours, minutes, True)
    else:
        tm.numbers(hours, minutes, False)
    sleep(1)