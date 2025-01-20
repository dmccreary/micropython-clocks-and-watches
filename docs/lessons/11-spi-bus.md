# The SPI Bus

The SPI Bus is the fastest serial bus that is used with most microcontrollers.  Although it is fast, most displays need
seven wires to connect a display.  This is in contrast to the I2C bus that only uses four wires.

```python
from machine import Pin, I2C
import ssd1306

SCL=machine.Pin(2) # SPI CLock
SDA=machine.Pin(3) # SPI Data

# configure the SPI bus
# for clocks with 20cm connectors 3MBS is a good choice
spi=machine.SPI(0, sck=SCL, mosi=SDA, baudrate=3_000_000)

RES = machine.Pin(4)
DC = machine.Pin(5)
CS = machine.Pin(6)

# configure the display
disp = ssd1306.SSD1306_SPI(128, 64, spi, DC, RES, CS)
```

The underscore in `3_000_000` is just Python syntax for making large numbers more readable - it's equivalent to writing `3000000`. This is a helpful convention when working with clock speeds and baudrates.

#### SPI Bus
A serial communication interface that operates in a master-slave configuration using separate clock and data lines to synchronize high-speed data transfer between electronic components. 

**Example:** Configuring an SPI bus with a 3 MHz clock rate to drive an OLED display.

#### OLED Display
A self-illuminating electronic visual output device that uses organic light-emitting diodes arranged in a matrix to show text, numbers, or graphics. 

**Example:** A 128x64 pixel monochrome display showing time and temperature readings.

#### Chip Select (CS)
A control signal that activates or deactivates a specific integrated circuit in a system with multiple devices sharing the same communication bus.

**Example:** We can change the state of th CS pin to enable communication with the display while keeping other SPI devices inactive.  This allows you to use a single bus to communicated with multiple displays.

#### Data/Command (DC)
A control line that indicates whether the transmitted information represents display commands or visual data to be shown. 

**Example:** Using Pin 5 to distinguish between instructions for display configuration and pixel data.

#### Reset (RES)
A control signal that returns an electronic device to its initial state, clearing all registers and settings to default values. 

**Example:** You can use the RESET to delay the startup of a display to make sure that the display has powered up in a coherent way and will start
in a consistent state.

#### Clock Line (SCL)
A signal wire that provides timing synchronization pulses to coordinate data transfer between electronic devices. 

**Example:** We use the Clock Line to generate 3 million clock pulses per second for display updates.

#### Data Line (SDA/MOSI)
A signal wire that carries information serially from a controlling device to a receiving device. 

**Example:** We use the SDA pin to transmit display content one bit at a time.

### Tuning the Baudrate

The baudrate parameter determines the transfer between thn microcontroller and the peripheral device.

The baudrate=3_000_000 (3 megabits per second) setting is a reasonable balance for this application.  Digital clock displays are often only updated once per second.

For SPI OLED displays with short connections (~20cm or less), a 3 MHz clock rate provides:

- Reliable data transfer while avoiding signal integrity issues
- Fast enough updates to prevent visible display flicker
- Reliable operation within the SSD1306 controller's specifications

### When Higher Speeds Matter

Simulating an analog clock face on a color watch display will
require a large amount of data being transmitted between the microcontroller and the display.  For these situations you will frequently
keep the wires between the microcontroller and the display short and then turn up the baudrate on the SPI interface.

