from machine import I2C, Pin
import config
CLK_PIN = config.CLK_PIN
DST_PIN = config.DST_PIN
RST_PIN = config.RST_PIN

scl_pin = Pin(CLK_PIN, Pin.IN, Pin.PULL_UP)
sda_pin = Pin(DST_PIN, Pin.IN, Pin.PULL_UP)
rst_pin = Pin(RST_PIN, Pin.OUT)
rst_pin.value(0)
rst_pin.value(1)

print("Clock on pin: ", CLK_PIN)
print("Data on pin: ", DST_PIN)
print("Reset on pin: ", RST_PIN)

i2c = I2C(0, scl=scl_pin, sda=sda_pin, freq=100000)

print(i2c.scan())