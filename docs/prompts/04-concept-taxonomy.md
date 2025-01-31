# Concept Taxonomy

!!! prompt
    Given the concepts below, our next step is to create a 10-element taxonomy
    of these concepts for the book "Building Clocks and Watches with MicroPython".

    Your task is to organize these concepts into a taxonomy by grouping similar Concepts into one of ten categories. Each category should include concepts
    that share similar characteristics, functions, or applications.

    Please suggest 10 categories for the taxonomy.  Attempt to
    create categories that evenly distribute the concepts so that
    each category has a similar number of concepts in it.

    Ensure that the categories cover
    a range of concept types, including abstract ideas, practical
    applications, common misunderstandings, and real-world examples.
    Avoid redundancy and ensure that each category is distinct.

    You can use "Foundational Concepts" as your first category.
    You can use "Terms and Definitions" as a second category.
    You can use "Example Projects" as a 10th category.

## ChatGPT o1 Response

Thought about taxonomy for course concepts for 2m 17s

Below is **one possible** 10‑category taxonomy that groups these 115 concepts into roughly even clusters. Each category highlights a distinct thematic area, from foundational ideas through advanced techniques and ending with example "capstone‑style" projects. Feel free to adjust or rename categories as needed for your curriculum goals.

### Category 1: **Foundational Concepts**

These are the most basic building blocks and hardware essentials on which everything else depends.

1.  (0) Timekeeping Components
2.  (1) MicroPython
3.  (2) Raspberry Pi Pico W
4.  (3) Breadboard
5.  (4) Power
6.  (5) USB Power
7.  (6) Battery Power
8.  (7) Battery Backup
9.  (8) Battery Drain Calculation
10.  (10) Real-time Clocks
11.  (11) The Thonny IDE
12.  (91) Hardware Documentation

### Category 2: Terms & Definitions

Core programming syntax and "must-know" terminology used throughout the course.

1.  (13) The localtime() Function
2.  (14) MicroPython Syntax
3.  (15) Loops
4.  (16) Conditionals
5.  (17) Functions
6.  (18) Libraries
7.  (20) Printing Time to the Console
8.  (34) Using 16 Bits to Represent Color
9.  (93) Using math Module for Geometry
10.  (94) Time Zones & UTC Offsets
11.  (95) Daylight Saving Time
12.  (101) Converting Between datetime Objects and Timestamps

### Category 3: Displays

An overview of the different display types you might use in clocks/watches.

1.  (9) LED Clock Displays
2.  (21) Displays
3.  (32) OLED Displays
4.  (33) Smartwatch Displays
5.  (53) Creating a 7-Segment Style Digital Display
6.  (54) Custom Segment-Based Displays
7.  (75) Using E-Paper Displays
8.  (76) Partial Refresh on E-Paper
9.  (77) Techniques to Minimize Ghosting on E-Paper
10.  (78) Using TFT Displays (e.g., ST7735, ILI9341)
11.  (79) Comparing Display Technologies
12.  (103) Implementing Clock Themes

### Category 4: Basic Drawing & Font Tools

Fundamental graphics APIs and driver-loading concepts.

1.  (19) Loading MicroPython Drivers
2.  (22) Drawing Lines
3.  (23) Drawing Text
4.  (24) Drawing Pixels
5.  (25) Drawing Rectangles
6.  (26) Drawing Circles
7.  (27) Drawing Ellipses
8.  (28) Drawing Arcs
9.  (29) Drawing Polygons
10.  (30) Changing Fonts
11.  (31) Using MicroPython Drivers
12.  (43) Loading Custom Fonts

### Category 5: Advanced Graphics & Animations

More complex graphics techniques and math-based rendering.

1.  (35) Framebuffer in MicroPython
2.  (39) Drawing Hands on an Analog Clock
3.  (40) Using math.sin() and math.cos()
4.  (41) Drawing Tick Marks on a Watch Face
5.  (42) Drawing Numbers on a Watch Face
6.  (80) Color Animations on Watch Faces
7.  (81) Flicker Reduction Techniques
8.  (82) Double Buffering for Smooth Animations
9.  (104) Fast Redraw Techniques (Blitting)
10.  (105) Partial Screen Updates for Watch Faces
11.  (106) Color Conversion & Palettes in MicroPython
12.  (83) Using the micropython-ufont Library

### Category 6: Graphics, Asynchronous, & Concurrency

All about getting time from the internet, using Wi-Fi, and handling multiple tasks.

