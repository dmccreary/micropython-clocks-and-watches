from machine import Pin
from neopixel import NeoPixel
from utime import sleep

# Configuration
NEOPIXEL_PIN = 0
NUM_PIXELS = 20

# Define colors (RGB values)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
OFF = (0, 0, 0)

# Initialize NeoPixels
pixels = NeoPixel(Pin(NEOPIXEL_PIN), NUM_PIXELS)

def clear_pixels():
    """Turn off all pixels"""
    for i in range(NUM_PIXELS):
        pixels[i] = OFF
    pixels.write()

def test_sections():
    """Test each time section with its designated color"""
    clear_pixels()
    
    # Seconds (indices 0-6) - RED
    # seconds ones (0-3)
    for i in range(4):
        pixels[i] = RED
    # seconds tens (4-6)
    for i in range(4, 7):
        pixels[i] = RED
        
    # Minutes (indices 7-13) - GREEN
    # minutes ones (7-10)
    for i in range(7, 11):
        pixels[i] = GREEN
    # minutes tens (11-13)
    for i in range(11, 14):
        pixels[i] = GREEN
        
    # Hours (indices 14-19) - BLUE
    # hours ones (14-17)
    for i in range(14, 18):
        pixels[i] = BLUE
    # hours tens (18-19)
    for i in range(18, 20):
        pixels[i] = BLUE
    
    pixels.write()

# Run the test
print("Starting NeoPixel test...")
print("Seconds pixels (0-6): RED")
print("Minutes pixels (7-13): GREEN")
print("Hours pixels (14-19): BLUE")

test_sections()
print("Test pattern displayed. Press Ctrl+C to exit.")

try:
    while True:
        sleep(1)
except KeyboardInterrupt:
    clear_pixels()
    print("Test ended.")