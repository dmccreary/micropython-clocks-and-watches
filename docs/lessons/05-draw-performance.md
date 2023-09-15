# Drawing Performance

One of the challenges we face when updating the watch display is that
refreshing an entire screen using a relatively slow SPI interface
means that we need to be thoughtful about updating the displays.

By default, many screen drivers update every pixel of the screen when
the user does a ```show()``` operation.  For small monochrome screens this is
not usually a problem.  But for larger color screens the draw times
can lead to slow updates.

Let's do a little math to see when drawing performance becomes a problem.  Remember that the human eye can's really see screen updates that occur faster than about 30 frames per second.  That is why most film movies were filled at 25 frames per second.

To calculate the full-screen draw time we need to calculate the total number of bits we need to send and then calculate the time it takes to send these bits.  We can then check our math by looking at timestamps just before we draw and after we finish
the drawing.

Let's start out with our favorite clock screen: the 128X64 monochrome OLED screen.

1. Width = 128
2. Height = 64
3. Bits per Pixel = 1

Total bits = 128 * 64 * 1 = 8,192 bits = 1024 bytes

Now we need to also know the transfer speed of our display interface.  Although there are both I2C and SPI versions of these displays, we usually prefer the SPI that should
transfer data at about 

[Pi Pico SPI LCD using a frame buffer to get 30fps animation - ILI9341 and ST7789 MicroPython drivers](https://www.youtube.com/watch?v=fGfb2NvDlG4)

## Sample Timer Code

We can calculate the time to draw the full screen by recording the number of clock
ticks in microseconds before and after we do a screen update.

```py
from utime import ticks_us

start = ticks_us()
screen_update()
end = ticks_us()
print('Execution time in microseconds:', end - start)
```

On the OLED screen, we get a result that is around 10 milliseconds which is 100 screen
updates per second.

## References

1. [Notes on the very slow refresh rate for ST7735
](https://www.reddit.com/r/raspberrypipico/comments/zx32ak/very_slow_refresh_rate_for_st7735/)