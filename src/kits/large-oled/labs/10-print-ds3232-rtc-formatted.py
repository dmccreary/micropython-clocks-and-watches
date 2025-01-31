from machine import Pin, I2C
import ds3231
import config

i2c = I2C(0, sda=Pin(config.I2C_SDA_PIN), scl=Pin(config.I2C_SCL_PIN))
rtc = ds3231.DS3231(i2c)

def format_time(datetime_tuple):
    # Unpack the 8-value tuple
    year, month, day, hour, minute, second, subseconds, weekday = datetime_tuple
    
    # Convert to 12-hour format
    am_pm = "AM" if hour < 12 else "PM"
    hour_12 = hour if hour <= 12 else hour - 12
    if hour_12 == 0:
        hour_12 = 12
        
    # Create day and month lookup tables
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    months = ['January', 'February', 'March', 'April', 'May', 'June', 
              'July', 'August', 'September', 'October', 'November', 'December']
    
    # Use 'd' instead of '02d' for hours to remove leading zero
    return f"{days[weekday]}, {months[month-1]} {day}, {year} {hour_12}:{minute:02d}:{second:02d} {am_pm}"

datetime = rtc.datetime()
# this returns a format like Monday, January 31, 2025 5:11:30 AM
print(format_time(datetime))