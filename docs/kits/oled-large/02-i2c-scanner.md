# I2C Scanner Test

This program will verify that your RTC clock is connected correctly to your Raspberry Pi Pico.

```py
from machine import I2C, Pin
import config

DST_PIN = 0
CLK_PIN = 1

print("Data DST on pin: ", DST_PIN)
print("Clock CLK on pin: ", CLK_PIN)

i2c = I2C(0, scl=Pin(CLK_PIN), sda=Pin(DST_PIN), freq=800000)

scan_result = i2c.scan()

print(scan_result)

print("I2C addresses found:", [hex(device_address) for device_address in i2c.scan()])
```

This will return a list of the I2C addresses found on your I2C Bus 0.
If your DS3231 real-time clock has an address of
0x68 (hex) which is 104 decimal.

You will also see a second I2C address for the EEPROM which is 
0x50 (hex) and 80 decimal.  These numbers may vary if you purchased
different versions of a real-time clock.

For details see the section on [Real Time Clocks](../../lessons/rtc/index.md).