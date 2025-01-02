# Real Time Clocks

!!! note
    Real-time clock support has only recently been added to the core MicroPython libraries.
    Make sure you are using the latest release of MicroPython to use the features
    built into the MicroPython Runtime.

    See [The MicroPython RTC Documentation](https://docs.micropython.org/en/latest/library/machine.RTC.html) to make sure you have the right release.

## The DS1307 and the DS3231

Our lessons use two different RTC chips.  Let's do a comparison of these RTC modules and explain their implementation with the MicroPython.

### DS1307
![](../img/rtc-ds1307-front-back.jpg)

This is the original battery-backed real-time clock with I2C interface that maintains basic timekeeping functions introduced by Maxim (then Dallas Semiconductor) around 2004-2005.
For example, the DS1307 can be used for tracking hours, minutes, seconds with ±2 seconds/day accuracy at C 77°F (25°).
This is appropriate for room temperature household clocks that have a uniform temperature.  Large
swings in temperature change crystal vibration frequency which can impact clock accuracy.

### DS3231

![](../img/rtc-ds3231-front-back.jpg)

This is a newer temperature-compensated real-time clock Released by Maxim Integrated around 2009-2010.
With integrated crystal and I2C interface that maintains highly accurate timekeeping under varying conditions.

The DS3231 represented a significant advancement in accuracy and temperature compensation over the earlier DS1307. The improved technology helped make the DS3231 the preferred choice for precision timekeeping applications, despite its higher cost. The DS3231m typically maintains an accuracy of ±2 seconds each **month** (not day) across an incredible range of  -40°F to 185°F (-40°C to +85°C).
The DS3231 also has an on-board register you can access to get the current temperature
of the device.

Key Technical and Financial Differences:

1. Accuracy:
- DS1307: ±2 seconds/day
- DS3231: ±2 seconds/month due to temperature compensation

2. Temperature Operation:
- DS1307: 32°F to 158°F (0°C to +70°C)
- DS3231: -40°F to 185°F (-40°C to +85°C) with compensation

3. Clock Output:
- DS1307: Programmable square wave (1Hz, 4kHz, 8kHz, 32kHz)
- DS3231: 32kHz output plus programmable square wave

4. Based on typical retail prices as of 2024:
- DS1307: $1-2 USD
- DS3231: $3-5 USD

## Implementation with MicroPython

The coding for each of these chips in almost identical since they implement the same I2C interface.

```python
from machine import I2C, Pin

# Both modules use same I2C interface setup
i2c = I2C(0, sda=Pin(0), scl=Pin(1))

# DS1307 implementation
DS1307_ADDR = 0x68
def ds1307_get_time():
    return i2c.readfrom_mem(DS1307_ADDR, 0x00, 7)

# DS3231 implementation
DS3231_ADDR = 0x68
def ds3231_get_time():
    return i2c.readfrom_mem(DS3231_ADDR, 0x00, 7)
    
# Both modules store time in BCD format
def decode_bcd(bcd):
    return (bcd & 0xF) + ((bcd >> 4) * 10)
```

The code structure remains similar for both modules since they share the I2C interface and address. The DS3231 provides additional registers for temperature data and aging offset, which can be accessed for more precise timekeeping.

For classroom use, the DS3231 is recommended due to its superior accuracy and temperature compensation, though it typically costs more than the DS1307.

## Detecting the RTC Type

Both the DS1307 and the DS3231 appear at exactly the same address `0x68`.  So
how can you tell which device you have?  The answer is that the DS3231
has additional status, control and temperature registers we can look
for.  If it has these values we know it is the good stuff!

```python
from machine import I2C, Pin
import time

# I2C setup
i2c = I2C(0, sda=Pin(0), scl=Pin(1))

# Device addresses
RTC_ADDR = 0x68  # Both DS1307 and DS3231 use 0x68

def identify_rtc():
    """
    Identify whether the RTC is a DS1307 or DS3231
    Returns: String identifying the RTC type
    """
    try:
        # Try to read the status register (0x0F) - only exists on DS3231
        i2c.writeto(RTC_ADDR, b'\x0F')
        status = i2c.readfrom(RTC_ADDR, 1)[0]
        
        # Try to read control register (0x0E) - only exists on DS3231
        i2c.writeto(RTC_ADDR, b'\x0E')
        control = i2c.readfrom(RTC_ADDR, 1)[0]
        
        # If we got here, it's almost certainly a DS3231
        # Try reading temperature registers as final confirmation
        i2c.writeto(RTC_ADDR, b'\x11')
        temp_data = i2c.readfrom(RTC_ADDR, 2)
        
        return "DS3231 (Temperature-compensated RTC)"
        
    except Exception as e:
        # If we couldn't read those registers, it's probably a DS1307
        # Let's verify by trying to read the control register (0x07) of DS1307
        try:
            i2c.writeto(RTC_ADDR, b'\x07')
            control = i2c.readfrom(RTC_ADDR, 1)[0]
            return "DS1307 (Basic RTC)"
        except:
            return "Unknown RTC device"

def main():
    print("\nRTC Model Identifier")
    print("-" * 40)
    
    # First check if any device is present at RTC address
    devices = i2c.scan()
    if RTC_ADDR not in devices:
        print(f"No RTC found at address 0x{RTC_ADDR:02X}")
        return
        
    # Identify the RTC
    rtc_type = identify_rtc()
    print(f"Found: {rtc_type}")
    
    if "DS3231" in rtc_type:
        # Read temperature for DS3231
        i2c.writeto(RTC_ADDR, b'\x11')
        temp_data = i2c.readfrom(RTC_ADDR, 2)
        temp_msb = temp_data[0]
        temp_lsb = (temp_data[1] >> 6) * 25  # 0.25°C precision
        temp_c = temp_msb + (temp_lsb / 100.0)
        temp_f = (temp_c * 9/5) + 32
        print(f"Temperature: {temp_c:.2f}°C ({temp_f:.2f}°F)")

if __name__ == "__main__":
    main()
```

## RTCs and EEPROM

Some RTCs also include a small 4K EEPROM to store information such
as what time zone you are in and what the clock skew was for
the last period.  If your i2c scanner shows something
at digital 80 (0x50) when you add your RTC, this is your EEPROM.

The device at 80 (0x50) is almost certainly an AT24C32 EEPROM (Electrically Erasable Programmable Read-Only Memory). It's commonly included on DS3231 RTC modules to provide non-volatile storage. This EEPROM can store about 4KB of data and is often used to store configuration settings.

You can get a dump of its contents by doing the following detection code:

```python
from machine import I2C, Pin
import time

# I2C setup
i2c = I2C(0, sda=Pin(0), scl=Pin(1))

# Device addresses
DS3231_ADDR = 0x68  # 104 decimal
EEPROM_ADDR = 0x50  # 80 decimal

def read_ds3231_temp():
    """Read temperature from DS3231"""
    try:
        # First ensure we're reading fresh temperature data
        # Write to the control register (0x0E) to force a temperature conversion
        i2c.writeto(DS3231_ADDR, b'\x0E\x20')  # Set CONV bit
        time.sleep(0.2)  # Wait for conversion
        
        # Now read temperature registers (0x11 and 0x12)
        i2c.writeto(DS3231_ADDR, b'\x11')
        temp_data = i2c.readfrom(DS3231_ADDR, 2)
        
        # MSB is the integer part
        temp_msb = temp_data[0]
        
        # LSB holds two bits for decimal part
        temp_lsb = (temp_data[1] >> 6) * 25  # Convert to decimal (0.25°C precision)
        
        # Handle negative temperatures (2's complement)
        if temp_msb & 0x80:
            temp_msb = -(~(temp_msb - 1) & 0xFF)
            
        temp_c = temp_msb + (temp_lsb / 100.0)  # Combine integer and decimal parts
        temp_f = (temp_c * 9/5) + 32
        
        return temp_c, temp_f
    except Exception as e:
        return f"Error reading temperature: {str(e)}"

def read_ds3231_time():
    """Read current time from DS3231"""
    try:
        # Start reading from register 0x00
        i2c.writeto(DS3231_ADDR, b'\x00')
        data = i2c.readfrom(DS3231_ADDR, 7)
        
        # Convert BCD to decimal
        def bcd2dec(bcd):
            return (bcd & 0x0F) + ((bcd >> 4) * 10)
        
        second = bcd2dec(data[0])
        minute = bcd2dec(data[1])
        hour = bcd2dec(data[2])
        day = bcd2dec(data[4])
        month = bcd2dec(data[5] & 0x1F)
        year = bcd2dec(data[6]) + 2000
        
        return f"{year:04d}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:{second:02d}"
    except Exception as e:
        return f"Error reading time: {str(e)}"

def read_eeprom(start_addr=0, length=32):
    """Read data from EEPROM"""
    try:
        # Create buffer for address
        addr_buf = bytearray(2)
        addr_buf[0] = (start_addr >> 8) & 0xFF  # High byte
        addr_buf[1] = start_addr & 0xFF         # Low byte
        
        # Write address to EEPROM
        i2c.writeto(EEPROM_ADDR, addr_buf)
        
        # Read data
        data = i2c.readfrom(EEPROM_ADDR, length)
        return data
    except Exception as e:
        return f"Error reading EEPROM: {str(e)}"

def main():
    """Main program to read and display device information"""
    print("\nI2C Device Information Reader")
    print("-" * 40)
    
    # Scan for devices
    devices = i2c.scan()
    print(f"Found devices at addresses: {[hex(x) for x in devices]}")
    print("-" * 40)
    
    # Read and display DS3231 information
    # Note that the DS1307 does not have any temperature registers
    if DS3231_ADDR in devices:
        print("DS3231 RTC Information:")
        print(f"Current Time: {read_ds3231_time()}")
        temp_c, temp_f = read_ds3231_temp()
        print(f"Temperature: {temp_c:.2f}°C ({temp_f:.2f}°F)")
    else:
        print("DS3231 not found!")
    
    print("-" * 40)
    
    # Read and display EEPROM contents
    if EEPROM_ADDR in devices:
        print("AT24C32 EEPROM Contents (first 32 bytes):")
        eeprom_data = read_eeprom(0, 32)
        
        # Display as hex
        print("Hex dump:")
        for i in range(0, len(eeprom_data), 16):
            chunk = eeprom_data[i:i+16]
            hex_values = ' '.join([f'{x:02X}' for x in chunk])
            ascii_values = ''.join([chr(x) if 32 <= x <= 126 else '.' for x in chunk])
            print(f"{i:04X}: {hex_values:<48} {ascii_values}")
        
        # Try to interpret as ASCII
        print("\nASCII interpretation (if printable):")
        ascii_text = ''.join([chr(x) if 32 <= x <= 126 else '.' for x in eeprom_data])
        print(ascii_text)
    else:
        print("EEPROM not found!")

if __name__ == "__main__":
    main()
```

### Results of Scan on RTM with EEPROM

```
AT24C32 EEPROM Contents (first 32 bytes):
Hex dump:
0000: FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF  ................
0010: FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF  ................
ASCII interpretation (if printable):
................................
```

### Dump EEPROM Address

The AT24C32/AT24C64 EEPROM typically is located at 87 (0x57).

Here is a script to dump this memory.

```python
import time

# I2C setup
i2c = I2C(0, sda=Pin(0), scl=Pin(1))

# Device addresses
RTC_ADDR = 0x68  # Both DS1307 and DS3231 use 0x68
# EEPROM address
EEPROM_ADDR = 0x57

def dump_eeprom():
   # Read first 100 bytes in chunks of 8
   for addr in range(0, 100, 8):
       data = i2c.readfrom_mem(EEPROM_ADDR, addr, 8)
       print(f"0x{addr:02x}:", " ".join([f"{x:02x}" for x in data]))
       time.sleep(0.1)  # Small delay between reads

dump_eeprom()
```

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

[Insert image of a DS3231 chip]

Now, let's move on to the newer and more accurate DS3231. Released in 2011, the DS3231 is known for its incredible precision. It has a temperature-compensated crystal oscillator (TCXO), which means it can maintain accurate timekeeping even when the temperature changes. This is important because temperature fluctuations can affect the frequency of regular crystal oscillators, causing the clock to drift over time.

[Insert image comparing the accuracy of DS1307 and DS3231]

How accurate is the DS3231, you might ask? Well, it has a typical accuracy of ±2 parts per million (ppm), which translates to a drift of about 1 minute per year! In comparison, the DS1307 has an accuracy of around ±20 ppm, which means it can drift by about 10 minutes per year. That's a significant difference!

[Insert image of I2C communication]

Just like the DS1307, the DS3231 communicates with the main processor using the I2C protocol. It has a simple register-based interface that allows you to read and set the time easily.

Now, let's talk about some fun applications of RTCs. One cool project you can build is a digital clock that always displays the correct time, even if it's been unplugged for a while. You can also create a data logger that records temperature, humidity, or other sensor readings along with precise timestamps. The possibilities are endless!

[Insert image of a digital clock or a data logger project]

In our hands-on lab today, we'll be working with both the DS1307 and the DS3231. You'll learn how to wire them up, set the time, and read the current time using a microcontroller. We'll also explore some practical examples and discuss how to choose the right RTC for your projects.

[Insert image of students working on a project]

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