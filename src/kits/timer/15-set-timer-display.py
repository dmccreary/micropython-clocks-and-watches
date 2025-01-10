from machine import Pin, SPI, PWM
import ssd1306
from utime import sleep, ticks_ms, ticks_diff, sleep_ms

# Pin definitions (unchanged)
SET_BUTTON = const(13)
INCREMENT_BUTTON = const(14)
DECREMENT_BUTTON = const(15)
PICO_ONBOARD_LED_PIN = 25
SPEAKER_PIN = 10


# Display pins (unchanged)
DISPLAY_SCL_PIN = 2
DISPLAY_SDA_PIN = 3
DISPLAY_RES_PIN = 4
DISPLAY_DC_PIN = 5
DISPLAY_CS_PIN = 6

# Initialize hardware (display, buttons, etc.)
set_pin = Pin(SET_BUTTON, Pin.IN, Pin.PULL_UP)
increment_pin = Pin(INCREMENT_BUTTON, Pin.IN, Pin.PULL_UP)
decrement_pin = Pin(DECREMENT_BUTTON, Pin.IN, Pin.PULL_UP)
led = Pin(PICO_ONBOARD_LED_PIN, Pin.OUT)

speaker = PWM(Pin(SPEAKER_PIN))
MAX_DUTY = 65535
HALF_DUTY = MAX_DUTY // 2

# Display setup
SCL = Pin(DISPLAY_SCL_PIN)
SDA = Pin(DISPLAY_SDA_PIN)
spi = SPI(0, sck=SCL, mosi=SDA)
RES = Pin(DISPLAY_RES_PIN)
DC = Pin(DISPLAY_DC_PIN)
CS = Pin(DISPLAY_CS_PIN)
oled = ssd1306.SSD1306_SPI(128, 64, spi, DC, RES, CS)

# Timer states
STOPPED = const(0)
RUNNING = const(1)
SET_HOURS = const(2)
SET_MINUTES = const(3)
SET_SECONDS = const(4)
timer_state = STOPPED
timer_state_names = ["STOPPED", "RUNNING", "SET_HOURS", "SET_MINUTES", "SET_SECONDS"]

# Timer variables
hours = 0
minutes = 0
seconds = 10
time_remaining = minutes * 60

# Debounce variables
last_set_time = 0
last_increment_time = 0
last_decrement_time = 0
last_blink = 0
DEBOUNCE_MS = 250
BLINK_INTERVAL = 500  # Blink every 500ms
blink_state = False

def update_time_remaining():
    global time_remaining
    time_remaining = hours * 3600 + minutes * 60 + seconds

def set_irq(pin):
    global last_set_time, timer_state
    current_time = ticks_ms()
    if ticks_diff(current_time, last_set_time) > DEBOUNCE_MS:
        last_set_time = current_time
        if timer_state == STOPPED:
            timer_state = SET_HOURS
        elif timer_state == SET_HOURS:
            timer_state = SET_MINUTES
        elif timer_state == SET_MINUTES:
            timer_state = SET_SECONDS
        elif timer_state == SET_SECONDS:
            timer_state = RUNNING
            update_time_remaining()
        elif timer_state == RUNNING:
            timer_state = STOPPED
        print(f'State: {timer_state_names[timer_state]}')

def increment_irq(pin):
    global last_increment_time, hours, minutes, seconds
    current_time = ticks_ms()
    if ticks_diff(current_time, last_increment_time) > DEBOUNCE_MS:
        last_increment_time = current_time
        if timer_state == SET_HOURS:
            hours = (hours + 1) % 24
        elif timer_state == SET_MINUTES:
            minutes = (minutes + 1) % 60
        elif timer_state == SET_SECONDS:
            seconds = (seconds + 1) % 60
        print(f'Time: {hours:02d}:{minutes:02d}:{seconds:02d}')

def decrement_irq(pin):
    global last_decrement_time, hours, minutes, seconds
    current_time = ticks_ms()
    if ticks_diff(current_time, last_decrement_time) > DEBOUNCE_MS:
        last_decrement_time = current_time
        if timer_state == SET_HOURS:
            hours = (hours - 1) % 24
        elif timer_state == SET_MINUTES:
            minutes = (minutes - 1) % 60
        elif timer_state == SET_SECONDS:
            seconds = (seconds - 1) % 60
        print(f'Time: {hours:02d}:{minutes:02d}:{seconds:02d}')

