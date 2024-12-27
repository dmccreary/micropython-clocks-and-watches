# Strategy for Parts Purchasing Guide

## Breadboards

We strongly suggest purchasing breadboards in bulk at least 10 at a time.

## MicroControllers

We love MicroCenter because they sell the Pico for $4

### Raspberry Pi Pico

### Raspberry Pi Pico W

## Displays

### OLED Displays

Although the small 1" OLED displays work, they are hard to read from a distance.
We like the 2.42" inch OLED displays since they are bright and have a wide viewing angle.

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
