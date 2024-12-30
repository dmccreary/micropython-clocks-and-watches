from machine import Pin, RTC
from sr74hc595 import SR74HC595_BITBANG
from mp_button import Button
from time import localtime, sleep, ticks_ms

def wait_for_rtc():
    print("Waiting for RTC to be ready...")
    rtc = RTC()
    while True:
        current_time = rtc.datetime()
        if current_time[0] != 2021 or current_time[1] != 1 or current_time[2] != 1:
            print("RTC is ready!")
            return
        print("RTC not ready yet...")
        sleep(1)

class FourDigitClock:
    ALL_OFF = 0xFF  
    
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
            sleep(0.002)

def button_mode_irq(button, event):
    global mode
    if event == Button.PRESSED:
        mode += 1
        mode = mode % mode_count
        print('new mode:', mode, mode_names[mode])

def button_next_irq(button, event):
    global mode, hours, minutes, am_pm
    if event == Button.PRESSED:
        if mode == 1:
            hours = (hours + 1) % 24
        if mode == 2:
            minutes = (minutes + 1) % 60
        if mode == 3:
            am_pm = 1 if am_pm == 0 else 0
        print('next button:', hours, minutes, am_pm)
            
def button_previous_irq(button, event):
    global mode, hours, minutes, am_pm
    if event == Button.PRESSED:
        if mode == 1:
            hours = (hours - 1) % 24
        if mode == 2:
            minutes = (minutes - 1) % 60
        if mode == 3:
            am_pm = 1 if am_pm == 0 else 0
        print('prev button:', hours, minutes, am_pm)

def run_clock():
    global mode, hours, minutes, am_pm, mode_count, mode_names
    
    wait_for_rtc()
    
    clock = FourDigitClock(ser_pin=2, srclk_pin=1, rclk_pin=0)
    print("Starting clock...")
    
    mode = 0
    mode_names = ["run", "set hour", "set minute", "set AM/PM"]
    mode_count = len(mode_names)
    
    # Initialize buttons
    button_mode = Button(16, False, button_mode_irq, internal_pullup=True, debounce_time=100)
    button_next = Button(17, False, button_next_irq, internal_pullup=True, debounce_time=100)
    button_previous = Button(18, False, button_previous_irq, internal_pullup=True, debounce_time=100)
    
    colon_state = True
    last_toggle = ticks_ms()
    last_time = localtime()
    hours = last_time[3]
    minutes = last_time[4]
    am_pm = 1 if hours >= 12 else 0
    
    while True:
        # Update buttons
        button_mode.update()
        button_next.update()
        button_previous.update()
        
        # Handle display updates
        if mode == 0:  # Normal running mode
            current_time = localtime()
            hours = current_time[3]
            minutes = current_time[4]
            
        # Update colon every 500ms
        if ticks_ms() - last_toggle >= 500:
            colon_state = not colon_state
            last_toggle = ticks_ms()
            
        # Display current time
        clock.display_time(hours, minutes, colon_state)
        sleep(0.01)  # Small delay to prevent display flickering

if __name__ == '__main__':
    run_clock()