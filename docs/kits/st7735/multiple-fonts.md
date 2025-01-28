# Multiple Fonts

Looking at the provided code, I can help explain the font situation and suggest some improvements for working with larger fonts on the ST7735 display.

Currently, the code is using a basic 5x7 pixel font ("font5x7.fnt") which is indeed quite small and pixelated. There are several ways to handle larger, better-looking fonts on this display:

### 1. BDF/PCF Fonts:
You could convert standard BDF/PCF fonts into a custom format that works with your display. Here's how we could implement this:

To use this improved font system, you would:

1. Convert a BDF font to our binary format using the `convert_bdf_to_binary()` function
2. Load and use the font in your main code like this:

```python
from custom_font_handler import FontHandler

# Initialize your display as before
spi = machine.SPI(0, baudrate=8000000)
d = ST7735.ST7735(spi, rst=4, ce=6, dc=5)
d.reset()
d.begin()

# Create font handler and load font
font_handler = FontHandler(d)
font_handler.load_font('your_converted_font.bin')

# Use the font
font_handler.text(10, 10, "Hello World!", d.rgb_to_565(255, 255, 255))
```

### 2. Bitmap Fonts:
Another approach would be to store pre-rendered characters as bitmap images and display them using your existing `bmp()` function. This would give you the best quality but would use more storage space.

### 3. Vector Fonts:
While more complex, you could implement basic vector font rendering. This would give you scalable text but would require more processing power.

For the best balance of quality and performance, I recommend going with the BDF font approach (option 1). You can find many BDF fonts online, including larger sizes that would look better on your display. Some good fonts to start with would be:

- Terminus (has sizes from 6x12 to 20x40)
- ProFont (clean and readable at various sizes)
- GNU Unifont (comprehensive character coverage)

To get started, you would:

1. Download a BDF font
2. Convert it using the provided converter
3. Copy the binary font file to your Pico
4. Use the FontHandler class to render text

Would you like me to provide an example using a specific BDF font, or would you prefer help implementing one of the other approaches?