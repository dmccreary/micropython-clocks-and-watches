# Larger Fonts

Many display libraries use the MicroPython framebuf standards that
only provide for a single font.  This is sometimes fine for simple
small displays, but it is sometimes insufficient for some projects
where either a smaller or larger font is used.

The ssd1306 driver is a good example of the default behaviour of text
drawing.  Only a single font is suppied.

```py
display.text('Hello, World!', 0, 0, 1)
display.show()
```

Some display drivers allow you to change the default font:

[LCD160 Set Font](https://docs.micropython.org/en/latest/library/lcd160cr.html#lcd160cr.LCD160CR.set_font)

[Font to Py Command](https://github.com/peterhinch/micropython-font-to-py)

[Sample Font Files](https://github.com/peterhinch/micropython-nano-gui/tree/master/gui/fonts)

## References

[Peter Hinch's Font to Python Utility](https://github.com/peterhinch/micropython-font-to-py) -  a utility takes input a font file in ttf or otf form together with a height in pixels and outputs a Python source file containing the font as a bitmap.

[Peter Hinch's Nano GUI](https://github.com/peterhinch/micropython-nano-gui)

[Les' Lab: Designing your own Pico fonts](https://www.youtube.com/watch?v=BMlGyAYNdF8&t=2s) - Raspberry Pi Pico display fonts in MicroPython: How to design fonts for your Pi Pico project.
