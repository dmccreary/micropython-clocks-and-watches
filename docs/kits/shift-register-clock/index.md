# 74HC595 Shift Register Clock

The display has five wires.  In addition to power and ground we have:

```python
ser_pin=2,    # DIO
srclk_pin=1,  # SCLK
rclk_pin=0    # RCLK
```

The shift register takes in a set of 16 bit commands.
The first byte is the segment information with one
bit for each of the 7 segments and one bit for the colon.
The second bit indicates what digit should be turned on.

Note that for a segment to be on, the bit must be "0".

Here are the letters associated with each of the 7 segments:

```
 aaaa
f    b
f    b
 gggg
e    c
e    c
 dddd
``` 

```python
# bit 0 is the right-most significant bit and is used to turn on the colon.
self.SEGMENTS = {
    'a': 4,  # bit 4
    'b': 3,  # bit 3
    'c': 2,  # bit 2
    'd': 7,  # bit 7
    'e': 6,  # bit 6
    'f': 5,  # bit 5
    'g': 1   # bit 1
}
```

"d"
First byte:  00110000
Second byte: 00010000

This is where "a" is missing.  a is the fourth bit.
First byte:  00010000

This is where all the segments are on except f.  "f" is the 3rd bit
First byte:  00100000
"A" is First byte:  10000000

## Sample Test

The following program will cycle through the digits 0 to 9
on the right most digit to the left most digit.

```python
from machine import Pin
from sr74hc595 import SR74HC595_BITBANG
from utime import sleep, localtime

class FourDigitClock:
    # Class constants
    ALL_OFF = 0xFF            # All segments off (inverted logic)
    SECOND_BYTE = 0b00010000  # Keep bit 4 set in second byte
    
    def __init__(self, ser_pin, srclk_pin, rclk_pin):
        # Initialize pins
        self.ser = Pin(ser_pin, Pin.OUT)      # Serial data
        self.srclk = Pin(srclk_pin, Pin.OUT)  # Shift register clock
        self.rclk = Pin(rclk_pin, Pin.OUT)    # Storage register clock
        
        self.sr = SR74HC595_BITBANG(self.ser, self.srclk, self.rclk)
        
        # Segment bit positions (0 turns segment on)
        # a is the top, b in the upper right, c is the lower right
        # d is the bottom, e is the lower left, f is the upper right
        # g is the middle segment
        self.SEGMENTS = {
            'a': 4,  # bit 4
            'b': 3,  # bit 3
            'c': 2,  # bit 2
            'd': 7,  # bit 7
            'e': 6,  # bit 6
            'f': 5,  # bit 5
            'g': 1   # bit 1
        }
        
        # Define segments needed for each digit
        self.DIGIT_SEGMENTS = {
            0: 'abcdef',   # 0 needs all but g
            1: 'bc',       # 1 needs just b and c
            2: 'abged',    # 2 needs all but c and f
            3: 'abgcd',    # 3 needs all but e and f
            4: 'fbcg',     # 4 needs these four
            5: 'afgcd',    # 5 needs all but e and b
            6: 'afedcg',   # 6 needs all but b
            7: 'abc',      # 7 needs just these three
            8: 'abcdefg',  # 8 needs all segments
            9: 'abfgcd'    # 9 needs all but e
        }
        
        # Pre-calculate patterns for all digits
        self.DIGIT_PATTERNS = {
            digit: self.create_pattern(segments) 
            for digit, segments in self.DIGIT_SEGMENTS.items()
        }

    def create_pattern(self, segments):
        """Create bit pattern from segment letters with inverted logic"""
        pattern = self.ALL_OFF
        for segment in segments:
            if segment in self.SEGMENTS:
                pattern &= ~(1 << self.SEGMENTS[segment])
        return pattern

    def display_pattern(self, first_byte, digit_select_byte):
        """Display a pattern with specified digit selection"""
        self.sr.bits(first_byte, 8)
        self.sr.bits(digit_select_byte, 8)
        self.sr.latch()

    def test_all_positions(self):
        """Test counting 0-9 on all digit positions"""
        print("Testing all digit positions...")
        
        # Digit selection patterns to try
        digit_patterns = [
            (0, 0b00010000, "Rightmost digit"),
            (1, 0b00100000, "Second digit"),
            (2, 0b01000000, "Third digit"),
            (3, 0b10000000, "Leftmost digit")
        ]
        
        # Test each digit position
        for position, digit_select, position_name in digit_patterns:
            print(f"\nTesting {position_name}")
            
            # Count 0-9 on this position
            for number in range(10):
                print(f"Displaying {number} on {position_name}")
                
                # Display the number
                self.display_pattern(self.DIGIT_PATTERNS[number], digit_select)
                sleep(.25)
                
                # Clear display between numbers
                self.display_pattern(self.ALL_OFF, self.ALL_OFF)
                sleep(0.05)
            
            # Wait for user input before moving to next position
            #input(f"Press Enter to test next position...")

def run_position_test():
    """Run position testing"""
    clock = FourDigitClock(
        ser_pin=2,    # DIO
        srclk_pin=1,  # SCLK
        rclk_pin=0    # RCLK
    )
    
    print("Starting position tests...")
    clock.test_all_positions()

# Run the position test
if __name__ == '__main__':
    run_position_test()
```


## References

[74HC595 Shift Register](https://how2electronics.com/shift-register-74hc595-with-raspberry-pi-pico-micropython/)