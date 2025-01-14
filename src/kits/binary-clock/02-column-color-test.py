from machine import Pin
from neopixel import NeoPixel
from utime import sleep

# Configuration
NEOPIXEL_PIN = 0
NUM_PIXELS = 20

# Define colors (RGB values)
RED = (150, 0, 0)         # Column 6 (seconds ones)
ORANGE = (180, 50, 0)    # Column 5 (seconds tens)
YELLOW = (255, 255, 0)    # Column 4 (minutes ones)
GREEN = (0, 150, 0)       # Column 3 (minutes tens)
BLUE = (0, 0, 150)        # Column 2 (hours ones)
PURPLE = (180, 0, 150)    # Column 1 (hours tens)
OFF = (0, 0, 0)

# Column configuration (start_index, height, color)
COLUMN_CONFIG = [
    {'start': 0, 'height': 4, 'color': RED},     # Column 6 (seconds ones)
    {'start': 4, 'height': 3, 'color': ORANGE},  # Column 5 (seconds tens)
    {'start': 7, 'height': 4, 'color': YELLOW},  # Column 4 (minutes ones)
    {'start': 11, 'height': 3, 'color': GREEN},  # Column 3 (minutes tens)
    {'start': 14, 'height': 4, 'color': BLUE},   # Column 2 (hours ones)
    {'start': 18, 'height': 2, 'color': PURPLE}, # Column 1 (hours tens)
]

# Initialize NeoPixels
pixels = NeoPixel(Pin(NEOPIXEL_PIN), NUM_PIXELS)

def test_columns():
    # Set each column to its color
    for col in COLUMN_CONFIG:
        for i in range(col['start'], col['start'] + col['height']):
            pixels[i] = col['color']
    
    pixels.write()

# Run the test
print("Starting NeoPixel column test...")
print("Column 6 (seconds ones, indices 0-3): Red")
print("Column 5 (seconds tens, indices 4-6): Orange")
print("Column 4 (minutes ones, indices 7-10): Yellow")
print("Column 3 (minutes tens, indices 11-13): Green")
print("Column 2 (hours ones, indices 14-17): Blue")
print("Column 1 (hours tens, indices 18-19): Purple")

test_columns()
