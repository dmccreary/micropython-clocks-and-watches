# Shift Register Displays

The 74hc595 is a chip that takes a clock and data stream in and turns many LEDs on or off.
74hc595 chips can be connected in series to control 7 segments on 4 digits.

I'll create a detailed walkthrough of the ```clock-driver.py``` program, breaking it down into digestible sections with accompanying labs. This will help students understand both the code and the underlying concepts.

## 1. Core Components and Imports

```python
from machine import Pin, RTC 
from sr74hc595 import SR74HC595_BITBANG
from utime import sleep, localtime, ticks_ms
```

This section imports the necessary libraries. The program uses:
- `machine.Pin`: Controls individual GPIO pins on the Pico
- `RTC`: Real-Time Clock for keeping time
- `sr74hc595`: Manages the shift register that controls the display
- `utime`: Provides timing functions

### **Lab 1: Understanding GPIO Pins**

Have students create a simple LED blink program:

```python
from machine import Pin
from utime import sleep

led = Pin(25, Pin.OUT)  # Built-in LED on Pico
while True:
    led.value(1)  # Turn on
    sleep(1)
    led.value(0)  # Turn off
    sleep(1)
```

## 2. RTC Initialization

```python
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
```

This function ensures the RTC has been set to a valid time before proceeding.

### **Lab 2: RTC Basics**

Have students experiment with reading and setting the RTC:

```python
from machine import RTC
from utime import sleep

rtc = RTC()
# Set the time (year, month, day, weekday, hour, minute, second, subsecond)
rtc.datetime((2024, 12, 27, 5, 14, 30, 0, 0))

while True:
    current_time = rtc.datetime()
    print(f"Current time: {current_time[4]:02d}:{current_time[5]:02d}:{current_time[6]:02d}")
    sleep(1)
```

## 3. Seven-Segment Display Setup
```python
class FourDigitClock:
    ALL_OFF = 0xFF  # All segments off (inverted logic)
    
    def __init__(self, ser_pin, srclk_pin, rclk_pin):
        self.ser = Pin(ser_pin, Pin.OUT)
        self.srclk = Pin(srclk_pin, Pin.OUT) 
        self.rclk = Pin(rclk_pin, Pin.OUT)
```
This class manages the four-digit display. It uses three pins to control the shift register.

### **Lab 3: Seven-Segment Pattern Display**
Have students create a simple program to display a single digit:
```python
from machine import Pin
from utime import sleep

# Create a simple version that lights up segments manually
segments = {
    'a': Pin(2, Pin.OUT),
    'b': Pin(3, Pin.OUT),
    'c': Pin(4, Pin.OUT),
    # ... add more segments
}

def display_number(number):
    # Pattern for number 1
    if number == 1:
        segments['b'].value(1)
        segments['c'].value(1)
    # Add more numbers...
```

## 4. Digit Patterns

```python
self.SEGMENTS = {
    'a': 4, 'b': 3, 'c': 2, 
    'd': 7, 'e': 6, 'f': 5, 'g': 1
}
self.DIGIT_SEGMENTS = {
    0: 'abcdef', 1: 'bc', 2: 'abged', 3: 'abgcd',
    4: 'fbcg', 5: 'afgcd', 6: 'afedcg', 
    7: 'abc', 8: 'abcdefg', 9: 'abfgcd'
}
```
This section defines which segments should be lit for each number.

### **Lab 4: Pattern Design**

Have students draw and design their own custom characters using the seven segments. They can create:
- Letters (A, b, C, d, E, F)
- Custom symbols
- Animated patterns

## 5. Time Display Logic

```python
def display_time(self, hour, minute, colon_state):
    # Convert to 12-hour format
    if hour > 12:
        hour -= 12
    elif hour == 0:  
        hour = 12
```

### **Lab 5: Time Format Conversion**
Have students write a program that converts between 24-hour and 12-hour time formats:

```python
def convert_time(hour24):
    if hour24 > 12:
        return hour24 - 12, "PM"
    elif hour24 == 0:
        return 12, "AM"
    elif hour24 == 12:
        return 12, "PM"
    else:
        return hour24, "AM"
```

## Advanced Labs and Extensions:

### 1. **Alarm Clock Lab**

Modify the clock to add alarm functionality:
- Add a button to set alarm time
- Add a buzzer for the alarm
- Implement snooze functionality

### 2. **Temperature Display Lab**

Alternate between showing time and temperature:
- Add a temperature sensor
- Display temperature for 3 seconds every minute
- Add a button to toggle between time and temperature

### 3. **Custom Animation Lab**

Create animations for the display:
- Make digits spin when changing
- Create a "snake" animation for the top of each hour
- Design transitions between numbers

### 4. **World Clock Lab**

Modify the clock to show multiple time zones:
- Add buttons to cycle through different time zones
- Show timezone abbreviation
- Store favorite time zones

### 5. **Stopwatch Lab**
Add stopwatch functionality:
- Use buttons to start/stop/reset
- Display tenths of seconds
- Store lap times

## Summary

These labs progressively build upon the base code while introducing new concepts and challenges. Each lab reinforces different programming concepts:

- Variables and data types
- Control structures (if/else, loops)
- Functions and methods
- Object-oriented programming
- Hardware interaction
- Time and date handling
- User input processing

This allows students to learn both programming and hardware concepts in a hands-on, engaging way while creating something practical and visible.
