from machine import Pin, PWM
from utime import sleep_ms

# Constants for pins
SPEAKER_PIN = 10  # Speaker on GPIO 16
STOP_BUTTON_PIN = 17  # Stop button on GPIO 17
MAX_DUTY = 65535
HALF_DUTY = MAX_DUTY // 2

# Create PWM object for speaker
speaker = PWM(Pin(SPEAKER_PIN))

# Create stop button with pull-up resistor
stop_button = Pin(STOP_BUTTON_PIN, Pin.IN, Pin.PULL_UP)

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
            # Check if button is pressed (active low due to pull-up)
            if not stop_button.value():
                stop_alarm()
                print("Alarm stopped by button")
                break
                
            # Play ascending pattern
            for freq in FREQUENCIES:
                if not stop_button.value():  # Check button between each note
                    break
                play_tone(freq, 150)
                
            # Brief pause between patterns
            sleep_ms(200)
            
            # Play descending pattern
            for freq in reversed(FREQUENCIES[:-1]):  # Skip highest note
                if not stop_button.value():  # Check button between each note
                    break
                play_tone(freq, 150)
                
            sleep_ms(400)  # Longer pause between repetitions
            
    except KeyboardInterrupt:
        stop_alarm()
        print("\nAlarm stopped by CTRL-C")
    finally:
        # Ensure speaker is off no matter how we exit
        stop_alarm()

# Optional test code
if __name__ == "__main__":
    try:
        print("Press button or CTRL-C to stop alarm when it starts")
        sleep_ms(2000)  # Wait 2 seconds before starting
        play_alarm()
    except KeyboardInterrupt:
        print("\nProgram terminated by user")
    finally:
        stop_alarm()  # Always ensure speaker is off when exiting