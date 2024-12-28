# Testing the DS1307 Real Time Clock

## Hardware Configuration

### DS1307 Connections
1. CLK - clock
2. DST - Data (incoming to Pico)
3. RST - Reset
4. VCC - must be 5 volts, not 3.2
5. GND - ground

We will use the lower right pins on the Pico so that the display can use the pins in the upper-right corner.

These pin assignments are

1. GP16 - far lower right - CLK
2. GP17 - second from the bottom - DST
3. GP18 - fourth pin up - RST

Contents of config.py

```python
CLK_PIN = 16
DST_PIN = 17
RST_PIN = 18
```

## Sample DS1307 MicroPython Test Program for the Raspberry Pi Pico

```python
from machine import I2C, Pin
import config

CLK_PIN = config.CLK_PIN
DST_PIN = config.DST_PIN
DS_PIN = config.DS_PIN

print("Clock on pin:", CLK_PIN)
print("Data on pin:", DST_PIN)
print("Data Select on pin:", DS_PIN)

i2c = I2C(0, scl=Pin(CLK_PIN), sda=Pin(DST_PIN), freq=100000)
scan_result = i2c.scan()
print("I2C addresses found:", [hex(device_address) for device_address in scan_result])

if 104 in scan_result:
    print("PASS: DS1307 FOUND")
else:
    print("FAIL: DS1307 NOT FOUND")
```

### Sample Test Result

```
Clock on pin: 17
Data on pin: 16
Data Select on pin: 18
I2C addresses found: ['0x50', '0x68']
PASS: DS1307 FOUND
```

## Full Test of DS1307

```python
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""I2C DS1307 showcase"""

from ds1307 import DS1307
from machine import I2C, Pin
from utime import gmtime, sleep, time
import config
CLK_PIN = config.CLK_PIN
DST_PIN = config.DST_PIN
DS_PIN = config.DS_PIN

# DS1307 on 0x68
I2C_ADDR = 0x68     # DEC 104, HEX 0x68

# define custom I2C interface, default is 'I2C(0)'
# check the docs of your device for further details and pin infos
# this are the pins for the Raspberry Pi Pico adapter board
i2c = I2C(0, scl=Pin(CLK_PIN), sda=Pin(DST_PIN), freq=800000)
print(i2c.scan())
ds1307 = DS1307(addr=I2C_ADDR, i2c=i2c)

# get LCD infos/properties
print("DS1307 is on I2C address 0x{0:02x}".format(ds1307.addr))
print("Weekday start is {}".format(ds1307.weekday_start))

# get the current RTC time
print("Current RTC time: {}".format(ds1307.datetime))

# set the RTC time to the current system time
now = gmtime(time())
ds1307.datetime = now

# Print the date and time in ISO8601 format: 2023-04-18T21:14:22
print("Today is {:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}".format(
    ds1307.year, ds1307.month, ds1307.day,
    ds1307.hour, ds1307.minute, ds1307.second))

# check whether this year is a leap year
print("Is this year a leap year? {}".format(ds1307.is_leap_year(ds1307.year)))

# get the day of the year
print("Today is day {} of {}".format(
    ds1307.day_of_year(year=ds1307.year, month=ds1307.month, day=ds1307.day),
    ds1307.year))

# halt the oscillator
print("The oscillator is currently active at {}? {}".format(
    ds1307.datetime, ds1307.halt))
print("Halt the oscillator and wait for 5 seconds ...")
ds1307.halt = True
sleep(5)

print("Current RTC time: {}".format(ds1307.datetime))

print("Enable the oscillator and wait for 5 seconds ...")
ds1307.halt = False
sleep(5)
print("Current RTC time: {}".format(ds1307.datetime))

# control the squarewave pin SQ
print("Set square wave output to 1Hz and wait for 5 seconds ...")
ds1307.square_wave(sqw=1)
sleep(5)

print("Set square wave output to 4.096kHz and wait for 5 seconds ...")
ds1307.square_wave(sqw=4)
sleep(5)

print("Set square wave output to 8.192kHz and wait for 5 seconds ...")
ds1307.square_wave(sqw=8)
sleep(5)

print("Set square wave output to HIGH and wait for 5 seconds ...")
ds1307.square_wave(out=1)
sleep(5)

print("Set square wave output to LOW and wait for 5 seconds ...")
ds1307.square_wave(sqw=0)
sleep(5)
```

