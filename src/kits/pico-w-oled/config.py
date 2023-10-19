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
SCL_PIN = 2 # Clock
SDA_PIN = 3 # labeled SDI(MOSI) on the back of the display
RESET_PIN = 4 # Reset
DC_PIN = 5 # Data/command
CS_PIN = 6 # Chip Select

# OLED Screen Dimensions
WIDTH=128
HEIGHT=64
