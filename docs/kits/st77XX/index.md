# Building a Clock with the Color ST7735 and ST7789 Displays

![Ebay Listing](./ebay-listing.png)

[Sample Listing on eBay for $3-4](https://www.ebay.com/itm/405396699577)

This clock is built on a low-cost 1.8 inch color TFT display.
It has a resolution of 160x128 which is enough to draw date, time
and temperature information.  It has an SPI interfaces and
runs on 3.3 volts.

## Interface

1. Ground
2. VCC Power input
3. SCL SPI clock input
4. SDA SPI data input
5. RES Reset
6. DC data/command selection foot
7. CS chip selection signal,low level active
8. BLK - Backlight - Must be at 3.3v to see the device. This can also
be used to dim the display.

## Driver

**Supported Resolutions:** 320x240, 240x240, 135x240 and 128x128 pixel displays

[Russ Hughes Binary Driver](https://github.com/russhughes/st7789_mpy)

## Compare

Let's compare these two common display driver ICs used in small color LCD displays.

Key Differences:

Resolution and Display Size:

- ST7735: Typically supports up to 128x160 pixels, commonly used in 1.8" displays
- ST7789: Supports up to 240x320 pixels, commonly used in 1.3" to 2.0" displays

Memory and Color Depth:

- ST7735: Has 132x162 display RAM, supports 16-bit (65K) colors
- ST7789: Has 240x320 display RAM, supports 16-bit (65K) and 18-bit (262K) colors

Power and Performance:

- ST7735: Lower power consumption, suitable for battery-operated devices
- ST7789: Higher refresh rates possible, better performance for animations

Common Features:

- Both use 4-wire SPI interface for communication
- Both support hardware scrolling
- Similar command sets, making code migration relatively straightforward
- Built-in display RAM
- Support sleep modes for power saving

In terms of practical use:

- ST7735 is often chosen for simpler projects where power efficiency is crucial
- ST7789 is preferred when higher resolution or better color reproduction is needed
- Both are well-supported in popular microcontroller libraries
- ST7789 is generally more expensive but offers better display quality

The code initialization and communication protocols are similar, though the ST7789 has some additional commands for its extended features.