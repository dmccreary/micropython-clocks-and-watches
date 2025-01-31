# Set RTC form the localtime

When you plug your Pico into your PC and use the Thonny IDE, the MicroPython runtime will startup and get the time from your desktop or laptop computer's clock and set the MicroPython runtimes localtime() with this time.

!!! Note
    You can disable the Thonny localtime if you want to test the RTC functions.

## Setting The RTC using the DS3231

This is a full raw way to set the DS3231 RTC from the MicroPython localtime.
You should only need to run this program when you first connect your RTC chip.
After you run it the clock should be accurate within 2-seconds per month.
In many cases when the clock is at room temperature the accuracy will be higher.

```python
from machine import Pin, I2C
from utime import localtime

# Constants
DS3231_ADDR = 0x68
STATUS_REG = 0x0F  # Status register address

# I2C setup
sda = Pin(0)
scl = Pin(1)
i2c = I2C(0, scl=scl, sda=sda, freq=100000)

def dec2bcd(dec):
    """Convert decimal to binary coded decimal."""
    return (dec // 10) << 4 | (dec % 10)

def check_osf():
    """Check the oscillator stop flag."""
    status = i2c.readfrom_mem(DS3231_ADDR, STATUS_REG, 1)[0]
    return bool(status >> 7)

def reset_osf():
    """Clear the oscillator stop flag."""
    status = bytearray(1)
    i2c.readfrom_mem_into(DS3231_ADDR, STATUS_REG, status)
    i2c.writeto_mem(DS3231_ADDR, STATUS_REG, bytearray([status[0] & 0x7f]))

def set_ds3231():
    """Set the DS3231 RTC time and ensure oscillator is running."""
    now = localtime()
    year = now[0] % 100  # Convert to 2-digit year
    month = now[1]
    day = now[2]
    hour = now[3]
    minute = now[4]
    second = now[5]
    
    # First check if oscillator is stopped
    if check_osf():
        print("Oscillator was stopped. Resetting OSF flag...")
        reset_osf()
    
    data = bytearray([
        dec2bcd(second),
        dec2bcd(minute),
        dec2bcd(hour),
        dec2bcd(now[6] + 1),  # Convert weekday from 0-6 to 1-7
        dec2bcd(day),
        dec2bcd(month),
        dec2bcd(year)
    ])
    
    i2c.writeto_mem(DS3231_ADDR, 0x00, data)
    print(f"RTC set to: {month}/{day}/{now[0]} {hour:02d}:{minute:02d}:{second:02d}")
    
    # Verify oscillator is running
    if check_osf():
        print("Warning: Oscillator still shows stopped state!")
    else:
        print("Oscillator running normally")

if __name__ == "__main__":
    set_ds3231()
```

## Setting the RTC using the DS1307

```python
# set the localtime from the DS1307 RTC
from machine import Pin, I2C
from utime import localtime
from ds1307 import DS1307
import config

sda = Pin(config.I2C_SDA_PIN)
scl = Pin(config.I2C_SCL_PIN)
I2C_BUS = config.I2C_BUS
RTC_TYPE = config.RTC_TYPE
RTC_I2C_ADDR = config.RTC_I2C_ADDR

# I2C setup
i2c = I2C(I2C_BUS, scl=scl, sda=sda, freq=3000000)
print(i2c.scan())
rtc = DS1307(addr=RTC_I2C_ADDR, i2c=i2c)
print("DS1307 is on I2C address 0x{0:02x}".format(rtc.addr))
print("Before setting the time the RTC clock had: ", rtc.datetime)
print("Localtime: ", localtime())

# Set the local time
rtc.datetime = localtime()

print("After setting the time from local time the RTC had: ", rtc.datetime)

# Print the date and time in ISO8601 format: 2023-04-18T21:14:22
print("Today is {:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d} weekday:{}".format(
    rtc.year, rtc.month, rtc.day,
    rtc.hour, rtc.minute, rtc.second, rtc.weekday))
```