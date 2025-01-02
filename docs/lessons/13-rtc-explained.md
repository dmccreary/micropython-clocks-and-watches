## Explaining RTC to Students

!!! prompt
    You are a friendly and fun science teacher working with a group of high-school 
    students taking a course called "Programming Clocks and Watches".  Today your 
    lecture is on "Real time Clocks" like the old DS1307 and the newer super 
    accurate DS3231.  Give the full text of a 15-minute lecture before the 
    hands-on lab and mention where images should be inserted.

Hello everyone, and welcome to today's exciting lecture on Real Time Clocks! 
In our "Programming Clocks and Watches" course, we're going to dive into 
the fascinating world of the good old DS1307 used in our classrooms
and the new super accurate DS3231.

First, let's talk about what a Real Time Clock (RTC) is. 
An RTC is a computer chip that keeps track of the current time, 
even when the main power is off. It's like a tiny, dedicated clock 
inside your electronic devices. RTCs are found in computers, 
smartphones, appliances, and many other gadgets that need to keep accurate time.

Here is how the DS1307 is typically used in a microcontroller project.

![](../img/rtc-ds1307-circuit-diagram.png)

The DS1307 is one of the most well-known RTCs.  We have a LOT of them lying around the lab.
This little chip was first introduced in 2005 and has been widely used in various electronic projects. The DS1307 keeps track of seconds, minutes, hours, days, months, and years. It communicates with the main processor using a protocol called I2C (Inter-Integrated Circuit).

Now, let's take a look at how the DS1307 works. It has a built-in crystal oscillator that vibrates at a specific frequency, acting as a precise clock source. The chip counts these oscillations to keep track of time. The DS1307 also has a small amount of battery-backed memory, allowing it to maintain the time even when the main power is off.

Speaking of power, the DS1307 uses a small coin cell battery to keep the clock running when the main power is disconnected. This battery can last for several years, ensuring that your device always has the correct time.

![](../img/rtc-ds3231-front-back.jpg)

Now, let's move on to the newer and more accurate DS3231. Released in 2011, the DS3231 is known for its incredible precision. It has a temperature-compensated crystal oscillator (TCXO), which means it can maintain accurate timekeeping even when the temperature changes. This is important because temperature fluctuations can affect the frequency of regular crystal oscillators, causing the clock to drift over time.

| Device | Strength | Accuracy (PPM) | Seconds Drift Per Month | Price |
| --- |  --- |  --- |  --- |  --- |
| DS1307 | Low Cost | ±20 | ±52 | $1 |
| DS3231 | Accuracy | ±2 | ±5 | $3 |


The DS1307 uses a standard crystal oscillator while the DS3231 uses a temperature-compensated crystal oscillator (TCXO), explaining the accuracy difference.
How accurate is the DS3231, you might ask? Well, it has a typical accuracy of ±2 parts per million (ppm), which translates to a drift of about 1 minute per year! In comparison, the DS1307 has an accuracy of around ±20 ppm, which means it can drift by about 10 minutes per year. That's a significant difference!

[Insert image of I2C communication]

Just like the DS1307, the DS3231 communicates with the main processor using the I2C protocol. It has a simple register-based interface that allows you to read and set the time easily.

Now, let's talk about some fun applications of RTCs. One cool project you can build is a digital clock that always displays the correct time, even if it's been unplugged for a while. You can also create a data logger that records temperature, humidity, or other sensor readings along with precise timestamps. The possibilities are endless!

In our hands-on lab today, we'll be working with both the DS1307 and the DS3231. You'll learn how to wire them up, set the time, and read the current time using a microcontroller. We'll also explore some practical examples and discuss how to choose the right RTC for your projects.

So, get ready to have some fun with Real Time Clocks! Remember, whether you're building a simple clock or a complex data logging system, an RTC is an essential component that keeps everything running on time.

Let's head to the lab and start tinkering with these amazing little chips!

## Testing the DS1307 and DS3232 Real Time Clocks

![RTC DS3231 Listing on eBay](../img/rtc-ds3231-ebay.png)

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

In our example, `time()` returned 1735332067. This timestamp corresponds to 
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

## Accuracy of the Clock on the Raspberry Pi Pico**

The Raspberry Pi Pico does not have a real-time clock (RTC) built into its hardware. Its clock is derived from the internal oscillator, which may be subject to drift and is not highly accurate for long-term timekeeping. The accuracy depends on the quality of the oscillator and the environmental conditions, such as temperature.

- **Drift**: The internal clock is typically accurate to within **1%** under normal conditions.

- **Seconds off per day**: For a 1% drift:

$$
1\% \text{ of 24 hours} = 0.01 \times 24 \times 3600 \approx 864 \, \text{seconds off per day}.
$$

Thus, the clock on the Pico can drift up to **±864 seconds per day** without correction.

For improved accuracy, you can add an external RTC module to the Pico.

Accuracy of the Clock on the DS1307

The DS1307 is a low-cost RTC chip widely used in electronics projects. Its accuracy is based on an external 32.768 kHz quartz crystal oscillator, which is sensitive to factors like temperature and crystal quality.
	•	Drift: The DS1307 typically drifts by ±20 ppm (parts per million) at 25°C.
	•	Seconds off per day: With a drift of 20 ppm:

$$
20 \, \text{ppm} \times 24 \times 3600 \, \text{seconds} = 1.728 \, \text{seconds off per day}.
$$

The DS1307 clock may be off by approximately ±1.7 seconds per day under ideal conditions.

For more accurate timekeeping, consider using a higher-quality RTC like the DS3231, which has a drift of ±2 ppm (about ±0.17 seconds per day) due to its temperature compensation feature.

## References

* [DS1307 Data Sheet](https://www.analog.com/media/en/technical-documentation/data-sheets/ds1307.pdf)
* [Reference Manual](https://micropython-ds1307.readthedocs.io/en/latest/)