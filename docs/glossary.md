# Glossary of Terms DIY Clocks and Watches with MicroPython

#### Abstraction
A technique for managing complexity by hiding unnecessary details while keeping essential features visible. 

**Example:** Using a display_time() function that accepts hours and minutes without needing to know how individual LED segments are controlled.

#### Breadboard
A reusable plastic board with holes and internal connections for prototyping electronic circuits without soldering.

**Example:** Connecting LED displays and buttons to the Pico W using jumper wires on a breadboard.

#### Button Debouncing
A technique to prevent false button readings caused by mechanical switch contacts bouncing when pressed or released.

**Example:** `debounce_time = 100` in button configuration prevents multiple accidental triggers.

#### Callback Function
A function passed as an argument to another function, which will be executed when a specific event occurs.

**Example:** `button_mode_irq` function that runs whenever the mode button is pressed.

#### Digital Display
An electronic output device that shows numbers, letters, or symbols using discrete segments or pixels.

**Example:** Four-digit seven-segment LED display showing hours and minutes.

#### DS1307 Display

#### Event Handler
A function that responds to specific occurrences like button presses or timer updates.

**Example:** The `button_mode_irq` function handles mode button press events.

#### GPIO Pin
General Purpose Input/Output connection on a microcontroller that can be programmed to send or receive electrical signals.

**Example:** Using GPIO pin 16 for the mode button: `mode_pin = Pin(16, Pin.IN, Pin.PULL_UP)`

#### I2C
A communication protocol that allows multiple digital components to exchange data using just two wires plus power and ground.

#### Interrupt
A signal that causes the microcontroller to pause its current task and handle a high-priority event.

#### LED Matrix
An array of light-emitting diodes arranged in rows and columns that can display patterns, numbers, or text.

#### MicroPython
A streamlined version of Python programming language designed to run on microcontrollers and embedded systems.

#### OLED Display
A thin, bright display that uses organic light-emitting diodes to show text and graphics without a backlight.

#### Pin
A metal connector on electronic components that carries electrical signals or power.

#### Pull-up Resistor
An electronic component that ensures a consistent voltage level on input pins when buttons or switches are not pressed.

**Example:** Using internal pull-up resistors with `Pin.PULL_UP` for button inputs.

#### PWM
Pulse Width Modulation - a technique for creating varying levels of brightness or speed by rapidly switching a signal on and off.

#### Raspberry Pi Pico W
A small, low-cost microcontroller board with built-in wireless capabilities, designed for learning and DIY projects.

#### Real-Time Clock (RTC)
A specialized chip or circuit that keeps accurate time even when main power is removed.

**Example:** Using the RTC module to maintain accurate time: `rtc = RTC()`

#### Seven-Segment Display
A display made of seven LED segments plus a decimal point that can show numbers and some letters.

**Example:** Creating patterns for digits using segments 'a' through 'g': `SEGMENTS = {'a': 4, 'b': 3, 'c': 2, 'd': 7, 'e': 6, 'f': 5, 'g': 1}`

#### Shift Register
An integrated circuit that converts serial data into parallel outputs, useful for controlling multiple LEDs with fewer pins.

**Example:** Using SR74HC595 shift register to control display segments.

#### SPI
Serial Peripheral Interface - a fast communication protocol for connecting digital components using multiple signal lines.

#### State Machine
A programming concept where a system can be in one of several defined states, with specific rules for transitioning between them.

**Example:** Clock modes including "run", "set hour", "set minute", and "set AM/PM".

#### USB Power
A 5-volt power source available through Universal Serial Bus connections, commonly used for powering small electronic projects.

#### Web Services
Online resources that provide data or functionality through standard internet protocols.

**Example:** Fetching current time from an internet time server for clock synchronization.