# Set up interrupts
set_pin.irq(trigger=Pin.IRQ_RISING, handler=set_irq)
increment_pin.irq(trigger=Pin.IRQ_FALLING, handler=increment_irq)
decrement_pin.irq(trigger=Pin.IRQ_FALLING, handler=decrement_irq)

def format_time(h, m, s, blink=False, blink_state=False, current_setting=None):
    """Format time with optional blinking for the section being set"""
    if current_setting == SET_HOURS and not blink_state:
        h_str = "  "
    else:
        h_str = f"{h:02d}"
        
    if current_setting == SET_MINUTES and not blink_state:
        m_str = "  "
    else:
        m_str = f"{m:02d}"
        
    if current_setting == SET_SECONDS and not blink_state:
        s_str = "  "
    else:
        s_str = f"{s:02d}"
        
    return f"{h_str}:{m_str}:{s_str}"

# Pleasant frequencies for a pentatonic scale (in Hz)
FREQUENCIES = [262, 330, 392, 523, 659]  # C4, E4, G4, C5, E5

def play_tone(frequency, duration_ms):
    """Play a single tone with the specified frequency and duration."""
    speaker.duty_u16(HALF_DUTY)  # Set volume (0-65535)
    speaker.freq(frequency)
    sleep_ms(duration_ms)
    speaker.duty_u16(0)  # Silent between notes
    sleep_ms(50)  # Brief pause between notes

def stop_alarm():
    """Stop the alarm by turning off the speaker."""
    speaker.duty_u16(0)
    
def play_alarm():
    """Play a repeating pleasant alarm pattern until button is pressed or CTRL-C."""
    print("Alarm started - press button or CTRL-C to stop")
    
    try:
        while True:
            # Check if any button is pressed 
            if not set_pin.value():
                stop_alarm()
                print("Alarm stopped by button")
                break
                
            # Play ascending pattern
            for freq in FREQUENCIES:
                if not set_pin.value():  # Check if any button is pressed between notes
                    break
                play_tone(freq, 150)
                
            # Brief pause between patterns
            sleep_ms(200)
            
            # Play descending pattern
            for freq in reversed(FREQUENCIES[:-1]):  # Skip highest note
                if not set_pin.value():  # Check button between each note
                    break
                play_tone(freq, 150)
                
            sleep_ms(400)  # Longer pause between repetitions
            
    except KeyboardInterrupt:
        stop_alarm()
        print("\nAlarm stopped by CTRL-C")
    finally:
        # Ensure speaker is off no matter how we exit
        stop_alarm()


def format_remaining_time(seconds):
    """Convert total seconds to HH:MM:SS format"""
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:02d}"

def update_screen():
    global blink_state, last_blink
    current_time = ticks_ms()
    
    # Update blink state every BLINK_INTERVAL milliseconds
    if ticks_diff(current_time, last_blink) >= BLINK_INTERVAL:
        blink_state = not blink_state
        last_blink = current_time

    oled.fill(0)
    oled.text("Countdown Timer", 0, 0, 1)
    
    if timer_state in [SET_HOURS, SET_MINUTES, SET_SECONDS]:
        oled.text("Setting Time:", 0, 20, 1)
        time_str = format_time(hours, minutes, seconds, True, blink_state, timer_state)
    else:
        status = "Running" if timer_state == RUNNING else "Stopped"
        oled.text(f"Status: {status}", 0, 20, 1)
        if timer_state == RUNNING:
            time_str = format_remaining_time(time_remaining)
        else:
            time_str = format_time(hours, minutes, seconds)
    
    oled.text(time_str, 0, 40, 1)
    oled.show()

def main():
    global time_remaining
    try:
        while True:
            if timer_state == RUNNING and time_remaining > 0:
                time_remaining -= 1
                if time_remaining == 0:
                    play_alarm()
            update_screen()
            sleep(1)
            
    except KeyboardInterrupt:
        print("\nProgram terminated by user")
        stop_alarm()

if __name__ == "__main__":
    print("Countdown Timer Started")
    print("Press SET to start setting time")
    print("Use INCREMENT/DECREMENT to adjust values")
    main()