from machine import I2C, Pin
import time

# I2C setup
i2c = I2C(0, sda=Pin(0), scl=Pin(1))

# Device addresses
RTC_ADDR = 0x68  # Both DS1307 and DS3231 use 0x68

def identify_rtc():
    """
    Identify whether the RTC is a DS1307 or DS3231
    Returns: String identifying the RTC type
    """
    try:
        # Try to read the status register (0x0F) - only exists on DS3231
        i2c.writeto(RTC_ADDR, b'\x0F')
        status = i2c.readfrom(RTC_ADDR, 1)[0]

        # Try to read control register (0x0E) - only exists on DS3231
        i2c.writeto(RTC_ADDR, b'\x0E')
        control = i2c.readfrom(RTC_ADDR, 1)[0]

        # If we got here, it's almost certainly a DS3231
        # Try reading temperature registers as final confirmation
        i2c.writeto(RTC_ADDR, b'\x11')
        temp_data = i2c.readfrom(RTC_ADDR, 2)

        return "DS3231 (Temperature-compensated RTC)"

    except Exception as e:
        # If we couldn't read those registers, it's probably a DS1307
        # Let's verify by trying to read the control register (0x07) of DS1307
        try:
            i2c.writeto(RTC_ADDR, b'\x07')
            control = i2c.readfrom(RTC_ADDR, 1)[0]
            return "DS1307 (Basic RTC)"
        except:
            return "Unknown RTC device"

def main():
    print("\nRTC Model Identifier")
    print("-" * 40)

    # First check if any device is present at RTC address
    devices = i2c.scan()
    if RTC_ADDR not in devices:
        print(f"No RTC found at address 0x{RTC_ADDR:02X}")
        return

    # Identify the RTC
    rtc_type = identify_rtc()
    print(f"Found: {rtc_type}")

    if "DS3231" in rtc_type:
        # Read temperature for DS3231
        i2c.writeto(RTC_ADDR, b'\x11')
        temp_data = i2c.readfrom(RTC_ADDR, 2)
        temp_msb = temp_data[0]
        temp_lsb = (temp_data[1] >> 6) * 25  # 0.25°C precision
        temp_c = temp_msb + (temp_lsb / 100.0)
        temp_f = (temp_c * 9/5) + 32
        print(f"Temperature: {temp_c:.2f}°C ({temp_f:.2f}°F)")

if __name__ == "__main__":
    main()