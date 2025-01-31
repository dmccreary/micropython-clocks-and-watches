# OLED Test Prompt

We can use generative AI tools to build test programs.
But in order to get working programs, we need to tell
the generative AI about what our hardware is and
what our configuration is.  We can leverage the
```config.py``` file to tell the generative AI tools
about our local configuration.

## Sample Prompt

!!! prompt
    You are an expert at helping high-school kids learn computational thinking using MicroPython.
    I am working on writing a test program written in MicroPython.
    I have a 128x64 OLED using ssd1306 display driver chip connected to a Raspberry Pi Pico W running MicroPython version 1.24.1 using
    an SPI bus.
    I have the ssd1306.py driver loaded into the /lib directory.

    Please write a MicroPython program that prints "Hello World!" on the OLED display.  Use the config.py program in the project to setup
    the display.

If your AI does not have a project feature, you can include the config.py in the prompt:

```python
# MicroPython hardware configuration file for Raspberry Pi Pico W
# Using an SPI OLED Display, a DS3231 RTC with EEPROM, and three buttons

SPI_BUS = 0
SPI_SCL_PIN = 2 # Clock
SPI_SDA_PIN = 3 # labeled SDI(MOSI) on the back of the display
SPI_RESET_PIN = 4 # Reset
SPI_DC_PIN = 5 # Data/command
SPI_CS_PIN = 6 # Chip Select

# I2C Bus for the DS3231 RTC
I2C_BUS = 0
I2C_DT_PIN = 0 # Data
I2C_SCK_PIN = 1 # Clock
RTC_ADDRESS = 0x68
EEPROM_ADDRESS = 0x57

# OLED Screen Dimensions
DISPLAY_WIDTH=128
DISPLAY_HEIGHT=64

# Button Pins where the buttons are between the GPIO and GND
# Make sure to configure the pull-up resistor in the code
BUTTON_MODE_PIN = 14
BUTTON_INCREMENT_PIN = 15
BUTTON_DECREMENT_PIN = 16
```