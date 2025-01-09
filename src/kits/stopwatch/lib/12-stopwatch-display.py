from mp_button import Button
from machine import Pin, SPI
import ssd1306
from utime import sleep, ticks_ms, ticks_diff

# lower right corner - button closes path to GND
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

# configure the pins
start_stop_pin = Pin(STOPWATCH_START_STOP_PIN, Pin.IN, Pin.PULL_UP)
reset_pin = Pin(STOPWATCH_RESET_PIN, Pin.IN, Pin.PULL_UP)

led = machine.Pin(PICO_ONBOARD_LED_PIN, machine.Pin.OUT)

SCL=Pin(DISPLAY_SCL_PIN)
SDA=Pin(DISPLAY_SDA_PIN)
spi=SPI(0, sck=SCL, mosi=SDA)
RES = Pin(DISPLAY_RES_PIN)
DC = Pin(DISPLAY_DC_PIN)
CS = machine.Pin(DISPLAY_CS_PIN)
oled = ssd1306.SSD1306_SPI(128, 64, spi, DC, RES, CS)

# Global variables
STOPPED = const(0)
RUNNING = const(1)
stopwatch_state = STOPPED
stopwatch_starttime = 0
stopwatch_elapsed_time = 0  # Renamed from stopwatch_resume_time for clarity
last_start_stop_press = 0
last_reset_press = 0
DEBOUNCE_MS = 250

def start_stop_irq(pin):
    global last_start_stop_press, stopwatch_state, stopwatch_starttime, stopwatch_elapsed_time
    current_time = ticks_ms()
    if ticks_diff(current_time, last_start_stop_press) > DEBOUNCE_MS:
        last_start_stop_press = current_time
        
        if stopwatch_state == STOPPED:
            stopwatch_state = RUNNING
            stopwatch_starttime = ticks_ms()
        else:
            # Calculate the time elapsed since last start
            stopwatch_elapsed_time += ticks_diff(ticks_ms(), stopwatch_starttime)
            stopwatch_state = STOPPED

def reset_irq(pin):
    global last_reset_press, stopwatch_state, stopwatch_elapsed_time
    current_time = ticks_ms()
    if ticks_diff(current_time, last_reset_press) > DEBOUNCE_MS:
        last_reset_press = current_time
        stopwatch_state = STOPPED
        stopwatch_elapsed_time = 0

# Here are the Interupt handlers
start_stop_pin.irq(trigger=Pin.IRQ_RISING, handler=start_stop_irq)
reset_pin.irq(trigger=Pin.IRQ_FALLING, handler=reset_irq)


def format_time(milliseconds):
    """Convert milliseconds to formatted time string (MM:SS.mmm)"""
    seconds = milliseconds // 1000
    ms = milliseconds % 1000
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02d}:{seconds:02d}.{ms:03d}"

def update_screen(state, elapsed_time):
    global stopwatch_starttime
    oled.fill(0)
    oled.text("stopwatch lab", 0, 0, 1)
    state_text = "RUNNING" if state == RUNNING else "STOPPED"
    oled.text(state_text, 0, 20, 1)
    
    if state == RUNNING:
        current_time = elapsed_time + ticks_diff(ticks_ms(), stopwatch_starttime)
        oled.text(format_time(current_time), 0, 40, 1)
    else:
        oled.text(format_time(elapsed_time), 0, 40, 1)
    oled.show()

# Main loop
while True:
    update_screen(stopwatch_state, stopwatch_elapsed_time)
    sleep(0.1)