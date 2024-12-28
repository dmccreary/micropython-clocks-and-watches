from ds1307 import DS1307
from machine import I2C, Pin
from utime import gmtime, sleep, time
import config
CLK_PIN = config.CLK_PIN
DST_PIN = config.DST_PIN
RST_PIN = config.RST_PIN

scl_pin = Pin(CLK_PIN, Pin.IN, Pin.PULL_UP)
sda_pin = Pin(DST_PIN, Pin.IN)
rst_pin = Pin(RST_PIN, Pin.OUT)
rst_pin.value(0)
sleep(.001)
rst_pin.value(1)

print("Clock on pin: ", CLK_PIN)
print("Data on pin: ", DST_PIN)
print("Reset on pin: ", RST_PIN)

# DS1307 on 0x68
I2C_ADDR = 0x68     # DEC 104, HEX 0x68

# define custom I2C interface, default is 'I2C(0)'
# check the docs of your device for further details and pin infos
# this are the pins for the Raspberry Pi Pico adapter board
i2c = I2C(0, scl=Pin(CLK_PIN), sda=Pin(DST_PIN), freq=800000)
print(i2c.scan())

ds1307 = DS1307(addr=I2C_ADDR, i2c=i2c)

print(hex(ds1307.addr))
print(hex(ds1307.weekday_start))
print(hex(ds1307.year))





