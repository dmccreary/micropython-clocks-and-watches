# Hardware configuration file for ST7735 clock

SPI_BUS = 0
SPI_SCL_PIN = 2 # Clock
SPI_SDA_PIN = 3 # labeled SDI(MOSI) on the back of the display
SPI_RESET_PIN = 4 # Reset
SPI_DC_PIN = 5 # Data/command
SPI_CS_PIN = 6 # Chip Select

# OLED Screen Dimensions
DISPLAY_WIDTH=160
DISPLAY_HEIGHT=128
DISPLAY_ROTATION = 1
# use builtin pullups
MODE_PIN = 14 # one up from lower-left corner
INCREMENT_PIN = 15 # lower left corner with USB on top
DECREMENT_PIN = 16 # lower left corner with USB on top