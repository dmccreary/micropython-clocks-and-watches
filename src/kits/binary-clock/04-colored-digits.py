from machine import Pin
from neopixel import NeoPixel
from utime import localtime, sleep

# Configuration
NEOPIXEL_PIN = 0
NUM_PIXELS = 20  # Total number of pixels (18 + 2)

# Colors (RGB values) - using light/pastel versions
HOURS_COLOR = (10, 50, 10)     # Light green
MINUTES_COLOR = (10, 10, 60)   # Light cyan
SECONDS_COLOR = (30, 40, 0)    # Light yellow
OFF_COLOR = (0, 0, 0)          # Off

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

def main():
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
        t = localtime()
        hours, minutes, seconds = t[3], t[4], t[5]
        
        # Update the display
        update_display(hours, minutes, seconds)
        
        # Print current time for debugging
        print(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
        
        # Wait before next update
        sleep(1)

if __name__ == "__main__":
    main()