from machine import Pin, SPI
import utime
import ssd1306
from mp_button import Button
from utime import sleep, localtime

# HARDWARE PIN CONFIGURATION
# LEDs
PICO_ONBOARD_LED_PIN = 25
# Button pins
STOPWATCH_START_STOP_PIN = 14
STOPWATCH_RESET_PIN = 15
# Display pins
DISPLAY_SCL_PIN = 2
DISPLAY_SDA_PIN = 3
DISPLAY_RES_PIN = 4
DISPLAY_DC_PIN = 5
DISPLAY_CS_PIN = 6

led = machine.Pin(PICO_ONBOARD_LED_PIN, machine.Pin.OUT)

SCL=Pin(DISPLAY_SCL_PIN)
SDA=Pin(DISPLAY_SDA_PIN)
spi=SPI(0, sck=SCL, mosi=SDA)
RES = Pin(DISPLAY_RES_PIN)
DC = Pin(DISPLAY_DC_PIN)
CS = machine.Pin(DISPLAY_CS_PIN)
oled = ssd1306.SSD1306_SPI(128, 64, spi, DC, RES, CS)

def update_screen(seconds):
    oled.fill(0)
    oled.text("stopwatch lab", 0, 0, 1)
    oled.text(str(counter), 0, 10, 1)
    oled.show()

counter = 0
while True:
    update_screen(counter)
    print(counter)
    led.toggle()
    sleep(.5)
    counter += 1