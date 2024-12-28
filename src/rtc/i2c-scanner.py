from machine import I2C, Pin
import config
CLK_PIN = config.CLK_PIN
DST_PIN = config.DST_PIN
RST_PIN = config.RST_PIN

print("Clock on pin: ", CLK_PIN)
print("Data on pin: ", DST_PIN)
print("Reset on pin: ", RST_PIN)

i2c = I2C(0, scl=Pin(CLK_PIN), sda=Pin(DST_PIN), freq=800000)

scan_result = i2c.scan()

print(scan_result)

print("I2C addresses found:", [hex(device_address) for device_address in i2c.scan()])