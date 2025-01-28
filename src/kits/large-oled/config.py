# Dan's Robot Labs configuration file for Raspberry Pi Pico and an SPI OLED Display
# The colors on the SPI bus cable are:
# 3.3v power - red
# SCK - orange
# MISO/Data - yellow
# DC - green
# RESET - blue
# GND - black
# CS - purple

SPI_BUS = 0
SPI_SCL_PIN = 2 # Clock
SPI_SDA_PIN = 3 # labeled SDI(MOSI) on the back of the display
SPI_RESET_PIN = 4 # Reset
SPI_DC_PIN = 5 # Data/command
SPI_CS_PIN = 6 # Chip Select

# OLED Screen Dimensions
DISPLAY_WIDTH=128
DISPLAY_HEIGHT=64
BUTTON_1_PIN = 14 # one up from lower-left corner
BUTTON_2_PIN = 15 # lower left corner with USB on top
BUTTON_3_PIN = 16 # lower left corner with USB on top