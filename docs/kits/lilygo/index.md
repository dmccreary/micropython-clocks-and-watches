# LILYGO T-Display RP2040 

[LILYGO](https://www.lilygo.cc/) makes low-cost and high-quality microcontroller development boards that include small displays.  Although
most of their boards run on C programs on ESP-32 processors, they
do have one that runs MicroPython on an RP2040.  This "kit" is
really just that development board placed on a breadboard.  The device
has two buttons on it which can be used to adjust the time.

This is a color 1.14 inch LCD display PS with 240*135 resolution.
It uses the ST7789V chip that has an extreamly high quality
driver created by Russ Hughes that allows for flicker-free
drawing.

I purchased mine on [Ebay](https://www.ebay.com/itm/255602844724) for $10.66 and three dollars for shipping.

Although the display is too small for most robotic applications where the
robot is on the floor and we are standing, it is a good example of how
we can get both clocks and watches to look great.  My hope is that LILYGO
comes out with a larger display in the future.

Lilygo also sells their own ["wearable" watch kits](https://www.lilygo.cc/collections/wearable-kit)] for $35 to $45.  However, I have not purchased any of these that can be programmed with an RP2040 and MicroPython yet.  Here is a [GitHub Page for the T-Watch](https://github.com/Xinyuan-LilyGO/MicroPython_ESP32_psRAM_LoBo#micropython-for-ttgo-t-watch) that implies it might be on the way.

## Getting Started

To use the ST7789V driver we MUST use a custom image provide by Rull Hughes.  This is because the driver is written in low-level C code
and the python driver requires it to be combiled into the firmware image.

I downloaded the custom image here:

[T-DISPLAY RP2040 Firmware](https://github.com/russhughes/st7789_mpy/tree/master/firmware/T-DISPLAY-RP2040)

I then held the Boot button down while I powered up the device.

I soldered my own header pins on the LILYGO and placed it on a breadboard.  Unfortunatly this makes it impossible to hold down the
boot button with the device on the breadboard.




```py
```


## Referneces
Sample GitHub repo: https://github.com/Xinyuan-LilyGO/LILYGO-T-display-RP2040

ST7789V Submodule:
https://github.com/russhughes/st7789_mpy/tree/b4aa060b74e2d2490770fa92310571f7602059f9

Config:
https://github.com/russhughes/st7789_mpy/blob/b4aa060b74e2d2490770fa92310571f7602059f9/examples/configs/tdisplay_rp2040/tft_config.py
