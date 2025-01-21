# Play a Tune Using PWM

Below is an example MicroPython program that uses the provided note frequencies and plays the Mario melody on a PWM pin (GPIO 16 in this example). You can adjust timing and duty cycle to get the sound you want. Simply copy this code onto your MicroPython device (e.g., Raspberry Pi Pico running MicroPython) and run it.

```python
from machine import Pin, PWM
from utime import sleep

# Initialize speaker on GPIO16
speaker = PWM(Pin(16))

# Define the tone (note) frequency dictionary
tones = {
    "B0": 31,"C1": 33,"CS1": 35,"D1": 37,"DS1": 39,"E1": 41,"F1": 44,"FS1": 46,
    "G1": 49,"GS1": 52,"A1": 55,"AS1": 58,"B1": 62,"C2": 65,
    "CS2": 69,"D2": 73,"DS2": 78,"E2": 82,"F2": 87,"FS2": 93,"G2": 98,
    "GS2": 104,"A2": 110,"AS2": 117,"B2": 123,"C3": 131,"CS3": 139,
    "D3": 147,"DS3": 156,"E3": 165,"F3": 175,"FS3": 185,
    "G3": 196,"GS3": 208,"A3": 220,"AS3": 233,"B3": 247,"C4": 262,"CS4": 277,"D4": 294,"DS4": 311,
    "E4": 330,"F4": 349,"FS4": 370,"G4": 392,"GS4": 415,"A4": 440,"AS4": 466,"B4": 494,"C5": 523,"CS5": 554,"D5": 587,"DS5": 622,"E5": 659,"F5": 698,
    "FS5": 740,"G5": 784,"GS5": 831,"A5": 880,"AS5": 932,"B5": 988,"C6": 1047,"CS6": 1109,"D6": 1175,"DS6": 1245,"E6": 1319,"F6": 1397,"FS6": 1480,"G6": 1568,"GS6": 1661,
    "A6": 1760,"AS6": 1865,"B6": 1976,"C7": 2093,"CS7": 2217,"D7": 2349,"DS7": 2489,"E7": 2637,"F7": 2794,"FS7": 2960,"G7": 3136,"GS7": 3322,"A7": 3520,
    "AS7": 3729,"B7": 3951,"C8": 4186,"CS8": 4435,"D8": 4699,"DS8": 4978
}

# Mario melody notes
mario = [
    "E7", "E7", 0, "E7", 0, "C7", "E7", 0, "G7", 0, 0, 0, "G6", 0, 0, 0,
    "C7", 0, 0, "G6", 0, 0, "E6", 0, 0, "A6", 0, "B6", 0, "AS6", "A6", 0,
    "G6", "E7", 0, "G7", "A7", 0, "F7", "G7", 0, "E7", 0, "C7", "D7", "B6", 0, 0,
    "C7", 0, 0, "G6", 0, 0, "E6", 0, 0, "A6", 0, "B6", 0, "AS6", "A6", 0,
    "G6", "E7", 0, "G7", "A7", 0, "F7", "G7", 0, "E7", 0, "C7", "D7", "B6", 0, 0
]

def play_tone(note, duration=0.15):
    """
    Plays a single tone for the specified duration.
    If note is 0, it is treated as a rest (no sound).
    Adjust durations as needed for the best result.
    """
    if note == 0:
        # Rest (no sound)
        speaker.duty_u16(0)
        sleep(duration)
    else:
        # Play the specified note
        freq = tones[note]
        speaker.freq(freq)
        # Set a duty cycle (volume), 0 to 65535
        speaker.duty_u16(30000)
        sleep(duration)
        # Turn the sound off between notes
        speaker.duty_u16(0)
        sleep(0.05)

# Play the entire Mario melody
for n in mario:
    play_tone(n)

# Turn speaker off at the end
# Note that the note still plays on stop/interrupt!
speaker.duty_u16(0)
```

## Adjust the Tempo

```
duration=0.15
```

## Adding Interrupt Handling

