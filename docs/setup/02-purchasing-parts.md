# Strategy for Parts Purchasing Guide

We have seen many well intended parent come into our workshops telling stories
about a $400 robot kit that was used for an hour and then sat in the back
of a closet.  Before you go out and purchase an expensive STEM kit, we
suggest you start small and see if your student will really use the kit.

## Breadboards

We strongly suggest purchasing breadboards in bulk at least 10 at a time.
We use eBay for purchasing all our breadboards.

Many of our projects use the 1/2 size 400-tie breadboards.  This is usually
sufficient for simple projects.



## MicroControllers

Because all or examples run MicroPython, your microcontroller will also need to run MicroPython.
Unfortunately, older microcontrollers like the Arduino Uno only come with 2K of RAM.  Since we need at least 16K of RAM to run MicroPython, the older Arduino systems will not work.

Therefore we strongly suggest you go with a newer microcontroller like the Raspberry Pi Pico which
typically sells for under $4.

### Purchasing the Raspberry Pi Pico

We love MicroCenter because they sell the [Raspberry Pi Pico for only $3.99](https://www.microcenter.com/product/661033/raspberry-pi-pico-microcontroller-development-board).  If there is a MicroCenter near your home, we strongly suggest purchasing the parts there.  

![Pico](../img/microcenter-pico.png)

### Raspberry Pi Pico W

If you are going wireless, you will need to pay an extra dollar to get the [Raspberry Pi Pico for $5.99](https://www.microcenter.com/product/650108/raspberry-pi-pico-w)

![Pico W](../img/microcenter-pico-w.png)

If the Raspberry Pi Picos are out of stock, a backup plan might be an ESP-32 microcontroller.
There are two challenges you might face with the ESP-32:

1. The development boards at MicroCenter, SparkFun and Adafruit are 4x more expensive
2. There is a huge variety of these boards from many different manufactures.  So the instructions you get on each website may not match the device you purchase.

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
