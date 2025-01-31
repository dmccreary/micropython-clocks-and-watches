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