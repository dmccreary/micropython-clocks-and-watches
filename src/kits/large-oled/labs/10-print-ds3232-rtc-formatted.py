from machine import Pin, I2C
import ds3231
import config
from time import localtime

i2c = I2C(config.I2C_BUS, sda=Pin(config.I2C_SDA_PIN), scl=Pin(config.I2C_SCL_PIN))
rtc = ds3231.DS3231(i2c)

def format_time(datetime_tuple):
    # RTC returns: year, month, day, weekday, hour, minute, second, subseconds
    year, month, day, weekday, hour, minute, second, subseconds = datetime_tuple
    
    am_pm = "AM" if hour < 12 else "PM"
    hour_12 = hour if hour <= 12 else hour - 12
    if hour_12 == 0:
        hour_12 = 12
        
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    months = ['January', 'February', 'March', 'April', 'May', 'June', 
              'July', 'August', 'September', 'October', 'November', 'December']
    
    # RTC uses 1-7 for weekday, convert to 0-6 index
    weekday_index = (weekday - 1) % 7
    
    return f"{days[weekday_index]}, {months[month-1]} {day}, {year} {hour_12}:{minute:02d}:{second:02d} {am_pm}"

def verify_time(local_time):
    l_year, l_month, l_day, l_hour, l_min, l_sec, l_wday, l_yday = local_time
    return (2000 <= l_year <= 2099 and 1 <= l_month <= 12 and 1 <= l_day <= 31 
            and 0 <= l_hour <= 23 and 0 <= l_min <= 59 and 0 <= l_sec <= 59 
            and 0 <= l_wday <= 6)

print("\nCurrent RTC time before setting:")
current_rtc_time = rtc.datetime()
print(format_time(current_rtc_time))

local = localtime()
print("\nSystem local time:")
print(f"Year: {local[0]}, Month: {local[1]}, Day: {local[2]}")
print(f"Hour: {local[3]}, Minute: {local[4]}, Second: {local[5]}")
print(f"Weekday: {local[6]} (0=Monday, 6=Sunday)")

if verify_time(local):
    # Create datetime tuple for RTC
    # RTC expects: year, month, day, weekday in format 1-7
    new_time = (
        local[0],        # year
        local[1],        # month
        local[2],        # day
        local[3],        # hour
        local[4],        # minute
        local[5],        # second
        (local[6] + 1)   # weekday: convert 0-6 to 1-7
    )
    
    rtc.datetime(new_time)
    print("\nRTC time set successfully!")
    
    print("\nNew RTC time after setting:")
    new_rtc_time = rtc.datetime()
    print(format_time(new_rtc_time))
else:
    print("\nError: Time verification failed. RTC not set.")