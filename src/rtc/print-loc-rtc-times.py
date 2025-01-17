from machine import Pin, I2C
from utime import localtime, sleep
from ds3231 import DS3231

I2C_DATA_PIN = 0
I2C_CLOCK_PIN = 1

I2C_ADDR = 0x68     # DEC 104, HEX 0x68

i2c = I2C(0, scl=Pin(I2C_CLOCK_PIN), sda=Pin(I2C_DATA_PIN), freq=800000)
rtc = DS3231(addr=I2C_ADDR, i2c=i2c)

rtc_time = rtc.datetime()
rtc_year = rtc_time[0]
rtc_month = rtc_time[1]
rtc_day = rtc_time[2]
# skip 3
rtc_hour = rtc_time[4]
rtc_minute = rtc_time[5]
rtc_second = rtc_time[6]

loc_year = rtc_time[0]
loc_month = rtc_time[1]
loc_day = rtc_time[2]
loc_hour = rtc_time[4]
loc_minute = rtc_time[5]
loc_second = rtc_time[6]

print("   localtime()", localtime())
print("rtc.datetime()", rtc.datetime())
while True:
    print(f"LOC: {loc_month}/{loc_day}/{loc_year} {loc_hour:02d}:{loc_minute:02d}:{loc_second:02d}")
    print(f"RTC: {rtc_month}/{rtc_day}/{rtc_year} {rtc_hour:02d}:{rtc_minute:02d}:{rtc_second:02d}")
    sleep(1)

