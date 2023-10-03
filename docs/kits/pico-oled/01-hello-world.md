# Hello World

To get started, let's just draw the string "Hello world!" on the display.

Here is the code:

```py
import machine
import ssd1306

SCL=machine.Pin(2) # SPI CLock
SDA=machine.Pin(3) # SPI Data

RES = machine.Pin(4) # Reset
DC = machine.Pin(5) # Data/command
CS = machine.Pin(6) # Chip Select

spi=machine.SPI(0, sck=SCL, mosi=SDA)
oled = ssd1306.SSD1306_SPI(128, 64, spi, DC, RES, CS)

# erase the entire screen with black
oled.fill(0)

# place a hello message at point (0,0) in white
oled.text("Hello world!", 0, 0, 1)

# send the entire frame buffer to the display via the SPI bus
oled.show()
```

!!! Challenges
    1. Can you change the message from "Hello world!" to have your name in it?
    2. Can you change the location of the text on the screen by changing the location point from (0,0) to another place on the screen?  The screen is 128 pixels wide by 64 pixels high.
    3. How far down can you display the message without going off the screen?
    2. How many characters wide can a message be before it goes off the right edge of the dipsplay?
    4. Can you display multiple messages on different lines?