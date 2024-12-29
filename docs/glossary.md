# Glossary of Terms DIY Clocks and Watches with MicroPython

#### Abstraction
A technique for managing complexity by hiding unnecessary details while keeping essential features visible. 

**Example:** Using a `display_time()` function that accepts hours and minutes without needing to know how individual LED segments are controlled.

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

#### DS1307

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

#### 3D Printing Watch Enclosures
A process of creating custom protective cases for watch components using additive manufacturing technology.

#### Accelerometer
A sensor that measures physical acceleration and orientation, useful for tilt-based display activation.

**Example:** Detecting when a user lifts their wrist to view the watch face.

#### Alarm
A scheduled alert that triggers audio, visual, or vibration notifications at specific times.

**Example:** Setting multiple daily alarms using the RTC module.

#### Analog Clock Face
A traditional clock display using rotating hands to show time on a circular dial.

**Example:** Drawing hour and minute hands using `math.sin()` and `math.cos()` for position calculations.

#### Animation
The process of creating movement by rapidly updating display contents.

**Example:** Smoothly rotating second hands or creating blinking colons between hours and minutes.

#### Asynchronous Programming
A coding technique that allows multiple tasks to run concurrently without blocking each other.

**Example:** Using `uasyncio` to handle display updates while monitoring button presses.

#### Battery Backup
A power system that maintains time and settings when main power is disconnected.

#### Battery Power
Portable electrical energy storage used to operate mobile timepieces.

**Example:** Calculating power consumption to estimate battery life.

#### Blitting
A technique for rapidly copying rectangular portions of memory to update displays efficiently.

**Example:** Using framebuffer operations to reduce screen flicker.

#### Chronograph
A timepiece with both timekeeping and stopwatch capabilities.

#### Color Depth
The number of bits used to represent colors in a display.

**Example:** Using 16 bits per pixel to show 65,536 different colors.

#### Concurrency
The ability to handle multiple tasks or events simultaneously in a program.

**Example:** Updating the display while checking for button presses.

#### Conditionals
Programming statements that perform different actions based on whether a condition is true or false.

**Example:** Switching between 12-hour and 24-hour time formats.

#### Custom Font
A specialized set of character designs loaded into memory for display purposes.

**Example:** Loading compact number fonts using the micropython-ufont library.

#### Daylight Saving Time
A seasonal time adjustment typically involving a one-hour shift.

**Example:** Automatically adjusting clock time based on DST rules.

#### Deep Sleep
A low-power mode that disables most system functions to conserve energy.

**Example:** Entering sleep mode when the watch face isn't being viewed.

#### Display Driver
Software that controls how information is shown on a specific type of display.

**Example:** Using the ST7735 driver for TFT LCD screens.

#### Double Buffering
A technique using two memory areas to prepare the next frame while displaying the current one.

**Example:** Creating smooth animations without visible drawing operations.

#### E-Paper Display
A low-power screen technology that maintains its image without constant power.

**Example:** Using partial updates to change only modified portions of the display.

#### External RTC
A separate timekeeping chip that maintains accurate time independent of the main processor.

**Example:** Using a DS3231 module for precise timekeeping.

#### Filesystem
A system for storing and organizing files on the microcontroller.

**Example:** Saving configuration settings and logs to internal storage.

#### Framebuffer
A region of memory that holds the complete contents of a display.

**Example:** Modifying pixel data before updating the screen.

#### Functions
Reusable blocks of code that perform specific tasks.

**Example:** Creating a function to convert between 12-hour and 24-hour formats.

#### Ghosting
A visual artifact where previous images remain partially visible on certain display types.

**Example:** Using display clearing techniques on e-paper screens.

#### I2C Sensors
Digital components that communicate using the I2C protocol to provide measurements.

**Example:** Reading temperature and humidity data for weather display.

#### Interrupt
A signal that temporarily pauses normal program execution to handle important events.

**Example:** Responding immediately to button presses.

#### JSON
A text-based data format commonly used for exchanging information with web services.

**Example:** Parsing weather data from online APIs.

#### Libraries
Collections of pre-written code that provide useful functions and features.

**Example:** Using the `math` module for trigonometric calculations.

#### LiPo Charging
The process of safely recharging Lithium Polymer batteries.

**Example:** Implementing USB charging circuits with protection features.

#### Logging
The practice of recording program events and data for debugging or analysis.

**Example:** Saving timing discrepancies to investigate accuracy issues.

#### Loops
Programming structures that repeat code blocks multiple times.

**Example:** Continuously updating the display every second.

#### Math Module
A collection of mathematical functions for complex calculations.

**Example:** Using trigonometry to position clock hands.

#### Menu System
An interface allowing users to navigate options and settings.

**Example:** Creating hierarchical settings menus for watch configuration.

#### Network Time Protocol (NTP)
A method for synchronizing time over the internet.

**Example:** Updating the RTC from online time servers.

#### Partial Refresh
Updating only changed portions of a display to improve efficiency.

**Example:** Refreshing only the seconds digits each update.

#### Pedometer
A feature that counts steps using motion sensor data.

**Example:** Calculating daily step counts from accelerometer readings.

#### Power Management
Techniques for minimizing and controlling energy consumption.

**Example:** Using sleep modes and efficient display updates.

#### PWM Audio
Using Pulse Width Modulation to generate sounds and tones.

**Example:** Creating alarm beeps and hourly chimes.

#### Rotary Encoder
A input device that converts rotational movement into digital signals.

**Example:** Using encoder rotation to adjust time settings.

#### Screen Update
The process of refreshing display contents to show new information.

**Example:** Efficiently updating only changed portions of the time display.

#### Servo Motor
An actuator that can rotate to precise positions.

**Example:** Moving physical clock hands on a hybrid display.

#### Sleep Mode
A low-power state that reduces energy consumption.

**Example:** Entering deep sleep between display updates.

#### SPI Interface
A high-speed serial communication protocol for connecting displays and sensors.

**Example:** Transferring data to TFT displays efficiently.

#### Temperature Sensor
A component that measures ambient temperature.

**Example:** Displaying current temperature alongside time.

#### Thonny IDE
An integrated development environment optimized for MicroPython programming.

**Example:** Using Thonny to upload code and debug timing issues.

#### Time Zone
A region that observes a uniform standard time.

**Example:** Converting between local time and UTC.

#### Timer
A system resource that generates regular time-based events.

**Example:** Creating precise one-second update intervals.

#### UTC
Coordinated Universal Time, the primary time standard for global time coordination.

**Example:** Converting local time to UTC for synchronization.

#### Watchdog Timer
A hardware feature that resets the system if the program stops responding.

**Example:** Ensuring reliability in long-running clock applications.

#### Weather Updates
Real-time weather information obtained through internet services.

**Example:** Displaying temperature and forecast alongside time.

#### Wi-Fi Module
Hardware that enables wireless network connectivity.

**Example:** Connecting to the internet for time synchronization.

#### World Clock
A timepiece that displays times for multiple time zones simultaneously.

**Example:** Showing local time alongside other major cities' times.