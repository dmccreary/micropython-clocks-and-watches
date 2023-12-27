# Hardware Configuration Files

All our current displays use the SPI interface.  The
alternative microcontroller bus, I2C, is about 10x
slower than SPI.  The SPI intrface
interface typically uses 7 wires, which can get
a little complex.  Just a single wire broken or two wires crossed can
will cause the display to not work.

We have dozens of sample programs for each kit.  And the exact
connections on our kits vary.  Rather than hard-coding the
hardware pin numbers in each example, we can move them
to a separate config.py file.  We can then just import
that file into each of our examples.

Here is a sample config.py file:

```py
# Dan's Robot Labs configuration file for ILI9341 clock project
# The colors on the SPI bus cable are:
# 3.3v power - red
# SCK - orange
# MISO/Data - yellow
# DC - green
# RESET - blue
# GND - black
# CS - purple

SCK_PIN = 2
MISO_PIN = 3 # labeled SDI(MOSI) on the back of the display
DC_PIN = 4
RESET_PIN = 5
CS_PIN = 6
ROTATION = 90

WIDTH=320
HEIGHT=240
BUTTON_1_PIN = 14 # one up from lower-left corner
BUTTON_2_PIN = 15 # lower left corner with USB on top
```

To use this configuration file you will need to do two things:

1. import the config file (don't add the .py extension)
2. Add the prefix ```config.``` to each value you would like
to reference.

```py
import config

WIDTH=config.WIDTH
```