# Parts Purchasing Guide

## Breadboards

## MicroControllers

### Raspberry Pi Pico

### Raspberry Pi Pico W

## Displays

### OLED Displays

### SmartWatch Displays

[Waveshare RP2040-LCD-1.28](https://www.waveshare.com/wiki/RP2040-LCD-1.28)

[Ebay Listing for $21](https://www.ebay.com/itm/265865445423)

### LED Strips

## Smartwatch Displays

## Real-Time Clock Boards

### The DS1307

Although this board is old, it is a simple and low-cost part that is easy to use.
Most of the development boards come with their own crystal and an I2C interface.

### The DS3231
The DS3231 is one of the most commonly used real-time clock (RTC) modules paired with microcontrollers like the Raspberry Pi Pico. It's popular because it:

1. Has high accuracy (temperature-compensated crystal oscillator)
2. Maintains accuracy over a wide temperature range
3. Has built-in temperature compensation
4. Uses the I2C interface, which is easy to implement
5. Includes a battery backup option
6. Is relatively inexpensive
7. Has extensive library support across different platforms

The second most common is probably the DS1307, which is an older and simpler version. While less accurate than the DS3231, it's even less expensive and still perfectly suitable for many basic timekeeping applications.

For microcontrollers in particular, the DS3231 tends to be favored because its accuracy doesn't depend on the microcontroller's clock, and it maintains accurate time even when the main microcontroller is reset or loses power.

Since this is quite specific technical information and while I believe this is accurate, you may want to verify these details, particularly regarding current market availability and relative popularity.
