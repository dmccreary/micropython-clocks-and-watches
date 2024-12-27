# A Simple Clock with the TM1637 LED Display

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

That is it!  Pretty cool that you can write an entire clock program
in that few lines of code.  But it is not perfect.  Let's
find some ways to make the clock work a little better.

Note that the hours is always in 24 hour time.  If you want to 
use 12 hour time you will need to subtract 12 from the hours if
the hours is greater than 12.

We can add the following lines of code to make the display better
for people that use a 12-hour clock.

```python
if hours > 12:
    hours = now[3]
    hours = hours - 12
```

This will work, but it has the disadvantage of displaying the leading zero
before the ones digit.  Unfortunately, this is the way that the ```numbers()``` function
was written in the TM1637 module.  Let's take a look at how we can clean this up a bit.

## Removing Leading Zeros

In order to fix the leading zeros problem in the hours place, we
need to write our own version of the ```numbers()``` function
that changes '0' to be a space (all 7 segments off) if the hours
is less than 10.

Here is the original ```numbers()``` function taken directly from the driver:
```python
def numbers(self, num1, num2, colon=True):
    """Display two numeric values -9 through 99, with leading zeros
    and separated by a colon."""
    num1 = max(-9, min(num1, 99))
    num2 = max(-9, min(num2, 99))
    segments = self.encode_string('{0:0>2d}{1:0>2d}'.format(num1, num2))
    if colon:
        segments[1] |= 0x80 # colon on
    self.write(segments)
```

You can see that the author used the Python .format function to
display the first number using a leading zero.  This is fine
for our minutes, but not a standard for the hours.

We will need to modify this code to put in a space character in if the hours is
less than 10 and to only display the hours number without a leading
zero.  The format ```{0:0>2d}``` will be changed to be: ```{prefix}{num1:d}```
where:

```python
prefix = ' ' if num1 < 10 else ''
```

```python
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
```

Now the display will work as most normal digital clocks.

So as long as the localtime() function is working, this
clock should work fine.  An as long as your device is connected
to your computer via an USB cable it will be fine.

What if you would like your clock to work without being connected
to a computer.  We have two options:

1. Used a Raspberry Pi Pico W to get time from a central time service over Wifi
2. or use a local clock and set the time manually