1.  (12) Synchronizing Time from the PC
2.  (45) Using Internal Timers on the Raspberry Pi Pico
3.  (48) Network Time Synchronization (NTP)
4.  (49) Setting Up WiFi on the Pico W
5.  (50) Working the network module
6.  (51) Parsing JSON
7.  (65) Timer-Based Events
8.  (84) Asynchronous Code with uasyncio
9.  (85) Time-Based Tasks with uasyncio
10.  (86) Handling Concurrency of Time Updates & UI
11.  (108) WiFi-Based Weather & Forecast Updates
12.  (114) World Clocks

#### Category 7: Sensors & Modules

External hardware modules, from RTC chips to accelerometers and I²C sensors.

1.  (46) External RTC Modules (DS1307, DS3231)
2.  (47) Setting the System Clock from an External RTC
3.  (69) Integrating External Sensors
4.  (70) Temperature and Humidity
5.  (71) Displaying Sensor Data
6.  (72) Accelerometers for Orientation
7.  (73) Tilt-Based Wake for Watch Display
8.  (98) Using I²C Sensors & Modules
9.  (109) Using Sensors for Step Counting (Pedometer)
10.  (110) Adding a LiPo Charging Circuit
11.  (90) Tools for Measuring Battery Usage
12.  (100) Servo Motors for Mechanical Pointers

### Category 8: User Input & Time Functions

Handling buttons, debouncing, rotary encoders, and time-related features.

1.  (52) Displaying Date and Day of Week
2.  (57) Setting Time with Buttons
3.  (58) Using Interrupts for Button Input
4.  (59) Button Debouncing Techniques
5.  (60) Using A Rotary Encoder
6.  (61) Setting Alarms with the RTC
7.  (96) Using the Built-In Filesystem on Pico
8.  (97) Logging Time Data to an SD Card
9.  (74) Ultra-Low Power
10.  (99) Menu Systems for Watch Settings
11.  (107) Handling 12-Hour vs. 24-Hour Formats
12.  (111) Chronograph Functionality

### Category 9: **Audio & Power Management**

Generating sounds, mechanical movements, and minimizing power consumption.

1.  (62) Connecting Speakers
2.  (63) Playing a Sound
3.  (64) Sound Encoding
4.  (66) Playing Chimes
5.  (67) Cuckoo Clocks
6.  (68) Generating Beep or Alarm Tones
7.  (102) Generating Waveforms for Audio
8.  (55) Minimizing Power Consumption (Sleep Modes)
9.  (56) Waking from Deep Sleep on RTC Alarm
10.  (89) Sleep Scheduling
11.  (87) Using a Watchdog Timer for Reliability
12.  (88) Logging & Debugging Time Issues

### Category 10: Example Projects

A set of "capstone" or real-world style projects/enhancements.

1.  (92) 3D Printing Watch Enclosures
2.  (100) *\[If not placed elsewhere --- but here we used 100 in Category 7, so you can swap if you prefer\]*
3.  (103) *\[If not used in Displays\]*
4.  (112) Timer Project
5.  (113) Stopwatch Project
6.  (109) *\[If not in Sensors\]*
7.  (99) *\[If not in User Input\]*
8.  ( ... )

Depending on how you ultimately shuffle things around, you can populate this "Example Projects" category with any concepts that serve well as culminating projects---for example, "Cuckoo Clocks," "Playing Chimes," "Implementing Clock Themes," "Using Sensors for Step Counting," or "Servo Motors for Mechanical Pointers."

### Final Notes

1.  **Balancing the Categories**

    -   Each category has ~11--12 items (with minor adjustments possible).
    -   Some concepts (e.g., "Servo Motors," "Implementing Clock Themes," or "Cuckoo Clocks") could fit either under a main topic (like "Sensors & Modules" or "Audio & Power") **or** under "Example Projects," depending on whether you treat them as discrete lessons or culminating builds.
2.  **Avoiding Duplication**

In a real curriculum, certain topics (e.g., "External RTC Modules" vs. "Setting Alarms with the RTC") might overlap across multiple categories. To keep it simple, each concept is listed once here.

3.  **Adapt as Needed**

This taxonomy is a **starting point**. You may decide to rename categories (e.g., split "Audio & Power Management" into two) or move individual concepts around to best match your teaching flow.

By defining these ten thematic groupings, you'll have a clear roadmap for both the **sequence of lessons** and the **range of coverage** in "Building Clocks and Watches with MicroPython."

[Clock and Watches](./clocks-and-watches.csv)