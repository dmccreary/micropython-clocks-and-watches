from machine import I2C, Pin

# OLED DATA Pin
OLED_SSD1306_SDA_PIN = 0
# OLED Clock Pin
OLED_SSD1306_SCL_PIN = 1

sda=Pin(OLED_SSD1306_SDA_PIN, Pin.OUT)
scl=Pin(OLED_SSD1306_SCL_PIN, Pin.OUT)

i2c = I2C(0, scl=scl, sda=sda, freq=3000000)
first_device = i2c.scan()[0]
# print("dec:", first_device, "hex:", hex(first_device))

if first_device == 60:
    print("PASS: OLED Found on dec: 60 hex: 0x3c")
else:
    print("FAIL: OLED not found on expected address dec: 60 hex: 0x3c")