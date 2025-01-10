# Get time from NTP server
# Jim Tannenbaum - Jan 9th, 2025
import network
import ntptime
import secrets
from utime import sleep
import time

days = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
months = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'June',
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')
ntpTimeHosts = ('time.google.com', 'time1.google.com', 'time2.google.com', 'time3.google.com', 'time4.google.com')
ntpTimeout = 5
maxConnectionAttempts = 10

def ShowDateTime(offsetHrs = 0):
    offsetSecs = offsetHrs * 60 * 60
    gmtTimeSecs = time.mktime(time.localtime())
    now = time.localtime(gmtTimeSecs - offsetSecs)

    month_number = now[1]
    month_name = months[month_number - 1]
    weekday_number = now[6]
    day_name = days[weekday_number]
    hour_number = now[3]
    if hour_number == 0:
        hour_number = 12
    elif hour_number == 12:
        hour_number = 24
    if hour_number < 13:
        hour_12 = hour_number
        am_pm = 'am'
    else:
        hour_12 = hour_number - 12
        am_pm = 'pm'

    print()
    print("Date: {} {} {}, {}".format(day_name, month_name, now[2], now[0]))
    print("Time: {}:{:02} {}".format(hour_12, now[4], am_pm))

def wifiConnect(maxConnectionAttempts = 5):
    print()
    print('Connecting to WiFi Network Name:', secrets.wifi_ssid)
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True) # power up the WiFi chip
    print('Waiting for wifi chip to power up...')
    sleep(3) # wait three seconds for the chip to power up and initialize
    wlan.connect(secrets.wifi_ssid, secrets.wifi_pass)
    print('Waiting for access point to log us in.')
    while maxConnectionAttempts > 0:
            sleep(2)
            if wlan.isconnected():
                print('Success! We have connected to your access point!')
                break
            else:
                print('Failure! We have not connected to your access point!  Trying again.')
                maxConnectionAttempts -= 1
    return wlan.isconnected()

def ntptimeConnect():
    successfulConnection = False
    print()
    ntptime.timeout = ntpTimeout
    for ntpTimeHost in ntpTimeHosts:
        try:
            print('Trying NTP Time host: ' + ntpTimeHost)
            ntptime.host =  ntpTimeHost
            ntptime.settime()
            print('Success! We have connected to the NTP Time host!')
            successfulConnection = True
            break
        except:
            print('NTP Time host timed out! Will try another host')
    return successfulConnection

if wifiConnect(maxConnectionAttempts):
    if ntptimeConnect():
        ShowDateTime(offsetHrs=5) # Accounts for East Coast Time
    else:
        print('Try a different NTP Time host!')
else:
    print('Check your secrets file for SSID and password')
