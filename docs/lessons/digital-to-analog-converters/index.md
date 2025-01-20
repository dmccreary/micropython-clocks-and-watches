# Digital to Analog Converters and the I2S Protocol

## The PCM5102 DAC Board

![pcm5102a-board-top-bottom](./pcm5102a-board-top-bottom.png)
## Connections

Hooking the up PCM5102 board is pretty easy for the general case:

- SCK – Gnd
- BCK – I2S bit clock pin
- DIN – I2S data pin
- LCK – I2S word select pin
- GND – Gnd
- VIN – 3.3V

## Pico Connections

Use the lower right connections

- SCK_PIN = 16 # Connect to BCK on DAC (Bit Clock)
- WS_PIN = 17 #  Connect to LCK on DAC (Word Select/Left-Right Clock)
- SD_PIN = 18 # Connect to DIN on DAC (Data Input)
I2S_ID = 0
BUFFER_LENGTH_IN_BYTES = 2000


## Sampling Rates

We can also lower sample rates. The PCM5102A supports the following standard sample rates:

-   8000 Hz (telephone quality)
-   16000 Hz (decent speech quality)
-   22050 Hz (half of CD quality)
-   32000 Hz (digital radio quality)
-   44100 Hz (CD quality)
-   48000 Hz (professional audio)
-   88200 Hz (high resolution)
-   96000 Hz (high resolution)
## References

[Todbot Blog: Cheap stereo line out I2S DAC](https://todbot.com/blog/2023/05/16/cheap-stereo-line-out-i2s-dac-for-circuitpython-arduino-synths/)