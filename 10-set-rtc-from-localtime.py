from machine import Pin, I2C
from utime import localtime

# I2C setup
sda = Pin(0, Pin.OUT)
scl = Pin(1, Pin.OUT)
i2c = I2C(0, scl=scl, sda=sda, freq=3000000)
DS3231_ADDR = 0x68

def dec2bcd(dec):
    """Convert decimal to binary coded decimal."""
    return (dec // 10) << 4 | (dec % 10)

def set_ds3231():
    now = localtime()
    year = now[0] % 100  # Convert to 2-digit year
    month = now[1]
    day = now[2]
    hour = now[3]
    minute = now[4]
    second = now[5]
    
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

if __name__ == "__main__":
    set_ds3231()