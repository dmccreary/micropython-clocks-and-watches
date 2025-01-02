from machine import I2C, Pin
import time

# I2C setup
i2c = I2C(0, sda=Pin(0), scl=Pin(1))
devices_found = i2c.scan()
for device in devices_found:
    print(device, hex(device))