from utime import localtime, sleep
from LCD_1inch28 import LCD_1inch28

LCD = LCD_1inch28()  


days = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday',
        'Sunday')
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
        
def format_date(now):
    month_number = now[1]
    month_name = months[month_number - 1]
    weekday_number = now[6]
    day_name = days[weekday_number]
    hour_number = now[3]
    return "{} {} {}, {}".format(day_name, month_name, now[2], now[0])

while(True):
    now = localtime()
    # print(now)
    LCD.fill(LCD.black)    
    LCD.text(format_time(now), 77, 50, LCD.white)
    LCD.text(format_date(now), 40, 80, LCD.white)
    LCD.show()
    sleep(1)