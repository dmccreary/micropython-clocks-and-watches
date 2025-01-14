# Introduction to Clock and Watch Projects and Kits

## Project Structure

Each project has a brief overview of the project, a separate page for the physical assembly of the clock and a detailed guide to program the clock.  The documentation may also
have sample generative AI prompts you can use to generate your own code using a tool such as OpenAI's ChatGPT or Anthropic Claude.  In general, the more precise your prompt is, the higher the odds that the code generated will be correct.

Each project also has separate folder in the GitHub "src/kits" folder.  The running clock programs (called the "mains") come in several variations.  One uses manual buttons (main-buttons.py) to set the time after a power outage.  The other version called the "main-rtc.py" file name uses a real-time-clock to remember the time between power outages.  They require an additional RTC clock that uses a coin-cell battery to hold the current time.  If you find a "main-w.py" file that uses the secrets.py file to lookup
your local wifi login to get the time from the internet.  These versions don't need buttons or a RTC to get the correct time. They only need internet access.

## LED Clocks

### Standard TM1637 LED Clock

Easy to program LED clock with 4 7-segment displays.

[TM1637 LED Clock Kit](./tm1637/index.md)

### TinySSD1306 OLED with an I2C Interface

This small low-cost OLED display is easy to hook up with just 4 wires.
The combination of low-cost and easy hookup makes it an ideal
starter project.

We hav purchased these OLEDs on eBay for under $4 each.  Some of
they have the first 20 rows yellow and the remaining 44 rows blue.

[Tiny SSD1306 OLED with I2C Interface](./ssd1306-i2c/index.md)

### Larger 2.42" OLED SSD1306 with SPI Interface

[Larger OLED](./oled-large/index.md)

## NeoPixel Clocks

### Binary Clock

[Binary Clock](./neopixel/binary-clock/index.md)

### Seven Segment Clock

[](./neopixel/seven-segment-clock/index.md)

### Fibonacci Clock

[Fibonacci Clock](./neopixel/fibonacci-clock/index.md)


## LilyGo RP2040

[LilyGo RP2040 Kit](./lilygo/index.md)

## SmartWatch Displays

[GC9a01 Smartwatch Display](./gc9a01/index.md)

[Waveshare LCD Smartwatch Display](./waveshare-lcd/index.md)

## E-Paper Clocks

[Waveshare e-Paper](./e-ink/index.md)