```python
# Main execution
try:
    print("Playing Mario theme...")
    play_mario()
    # Clean up
    speaker.deinit()
    print("Done!")
except KeyboardInterrupt:
    # Clean up if interrupted
    speaker.deinit()
    print("\nStopped by user")
```

```python
from machine import Pin, PWM
from utime import sleep_ms

# Initialize speaker on GPIO 16
speaker = PWM(Pin(16))

# Note frequencies in Hz
tones = {
    "B0": 31, "C1": 33, "CS1": 35, "D1": 37, "DS1": 39, "E1": 41, "F1": 44, "FS1": 46,
    "G1": 49, "GS1": 52, "A1": 55, "AS1": 58, "B1": 62, "C2": 65,
    "CS2": 69, "D2": 73, "DS2": 78, "E2": 82, "F2": 87, "FS2": 93, "G2": 98,
    "GS2": 104, "A2": 110, "AS2": 117, "B2": 123, "C3": 131, "CS3": 139,
    "D3": 147, "DS3": 156, "E3": 165, "F3": 175, "FS3": 185,
    "G3": 196, "GS3": 208, "A3": 220, "AS3": 233, "B3": 247, "C4": 262, "CS4": 277, "D4": 294, "DS4": 311,
    "E4": 330, "F4": 349, "FS4": 370, "G4": 392, "GS4": 415, "A4": 440, "AS4": 466, "B4": 494, "C5": 523, "CS5": 554, "D5": 587, "DS5": 622, "E5": 659, "F5": 698,
    "FS5": 740, "G5": 784, "GS5": 831, "A5": 880, "AS5": 932, "B5": 988, "C6": 1047, "CS6": 1109, "D6": 1175, "DS6": 1245, "E6": 1319, "F6": 1397, "FS6": 1480, "G6": 1568, "GS6": 1661,
    "A6": 1760, "AS6": 1865, "B6": 1976, "C7": 2093, "CS7": 2217, "D7": 2349, "DS7": 2489, "E7": 2637, "F7": 2794, "FS7": 2960, "G7": 3136, "GS7": 3322, "A7": 3520,
    "AS7": 3729, "B7": 3951, "C8": 4186, "CS8": 4435, "D8": 4699, "DS8": 4978
}

mario = ["E7", "E7", 0, "E7", 0, "C7", "E7", 0, "G7", 0, 0, 0, "G6", 0, 0, 0, "C7", 0, 0, "G6",
         0, 0, "E6", 0, 0, "A6", 0, "B6", 0, "AS6", "A6", 0, "G6", "E7", 0, "G7", "A7", 0, "F7", "G7",
         0, "E7", 0, "C7", "D7", "B6", 0, 0, "C7", 0, 0, "G6", 0, 0, "E6", 0, 0, "A6", 0, "B6", 0,
         "AS6", "A6", 0, "G6", "E7", 0, "G7", "A7", 0, "F7", "G7", 0, "E7", 0, "C7", "D7", "B6", 0, 0]

def play_tone(frequency, duration=100):
    """Play a tone at the given frequency for the specified duration"""
    if frequency > 0:
        speaker.freq(frequency)  # Set frequency
        speaker.duty_u16(32768)  # 50% duty cycle (32768 is half of 65535)
        sleep_ms(duration)
        speaker.duty_u16(0)     # Turn off tone
    else:
        sleep_ms(duration)      # Rest for the specified duration

def play_mario():
    """Play the Mario theme song"""
    # Tempo control
    tempo = 150  # Adjust this value to control speed (lower = faster)
    
    # Play each note
    for note in mario:
        if note == 0:
            # Rest
            play_tone(0, tempo)
        else:
            # Play the note
            play_tone(tones[note], tempo)
        
        # Brief pause between notes to separate them
        sleep_ms(50)

# Main execution
try:
    print("Playing Mario theme...")
    play_mario()
    # Clean up
    speaker.deinit()
    print("Done!")
except KeyboardInterrupt:
    # Clean up if interrupted
    speaker.deinit()
    print("\nStopped by user")
```