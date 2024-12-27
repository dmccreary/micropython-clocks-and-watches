# Clock Main

## Details

This program use 12 hour time and also flashes the colon ever 1/2 second.
It also is designed to work with a real-time clock that might take
a bit of time to startup with the Pico first powers up.

```python
from machine import Pin, RTC 
from sr74hc595 import SR74HC595_BITBANG
from utime import sleep, localtime, ticks_ms

def wait_for_rtc():
    print("Waiting for RTC to be ready...")
    rtc = RTC()
    while True:
        current_time = rtc.datetime()
        # On Pico, default RTC starts at (2021, 1, 1, 0, 0, 0, 0, 0)
        # So we check if it's been set to something else
        if current_time[0] != 2021 or current_time[1] != 1 or current_time[2] != 1:
            print("RTC is ready!")
            return
        print("RTC not ready yet...")
        sleep(1)  # Check every second

class FourDigitClock:
    ALL_OFF = 0xFF  # All segments off (inverted logic)
    
    def __init__(self, ser_pin, srclk_pin, rclk_pin):
        self.ser = Pin(ser_pin, Pin.OUT)
        self.srclk = Pin(srclk_pin, Pin.OUT) 
        self.rclk = Pin(rclk_pin, Pin.OUT)
        self.sr = SR74HC595_BITBANG(self.ser, self.srclk, self.rclk)
        
        self.SEGMENTS = {
            'a': 4, 'b': 3, 'c': 2, 
            'd': 7, 'e': 6, 'f': 5, 'g': 1
        }
        self.DIGIT_SEGMENTS = {
            0: 'abcdef', 1: 'bc', 2: 'abged', 3: 'abgcd',
            4: 'fbcg', 5: 'afgcd', 6: 'afedcg', 
            7: 'abc', 8: 'abcdefg', 9: 'abfgcd'
        }
        self.DIGIT_PATTERNS = {
            digit: self.create_pattern(segments)
            for digit, segments in self.DIGIT_SEGMENTS.items()
        }
        self.DIGIT_SELECT = [
            0b00010000,  # Rightmost digit
            0b00100000,  # Second digit 
            0b01000000,  # Third digit
            0b10000000   # Leftmost digit  
        ]
        
    def create_pattern(self, segments):
        pattern = self.ALL_OFF
        for segment in segments:
            if segment in self.SEGMENTS:
                pattern &= ~(1 << self.SEGMENTS[segment]) 
        return pattern
    
    def display_digit(self, digit, position, dp=False):
        pattern = self.DIGIT_PATTERNS[digit]
        if dp:
            pattern &= ~(1 << 0)  # Turn on decimal point
        self.sr.bits(pattern, 8)
        self.sr.bits(self.DIGIT_SELECT[position], 8)
        self.sr.latch()
        
    def display_time(self, hour, minute, colon_state):
        # Convert to 12-hour format
        if hour > 12:
            hour -= 12
        elif hour == 0:  
            hour = 12
            
        digits = [hour // 10, hour % 10, minute // 10, minute % 10]
        
        for position, digit in enumerate(reversed(digits)):
            self.display_digit(digit, position, dp=(position == 1 and colon_state))
            sleep(0.002)  # Reduced persistence timing
            
    
def run_clock():
    # wait for a good time to come from localtime()
    wait_for_rtc()

    clock = FourDigitClock(ser_pin=2, srclk_pin=1, rclk_pin=0)
    print("Starting clock...")
    
    last_second = -1
    colon_state = True
    last_toggle = ticks_ms()
    
    while True:
        current_time = localtime()
        hour = current_time[3]
        minute = current_time[4]
        current_second = current_time[5]
        
        if ticks_ms() - last_toggle >= 500:
            colon_state = not colon_state
            last_toggle = ticks_ms()
        
        clock.display_time(hour, minute, colon_state)


if __name__ == '__main__':
    run_clock()
```