### Test Result

```
[80, 104]
DS1307 is on I2C address 0x68
Weekday start is 0
Current RTC time: (2024, 12, 27, 20, 29, 47, 4, 362)
Today is 2024-12-27T20:29:51
Is this year a leap year? True
Today is day 362 of 2024
The oscillator is currently active at (2024, 12, 27, 20, 29, 51, 4, 362)? False
Halt the oscillator and wait for 5 seconds ...
Current RTC time: (2024, 12, 27, 20, 29, 51, 4, 362)
Enable the oscillator and wait for 5 seconds ...
Current RTC time: (2024, 12, 27, 20, 29, 56, 4, 362)
Set square wave output to 1Hz and wait for 5 seconds ...
Set square wave output to 4.096kHz and wait for 5 seconds ...
Set square wave output to 8.192kHz and wait for 5 seconds ...
Set square wave output to HIGH and wait for 5 seconds ...
Set square wave output to LOW and wait for 5 seconds ...
```

### Localtime and gmtime(time())

```python
from utime import gmtime, time, localtime
print("time()", time())
print("   localtime()", localtime())
print("gmtime(time())", gmtime(time()))
```

Result

```
time() 1735332067
   localtime() (2024, 12, 27, 20, 41, 7, 4, 362)
gmtime(time()) (2024, 12, 27, 20, 41, 7, 4, 362)
```
This code is running on MicroPython on the Raspberry Pi Pico (RP2040)
and demonstrates the usage of time-related functions from the `utime` module. 

Let's break it down:

1.  `from utime import gmtime, time, localtime`: This line imports the `gmtime`, `time`, 
and `localtime` functions from the `utime` module, which is MicroPython's equivalent of 
the `time` module in standard Python.
2.  `print("time()", time())`: This line prints the label "time()" followed by the result
of calling the `time()` function. The `time()` function returns the number of seconds elapsed
since the Unix epoch (January 1, 1970, 00:00:00 UTC) as an integer value. In your output,
`time()` returned 1735332067, which represents the current timestamp.
3.  `print("   localtime()", localtime())`: This line prints the label "localtime()" 
followed by the result of calling the `localtime()` function. The `localtime()` 
function takes no arguments and returns a tuple representing the current local time. 
The tuple contains the following elements in order: (year, month, day, hour, minute, 
second, weekday, yearday). In your output, `localtime()` returned
`(2024, 12, 27, 20, 41, 7, 4, 362)`, indicating the current local time on the Raspberry Pi Pico.
4.  `print("gmtime(time())", gmtime(time()))`: This line prints the label
"gmtime(time())" followed by the result of calling the `gmtime()` function with 
the current timestamp obtained from `time()`. The `gmtime()` function takes a 
timestamp as an argument and returns a tuple representing the corresponding UTC time. 
The tuple has the same format as the one returned by `localtime()`. In your output, 
`gmtime(time())` returned `(2024, 12, 27, 20, 41, 7, 4, 362)`, which represents the current UTC time.

What does the number that `time()` returns represent?

The number returned by `time()` represents the number of seconds 
that have elapsed since the Unix epoch (January 1, 1970, 00:00:00 UTC). 
This value is commonly known as the Unix timestamp or epoch time. 
It is a widely used standard for representing points in time and is 
independent of time zones.

In your output, `time()` returned 1735332067. This timestamp corresponds to 
the date and time shown in the `localtime()` and `gmtime(time())` outputs,
which is December 27, 2024, at 20:41:07 UTC.

The Unix timestamp is a useful representation of time because it allows for 
easy arithmetic operations on timestamps and can be converted to human-readable
formats using functions like `localtime()` and `gmtime()`. It is widely used in 
various programming languages and systems for time-related operations.

It's important to note that the accuracy and synchronization of the time on the 
Raspberry Pi Pico depend on its internal clock and any time synchronization 
mechanisms used. Without external time synchronization, the Pico's internal 
clock may drift over time, resulting in slight inaccuracies compared to the actual current time.

## References

* [DS1307 Data Sheet](https://www.analog.com/media/en/technical-documentation/data-sheets/ds1307.pdf)
* [Reference Manual](https://micropython-ds1307.readthedocs.io/en/latest/)