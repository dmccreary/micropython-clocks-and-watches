# Manually Setting the Time

<iframe width="560" height="315" src="https://www.youtube.com/embed/0fLNS-BfQ48?si=9EUzF7gv-UDJ5R3z" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

[Setting the Time](https://youtu.be/0fLNS-BfQ48)

Next, we will create a complete program that implements a clock with 
manual time setting using the three buttons. This is a great practical 
example that teaches state management and user input handling.

```python
import tm1637
from machine import Pin, RTC
from utime import sleep, localtime, ticks_ms

# Initialize display and RTC
tm = tm1637.TM1637(clk=Pin(0), dio=Pin(1))
rtc = RTC()

# Initialize buttons with pull-up resistors
mode_btn = Pin(2, Pin.IN, Pin.PULL_UP)
next_btn = Pin(3, Pin.IN, Pin.PULL_UP)
prev_btn = Pin(4, Pin.IN, Pin.PULL_UP)

# Clock modes
RUNNING = 0
SET_HOUR = 1
SET_MINUTE = 2
SET_AMPM = 3

class Clock:
    def __init__(self):
        self.mode = RUNNING
        self.hours = 12
        self.minutes = 0
        self.is_pm = False
        self.colon_on = True
        self.last_button_time = ticks_ms()
        self.button_debounce = 200  # milliseconds
        self.load_time_from_rtc()
        
    def load_time_from_rtc(self):
        """Get current time from RTC"""
        _, _, _, _, hours, minutes, _, _ = rtc.datetime()
        self.hours = hours % 12
        if self.hours == 0:
            self.hours = 12
        self.is_pm = hours >= 12
        self.minutes = minutes
        
    def save_time_to_rtc(self):
        """Save current time to RTC"""
        current_time = list(rtc.datetime())
        hours = self.hours
        if self.is_pm and hours != 12:
            hours += 12
        elif not self.is_pm and hours == 12:
            hours = 0
        current_time[4] = hours  # Set hours
        current_time[5] = self.minutes  # Set minutes
        rtc.datetime(tuple(current_time))
        
    def debounce(self):
        """Handle button debouncing"""
        current_time = ticks_ms()
        if current_time - self.last_button_time < self.button_debounce:
            return False
        self.last_button_time = current_time
        return True
        
    def handle_buttons(self):
        """Process button inputs"""
        if not self.debounce():
            return
            
        # Mode button cycles through modes
        if mode_btn.value() == 0:  # Button pressed (active low)
            self.mode = (self.mode + 1) % 4
            if self.mode == RUNNING:
                self.save_time_to_rtc()
            
        # Next/Previous buttons modify current setting
        elif next_btn.value() == 0 or prev_btn.value() == 0:
            increment = -1 if prev_btn.value() == 0 else 1
            
            if self.mode == SET_HOUR:
                self.hours = ((self.hours + increment - 1) % 12) + 1
            elif self.mode == SET_MINUTE:
                self.minutes = (self.minutes + increment) % 60
            elif self.mode == SET_AMPM:
                self.is_pm = not self.is_pm
    
    def update_display(self):
        """Update the TM1637 display based on current mode and time"""
        if self.mode == RUNNING:
            # Normal time display with blinking colon
            self.colon_on = not self.colon_on
        else:
            # Setting mode - flash the active component
            flash_on = (ticks_ms() // 500) % 2 == 0
            
            if self.mode == SET_HOUR:
                if not flash_on:
                    tm.show('    ')
                    return
            elif self.mode == SET_MINUTE:
                if not flash_on:
                    tm.numbers(self.hours, 0)
                    return
            elif self.mode == SET_AMPM:
                if flash_on:
                    tm.show(' ' + ('P' if self.is_pm else 'A') + ' ')
                    return
                
        # Update display
        tm.numbers(self.hours, self.minutes, colon=self.colon_on)
        
    def run(self):
        """Main clock loop"""
        tm.brightness(2)  # Set initial brightness
        
        while True:
            self.handle_buttons()
            
            if self.mode == RUNNING:
                self.load_time_from_rtc()
            
            self.update_display()
            sleep(0.1)  # Small delay to prevent display flicker

# Create and run the clock
if __name__ == '__main__':
    clock = Clock()
    print("Starting clock... Use buttons to set time:")
    print("Mode: Switch between run/set hour/set minute/set AM,PM")
    print("Next/Prev: Adjust current setting")
    clock.run()
```

Key concepts and features of this implementation:

1. **Button Handling**
   - Uses pull-up resistors (buttons connect to ground when pressed)
   - Implements debouncing to prevent multiple triggers
   - Buttons are active-low (0 when pressed, 1 when released)

2. **Mode System**
   - RUNNING: Normal clock operation
   - SET_HOUR: Adjust hours (1-12)
   - SET_MINUTE: Adjust minutes (0-59)
   - SET_AMPM: Toggle between AM and PM

3. **Visual Feedback**
   - Selected component flashes when being set
   - Colon blinks in running mode
   - Special AM/PM display during setting

4. **Time Management**
   - Maintains time in 12-hour format internally
   - Converts to/from 24-hour format for RTC
   - Handles midnight/noon edge cases

5. **State Management**
   - Uses a class to organize state and behavior
   - Separates display, button handling, and time management

Common challenges students might encounter:

1. **Button Debouncing**
   - Understanding why debouncing is necessary
   - Adjusting debounce timing for reliable operation

2. **Time Format Conversion**
   - Converting between 12/24 hour formats
   - Handling edge cases (12 AM/PM)

3. **Display Updates**
   - Managing display refresh rate
   - Creating smooth visual feedback

Suggested exercises for students:

1. Add a temperature display mode
2. Implement a brightness adjustment feature
3. Add an alarm setting mode
4. Save settings to flash memory
5. Add a battery backup indicator

Would you like me to explain any part in more detail or provide examples of these extensions?