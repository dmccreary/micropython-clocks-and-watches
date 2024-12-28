from machine import I2C, Pin
import config

CLK_PIN = config.CLK_PIN
DST_PIN = config.DST_PIN
DS_PIN = config.DS_PIN

print("Clock on pin:", CLK_PIN)
print("Data on pin:", DST_PIN)
print("Data Select on pin:", DS_PIN)

i2c = I2C(0, scl=Pin(CLK_PIN), sda=Pin(DST_PIN), freq=100000)
scan_result = i2c.scan()
print("I2C addresses found:", [hex(device_address) for device_address in scan_result])

if 104 in scan_result:
    print("PASS: DS1307 FOUND")
else:
    print("FAIL: DS1307 NOT FOUND")