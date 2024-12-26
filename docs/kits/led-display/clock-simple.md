# Simple Clock

Here is a simple clock program that will display the hours and minutes
from the localtime() function.  It will also turn the colon LEDs
on and off every second using the ```modulo``` function to
test for the even/odd property of the second.

## The Localtime function

```python
# display hours and minutes on the TM1637 LED display
# make the colon go on and off every second
import tm1637
from machine import Pin
from utime import sleep, localtime
tm = tm1637.TM1637(clk=Pin(0), dio=Pin(1))

counter = 0
while True:
    now = localtime() # returns 8 inits for date and time
    hours = now[3]
    minutes = now[4]
    seconds = now[5]
    print(hours, ":", minutes, ' ', seconds)
    # flash the colon on and off every second
    if (seconds % 2): # modulo 2 will be true for odd numbers
        tm.numbers(hours, minutes, True)
    else:
        tm.numbers(hours, minutes, False)
    sleep(1)
```

