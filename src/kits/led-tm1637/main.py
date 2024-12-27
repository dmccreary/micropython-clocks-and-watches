# display hours and minutes on the TM1637 LED display
# make the colon go on and off every second
import tm1637
from machine import Pin
from utime import sleep, localtime
tm = tm1637.TM1637(clk=Pin(0), dio=Pin(1))
 
def numbers_nlz(num1, num2, colon=True):
    """Display two numeric values -9 through 99, with a leading space before
    single-digit first numbers and separated by a colon."""
    num1 = max(-9, min(num1, 99))
    num2 = max(-9, min(num2, 99))
    prefix = ' ' if num1 < 10 else ''
    print(f'"{prefix}{num1:d}{num2:0>2d}"')
    segments = tm.encode_string(f'{prefix}{num1:d}{num2:0>2d}')
    if colon:
        segments[1] |= 0x80  # colon on
    tm.write(segments)

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
        numbers_nlz(hours, minutes, True)
    else:
        numbers_nlz(hours, minutes, False)
    sleep(1)