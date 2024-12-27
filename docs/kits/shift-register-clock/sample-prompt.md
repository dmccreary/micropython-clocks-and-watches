# Sample ChatGPT Prompt

``` prompt
    Please help me write a micropython program for a 4-digit clock.  I have a digital clock display with 4 digits I purchased on eBay.  Each of the 4 digits has 7 segments and there is also a colon between the 2nd and 3rd digits.  The part says they use 74hc595 shift registers.  The names of the connectors are:

    1. GND
    2. VCC
    3. RCLK
    4. SCLK
    5. DIO

    I found a micropython driver called: sr74hc595.  When I run a test program the various segments do light up, but I don't see a pattern.  Can you give me some suggestions on how to write a driver that writes the correct time like 12:34?

    Here is the code that is working:

# SPDX-FileCopyrightText: 2021 Mike Causer <https://github.com/mcauser>
# SPDX-License-Identifier: MIT

"""
MicroPython 74HC595 8-Bit Shift Register
https://github.com/mcauser/micropython-74hc595
"""

from machine import Pin
# from sr74hc595 import SR74HC595_BITBANG
from sr74hc595 import SR74HC595_BITBANG
from utime import sleep

ser = Pin(2, Pin.OUT)
rclk = Pin(0, Pin.OUT)
srclk = Pin(1, Pin.OUT)

# construct without optional pins
sr = SR74HC595_BITBANG(ser, srclk, rclk)

#sr.clear()  # raises RuntimeError because you haven't provide srclr pin
#sr.enable()  # raises RuntimeError because you haven't provide oe pin

# reconstruct with all pins
oe = Pin(3, Pin.OUT, value=0)  # low enables output
srclr = Pin(3, Pin.OUT, value=1)  # pulsing low clears data

sr = SR74HC595_BITBANG(ser, srclk, rclk, srclr, oe)



while True:
    
    sr.bit(1)  # send high bit, do not latch yet
    sr.bit(0)  # send low bit, do not latch yet
    sr.latch()  # latch outputs, outputs=0000_0010

    sr.bit(1, 1)  # send high bit and latch, outputs=0000_0101
    sr.bit(0, 1)  # send low bit and latch, outputs=0000_1010

    sr.bits(0xFF, 4)  # send 4 lowest bits of 0xff (sends 0x0f), outputs=1010_1111
    sr.clear(0)  # clear the memory but don't latch yet
    sr.latch()  # next latch shows the outputs have been reset
    sr.bits(0b1010_1010, 8)  # write some bits
    sr.clear()  # clear the memory and latch, outputs have been reset

    sr.enable()  # outputs enabled
    sr.enable(0)  # outputs disabled

    sleep(1)

    sr.bits(0b1111_1111, 8)  # write some bits
    sr.clear()  # clear the memory and latch, outputs have been reset

    sr.enable()  # outputs enabled
    sr.enable(0)  # outputs disabled

    sleep(1)

    sr.bits(0b0000_0011, 8)  # write some bits
    sr.clear()  # clear the memory and latch, outputs have been reset

    sr.enable()  # outputs enabled
    sr.enable(0)  # outputs disabled
    sleep(1)

