# Sample Prompt to Generate Clock Code

## Prompt

!!! prompt
    We created a clock display using a 74 pixel WS2811B LED strip.
    The clock has three full digits and a "1" for the tens digit as well as two pixels for the colon.
    Each digit has seven segments with three pixels per segment.
    The right-most ones digit minutes digit starts at 0 and goes to 20.
    The second digit for the tens of minutes goes from 21 to 41.
    The colons are 42 and 43.
    The third digit is for the one hours and goes from 44 to 64.
    The hours ten single 1 goes from 65 to 73.
    Within a digit, here are the segment pixels
    Segment a on the top are pixels (0,1,2).
    Segment b on the upper right are pixels (3,4,5)
    Segment c on the lower right are pixels (6,7,8)
    Segment d on the bottom are pixels (9,10,11)
    Segment e on the lower left are pixels (12, 13, 14)
    Segment f on the upper left are pixels (15, 16, 17)
    Segment g in the middle are pixels (18,19 and 20)

    Please write a clock program in MicroPython that displays the hours and minutes of localtime() function but the hours range from 1 to 12.
    Make the colon turn on and off every second.

    Here is the preamble

    from machine import Pin
    from neopixel import NeoPixel
    from utime import sleep

    NUMBER_PIXELS = 74
    strip = NeoPixel(Pin(0), NUMBER_PIXELS)
    