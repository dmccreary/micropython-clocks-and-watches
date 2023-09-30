# Display Time and Date

Here is a program that will display the time and date
including the day-of-the-week and the name of the month.

We use the ``localtime()``` function to get the current time
in an array of integers that looks like this:

```py
(2023, 9, 30, 13, 18, 9, 5, 273)
```

The fields are:

1. Year
2. Month
3. Day of Month
4. Hour in 24-hour format
5. Minutes
6. Seconds
7. Day of Week (Monday = 0, Sunday = 6)
7. Day of the Year

We could convert each of these numbers to strings and display them.
However, most people like to do a bit of formatting such as
displaing a 12-hour am/pm format and returning the name
of the month and day of the week.  Here is the complete
progam with the formatting.

```py
# 02-display-time.py
# 
from machine import Pin, SPI
from utime import sleep, localtime
import gc9a01
import vga1_bold_16x32 as font

# this uses the standard Dupont ribbon cable spanning rows 4-9 on our breadboard
SCK_PIN = 2 # row 4
SDA_PIN = 3
DC_PIN = 4
CS_PIN = 5
# GND is row 8
RST_PIN = 6

# define the SPI intrface
spi = SPI(0, baudrate=60000000, sck=Pin(SCK_PIN), mosi=Pin(SDA_PIN))
tft = gc9a01.GC9A01(spi, 240, 240, reset=Pin(RST_PIN, Pin.OUT),
    cs=Pin(CS_PIN, Pin.OUT), dc=Pin(DC_PIN, Pin.OUT), rotation=0
)

tft.init()
tft.fill(0) # fill the screen with black

days = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday',
        'Sunday')
# I limit the month names to 5 characters max
months = ('Jan', 'Feb', 'March', 'April', 'May', 'June', 'July',
          'Aug', 'Sept', 'Oct', 'Nov', 'Dec')
label = ('year', 'month', 'mday', 'hour', 'minute', 'second', 'weekday', 'yearday')

def format_time(now):
    hour_number = now[3]
    if hour_number < 13:
        hour_12 = hour_number
        am_pm = 'am'
    else:
        hour_12 = hour_number - 12
        am_pm = 'pm'
    minutes_num = now[4]
    if minutes_num < 10:
        min_leading_zero = '0'
    else:
        min_leading_zero = ''
    seconds_num = now[5]
    if seconds_num < 10:
        sec_leading_zero = '0'
    else:
        sec_leading_zero = ''
    return "{}:{}{}:{}{} {}".format(hour_12, min_leading_zero, minutes_num, sec_leading_zero, seconds_num, am_pm)

def day_of_week(now):
    weekday_number = now[6]
    day_name = days[weekday_number]
    return day_name

def format_date(now):
    month_number = now[1]
    month_name = months[month_number - 1]
    weekday_number = now[6]
    day_name = days[weekday_number]
    hour_number = now[3]
    return "{} {}, {}".format(month_name, now[2], now[0])

tft.fill(0) # erase the screen to black
white = gc9a01.color565(255, 255, 255)
while(True):
    # get the time from the local real-time clock
    now = localtime()
    print(now)    
    tft.text(font, format_time(now), 35, 50, white)
    tft.text(font, day_of_week(now), 50, 80, white)
    tft.text(font, format_date(now), 5, 110, white)
    #tft.show()
    sleep(1)
```