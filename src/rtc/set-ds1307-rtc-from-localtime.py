from machine import Pin, I2C
from ds1307 import DS1307
from utime import localtime, sleep, time, gmtime

def setup_rtc():
    i2c = I2C(0, sda=Pin(8), scl=Pin(9), freq=100000)
    
    if 0x68 not in i2c.scan():
        print("DS1307 not found! Check connections.")
        return None
    
    return DS1307(i2c=i2c)

def format_time(t):
    """Format time tuple for consistent display"""
    return f"{t[1]:02d}/{t[2]:02d}/{t[0]:04d} {t[3]:02d}:{t[4]:02d}:{t[5]:02d}"

def set_rtc_from_local():
    rtc = setup_rtc()
    if not rtc:
        return
    
    try:
        # Get current time as gmtime tuple (matches the format expected by DS1307)
        current = gmtime(time())
        print("Current gmtime tuple:", current)
        print("Current time formatted:", format_time(current))
        
        # Set the RTC directly with the gmtime tuple
        # gmtime returns exactly what DS1307 expects:
        # (year, month, day, hour, minute, second, weekday, yearday)
        rtc.datetime = current
        print("\nTime set on RTC")
        
        # Verify by reading back
        sleep(1)
        rtc_time = rtc.datetime
        print("\nVerification:")
        print("RTC tuple:", rtc_time)
        print("RTC time formatted:", format_time(rtc_time))
        
    except Exception as e:
        print("Error setting RTC time:", e)

def main():
    print("\nStarting RTC synchronization...")
    set_rtc_from_local()

if __name__ == "__main__":
    main()