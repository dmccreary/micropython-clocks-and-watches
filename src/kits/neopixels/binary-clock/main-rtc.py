from machine import Pin, I2C
from neopixel import NeoPixel
from ds3231 import DS3231
from utime import localtime, sleep

# Configuration
NEOPIXEL_PIN = 2
NUM_PIXELS = 20  # Total number of pixels (18 + 2)
I2C_DATA_PIN = 0
I2C_CLOCK_PIN = 1

# Colors (RGB values) - using light/pastel versions
HOURS_COLOR = (10, 50, 10)     # Light green
MINUTES_COLOR = (10, 10, 60)   # Light cyan
SECONDS_COLOR = (30, 40, 0)    # Light yellow
OFF_COLOR = (0, 0, 0)          # Off

I2C_ADDR = 0x68     # DEC 104, HEX 0x68
# connect to the RTC on the I2C bus at 100 kHz
i2c = I2C(0, scl=Pin(I2C_CLOCK_PIN), sda=Pin(I2C_DATA_PIN), freq=100_000)
rtc = DS3231(addr=I2C_ADDR, i2c=i2c)

# Column configuration (start_index, height, color)
COLUMN_CONFIG = {
    'hours_tens':   (18, 2, HOURS_COLOR),   # Column 1: 2 pixels (0-2)
    'hours_ones':   (14, 4, HOURS_COLOR),   # Column 2: 4 pixels (0-9)
    'minutes_tens': (11, 3, MINUTES_COLOR), # Column 3: 3 pixels (0-5)
    'minutes_ones': (7, 4, MINUTES_COLOR),  # Column 4: 4 pixels (0-9)
    'seconds_tens': (4, 3, SECONDS_COLOR),  # Column 5: 3 pixels (0-5)
    'seconds_ones': (0, 4, SECONDS_COLOR),  # Column 6: 4 pixels (0-9)
}

# Initialize NeoPixels
pixels = NeoPixel(Pin(NEOPIXEL_PIN), NUM_PIXELS)

def int_to_binary_column(number, num_bits):
    """Convert a number to binary and return list of bits."""
    binary = []
    for i in range(num_bits):
        binary.append(1 if number & (1 << i) else 0)
    return binary  # LSB first

def set_column(start_index, height, color, number):
    """Set the LEDs for a specific column based on the number."""
    binary = int_to_binary_column(number, height)
    
    # Set each LED in the column
    for bit_pos in range(height):
        pixel_index = start_index + bit_pos
        pixels[pixel_index] = color if binary[bit_pos] else OFF_COLOR

def update_display(hours, minutes, seconds):
    """Update all columns with current time."""
    # Hours
    set_column(*COLUMN_CONFIG['hours_tens'], hours // 10)
    set_column(*COLUMN_CONFIG['hours_ones'], hours % 10)
    
    # Minutes
    set_column(*COLUMN_CONFIG['minutes_tens'], minutes // 10)
    set_column(*COLUMN_CONFIG['minutes_ones'], minutes % 10)
    
    # Seconds
    set_column(*COLUMN_CONFIG['seconds_tens'], seconds // 10)
    set_column(*COLUMN_CONFIG['seconds_ones'], seconds % 10)
    
    pixels.write()  # Update the NeoPixels


print("Binary Clock Started")
print("Columns from right to left:")
print("1. Seconds ones (4 bits) - Light Yellow")
print("2. Seconds tens (3 bits) - Light Yellow")
print("3. Minutes ones (4 bits) - Light Cyan")
print("4. Minutes tens (3 bits) - Light Cyan")
print("5. Hours ones (4 bits) - Light Green")
print("6. Hours tens (2 bits) - Light Green")
print("LSB at bottom of each column")
    
while True:
    # Get current time
    # t = localtime()
    t = rtc.datetime()
    hour = t[4]
    minute = t[5]
    second = t[6]
    
    # add this code to get 12-hour time
    if hour > 12:
        hour -= 12
    
    # Update the display
    update_display(hour, minute, second)
    
    # Print current time for debugging
    print(f"{hour:02d}:{minute:02d}:{second:02d}")
    
    # Wait before next update
    sleep(1)

