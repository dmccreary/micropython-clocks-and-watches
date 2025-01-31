from machine import Pin, I2C
import ds3231
import config
from time import localtime

# Initialize I2C and RTC
i2c = I2C(config.I2C_BUS, sda=Pin(config.I2C_SDA_PIN), scl=Pin(config.I2C_SCL_PIN))
rtc = ds3231.DS3231(i2c)

def format_time(datetime_tuple):
    # Unpack the 8-value tuple returned by rtc.datetime()
    # Format is: year, month, day, weekday, hour, minutes, seconds, subseconds
    year, month, day, weekday, hour, minute, second, subseconds = datetime_tuple
    
    # Convert to 12-hour format
    am_pm = "AM" if hour < 12 else "PM"
    hour_12 = hour if hour <= 12 else hour - 12
    if hour_12 == 0:
        hour_12 = 12
        
    # Create day and month lookup tables
    # weekday in RTC is 1-7 (Monday=1, Sunday=7)
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    months = ['January', 'February', 'March', 'April', 'May', 'June', 
              'July', 'August', 'September', 'October', 'November', 'December']
    
    # Adjust weekday to 0-based index for days list
    weekday_index = weekday - 1
    
    return f"{days[weekday_index]}, {months[month-1]} {day}, {year} {hour_12}:{minute:02d}:{second:02d} {am_pm}"

def verify_time(local_time):
    """
    Verify that local_time values are within acceptable bounds
    Returns: True if time appears valid, False otherwise
    """
    # Unpack tuple
    l_year, l_month, l_day, l_hour, l_min, l_sec, l_wday, l_yday = local_time
    
    # Basic bounds checking
    if not (2000 <= l_year <= 2099):
        print("Error: Year out of range (2000-2099)")
        return False
    if not (1 <= l_month <= 12):
        print("Error: Month out of range (1-12)")
        return False
    if not (1 <= l_day <= 31):
        print("Error: Day out of range (1-31)")
        return False
    if not (0 <= l_hour <= 23):
        print("Error: Hour out of range (0-23)")
        return False
    if not (0 <= l_min <= 59):
        print("Error: Minute out of range (0-59)")
        return False
    if not (0 <= l_sec <= 59):
        print("Error: Second out of range (0-59)")
        return False
    
    return True

# Get current RTC time and print it
print("\nCurrent RTC time before setting:")
current_rtc_time = rtc.datetime()
print(format_time(current_rtc_time))

# Get local time
local = localtime()
print("\nSystem local time:")
print(f"Year: {local[0]}, Month: {local[1]}, Day: {local[2]}")
print(f"Hour: {local[3]}, Minute: {local[4]}, Second: {local[5]}")
print(f"Weekday: {local[6]} (0=Monday, 6=Sunday)")

# Verify the time data
if verify_time(local):
    # Convert weekday from localtime (0-6, Monday=0) to RTC format (1-7, Monday=1)
    rtc_weekday = local[6] + 1
    
    # Create datetime tuple in correct order for rtc.datetime()
    # According to the driver docstring:
    # datetime : tuple, (0-year, 1-month, 2-day, 3-hour, 4-minutes[, 5-seconds[, 6-weekday]])
    new_time = (
        local[0],     # year
        local[1],     # month
        local[2],     # day
        local[3],     # hour
        local[4],     # minute
        local[5],     # second
        rtc_weekday   # weekday (1-7, Monday=1)
    )
    
    # Set the RTC
    rtc.datetime(new_time)
    print("\nRTC time set successfully!")
    
    # Read back and print the new time
    print("\nNew RTC time after setting:")
    new_rtc_time = rtc.datetime()
    print(format_time(new_rtc_time))
else:
    print("\nError: Time verification failed. RTC not set.")