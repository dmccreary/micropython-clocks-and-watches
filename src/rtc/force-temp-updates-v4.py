from machine import Pin, I2C, SPI
import ssd1306
from utime import sleep, localtime, time
from micropython import const

# Pin definitions
LED_PIN = const(25)
SCL_PIN = const(2)
SDA_PIN = const(3)
RES_PIN = const(4)
DC_PIN = const(5)
CS_PIN = const(6)
I2C_SCL_PIN = const(1)
I2C_SDA_PIN = const(0)

# Constants
DS3231_ADDR = const(0x68)
TEMP_UPDATE_INTERVAL = const(10)  # Force new reading every 10 seconds
DISPLAY_UPDATE_INTERVAL = const(1)  # Update display every second

# Initialize hardware
led = Pin(LED_PIN, Pin.OUT)
scl = Pin(SCL_PIN)
sda = Pin(SDA_PIN)
spi = SPI(0, sck=scl, mosi=sda, baudrate=100000)

# Display setup
res = Pin(RES_PIN)
dc = Pin(DC_PIN)
cs = Pin(CS_PIN)
oled = ssd1306.SSD1306_SPI(128, 64, spi, dc, res, cs)

# I2C setup for RTC
i2c = I2C(0, sda=Pin(I2C_SDA_PIN), scl=Pin(I2C_SCL_PIN))

def init_rtc():
    """Initialize RTC and verify it's responding"""
    devices = i2c.scan()
    print(f"I2C devices found: {[hex(d) for d in devices]}")
    if DS3231_ADDR not in devices:
        raise RuntimeError(f"DS3231 not found at address 0x{DS3231_ADDR:02X}")
    
    # Read and print all control registers
    print("\nRTC Register Status:")
    control = i2c.readfrom_mem(DS3231_ADDR, 0x0E, 1)[0]
    status = i2c.readfrom_mem(DS3231_ADDR, 0x0F, 1)[0]
    print(f"Control Register (0x0E): 0x{control:02X}")
    print(f"Status Register (0x0F): 0x{status:02X}")
    
    # Clear all flags in status register
    i2c.writeto_mem(DS3231_ADDR, 0x0F, bytes([0]))
    
    # Enable oscillator, disable square wave, enable temperature conversion
    control &= ~(1 << 7)  # Clear EOSC bit to enable oscillator
    control &= ~(1 << 2)  # Disable square wave
    control |= (1 << 5)   # Enable CONV bit for temperature conversion
    i2c.writeto_mem(DS3231_ADDR, 0x0E, bytes([control]))
    
    # Verify the changes
    control_verify = i2c.readfrom_mem(DS3231_ADDR, 0x0E, 1)[0]
    status_verify = i2c.readfrom_mem(DS3231_ADDR, 0x0F, 1)[0]
    print(f"After init - Control Register: 0x{control_verify:02X}")
    print(f"After init - Status Register: 0x{status_verify:02X}")

def bcd2dec(bcd):
    """Convert binary coded decimal to decimal."""
    return ((bcd >> 4) * 10) + (bcd & 0x0F)

def read_ds3231():
    """Read time from DS3231 RTC."""
    data = i2c.readfrom_mem(DS3231_ADDR, 0x00, 7)
    second = bcd2dec(data[0])
    minute = bcd2dec(data[1])
    hour = bcd2dec(data[2] & 0x3f)  # 24 hour mode
    day = bcd2dec(data[4])
    month = bcd2dec(data[5] & 0x1f)
    year = bcd2dec(data[6]) + 2000
    return (year, month, day, hour, minute, second)

def force_temp_conversion():
    """Force a new temperature conversion in the DS3231."""
    try:
        # First, ensure the control register is in a known state
        i2c.writeto_mem(DS3231_ADDR, 0x0E, bytes([0x20]))  # Base configuration
        sleep(0.01)  # Brief delay
        
        # Clear the status register
        i2c.writeto_mem(DS3231_ADDR, 0x0F, bytes([0x00]))
        sleep(0.01)  # Brief delay
        
        # Read initial state
        control = i2c.readfrom_mem(DS3231_ADDR, 0x0E, 1)[0]
        status = i2c.readfrom_mem(DS3231_ADDR, 0x0F, 1)[0]
        print(f"\nBefore conversion - Control: 0x{control:02X}, Status: 0x{status:02X}")
        
        # Explicitly set the CONV bit (don't use OR operation)
        i2c.writeto_mem(DS3231_ADDR, 0x0E, bytes([0x60]))  # 0x60 = 0x20 | (1 << 5)
        sleep(0.01)  # Brief delay
        
        # Verify the CONV bit was set
        control = i2c.readfrom_mem(DS3231_ADDR, 0x0E, 1)[0]
        print(f"After setting CONV - Control: 0x{control:02X}")
        
        if control != 0x60:
            print(f"Warning: CONV bit not set properly. Expected 0x60, got 0x{control:02X}")
        
        # Wait for the busy bit with retries
        start_time = time()
        attempt = 0
        while True:
            attempt += 1
            status = i2c.readfrom_mem(DS3231_ADDR, 0x0F, 1)[0]
            print(f"Status check {attempt}: 0x{status:02X}")
            
            if not (status & 0x04):  # Check BUSY bit (bit 2)
                print("Conversion complete!")
                break
            
            if time() - start_time > 0.5:  # Reduced timeout to 500ms
                print("Temperature conversion timeout")
                break
            
            sleep(0.05)  # 50ms between checks
            
    except Exception as e:
        print("Error forcing temperature conversion:", e)

def read_temperature():
    """Read temperature from DS3231 RTC with 0.25°C resolution."""
    try:
        # Read temperature registers
        temp_msb = i2c.readfrom_mem(DS3231_ADDR, 0x11, 1)[0]
        temp_lsb = i2c.readfrom_mem(DS3231_ADDR, 0x12, 1)[0]
        
        # Handle signed temperature value (2's complement)
        temp_c = temp_msb
        if temp_msb & 0x80:  # Negative value
            temp_c = -((~temp_msb + 1) & 0xFF)
        
        # Add fractional part (0.25°C resolution)
        temp_c += ((temp_lsb >> 6) * 0.25)
        
        # Convert to Fahrenheit
        temp_f = (temp_c * 9/5) + 32
        print(f"Raw temp data - MSB: 0x{temp_msb:02X}, LSB: 0x{temp_lsb:02X}")
        print(f"Temperature: {temp_c:.2f}°C, {temp_f:.2f}°F")
        return temp_f
        
    except Exception as e:
        print("Error reading temperature:", e)
        return None

# Seven-segment display mapping
segmentMapping = [
    #a, b, c, d, e, f, g
    [1, 1, 1, 1, 1, 1, 0], # 0
    [0, 1, 1, 0, 0, 0, 0], # 1
    [1, 1, 0, 1, 1, 0, 1], # 2
    [1, 1, 1, 1, 0, 0, 1], # 3
    [0, 1, 1, 0, 0, 1, 1], # 4
    [1, 0, 1, 1, 0, 1, 1], # 5
    [1, 0, 1, 1, 1, 1, 1], # 6
    [1, 1, 1, 0, 0, 0, 0], # 7
    [1, 1, 1, 1, 1, 1, 1], # 8
    [1, 1, 1, 1, 0, 1, 1]  # 9
]

def drawDigit(digit, x, y, width, height, thickness, color):
    """Draw a single digit using seven segments."""
    if digit < 0 or digit > 9:
        return
    
    segmentOn = segmentMapping[digit]
    
    # Draw horizontal segments (top, middle, bottom)
    for i in [0, 3, 6]:
        if segmentOn[i]:
            yOffset = 0 if i == 0 else \
                     (height - thickness) if i == 3 else \
                     (height // 2 - thickness // 2)
            oled.fill_rect(x, y + yOffset, width, thickness, color)
    
    # Draw vertical segments
    for i in [1, 2, 4, 5]:
        if segmentOn[i]:
            # Determine vertical position
            startY = y if (i == 1 or i == 5) else (y + height // 2)
            endY = (y + height // 2) if (i == 1 or i == 5) else (y + height)
            # Determine horizontal position
            xOffset = 0 if (i == 4 or i == 5) else (width - thickness)
            oled.fill_rect(x + xOffset, startY, thickness, endY - startY, color)

def draw_colon(x, y):
    """Draw the flashing colon separator."""
    oled.fill_rect(x, y, 3, 3, 1)
    oled.fill_rect(x, y + 14, 3, 3, 1)

def update_screen(year, month, day, hour, minute, am_pm, colon_on, temp_f):
    """Update the entire display with current time and temperature."""
    # Display layout constants
    left_margin = -28
    y_offset = 11
    digit_width = 33
    digit_height = 40
    digit_spacing = 41
    digit_thickness = 5

    oled.fill(0)  # Clear display
    
    # Draw date at top
    date_str = f"{month}/{day}/{year}"
    oled.text(date_str, 0, 0, 1)
    
    # Draw temperature
    if temp_f is not None:
        temp_str = f"{temp_f:.1f}F"
        oled.text(temp_str, 0, 54, 1)
    
    # Convert to 12-hour format
    display_hour = hour if hour <= 12 else hour - 12
    if display_hour == 0:
        display_hour = 12
    
    # Calculate digits
    hour_ten = display_hour // 10 if display_hour >= 10 else -1
    hour_right = display_hour % 10
    minute_ten = minute // 10
    minute_right = minute % 10
    
    # Draw digits
    drawDigit(hour_ten, left_margin, y_offset, digit_width, digit_height, digit_thickness, 1)
    drawDigit(hour_right, left_margin + digit_spacing - 2, y_offset, digit_width, digit_height, digit_thickness, 1)
    drawDigit(minute_ten, left_margin + 2 * digit_spacing, y_offset, digit_width, digit_height, digit_thickness, 1)
    drawDigit(minute_right, left_margin + 3 * digit_spacing, y_offset, digit_width, digit_height, digit_thickness, 1)
    
    if colon_on:
        draw_colon(47, 20)
    
    # Draw AM/PM indicator
    oled.text(am_pm, 106, 55, 1)
    oled.show()

def main():
    """Main program loop."""
    print("Initializing RTC...")
    init_rtc()
    print("RTC initialized successfully")
    
    # Initialize temperature conversion
    force_temp_conversion()
    temp_f = read_temperature()
    if temp_f is None:
        print("Failed to get initial temperature reading")
        temp_f = 0.0
    
    last_temp_conversion = time()
    last_display_update = time()
    colon_state = True
    
    print("Starting main loop...")
    while True:
        current_time = time()
        
        # Check if it's time for a new temperature reading
        if current_time - last_temp_conversion >= TEMP_UPDATE_INTERVAL:
            print("\nForcing new temperature conversion...")
            force_temp_conversion()
            temp_f = read_temperature()
            last_temp_conversion = current_time
        
        # Update display if needed
        if current_time - last_display_update >= DISPLAY_UPDATE_INTERVAL:
            now = read_ds3231()
            year, month, day, hour, minute, second = now
            am_pm = "PM" if hour >= 12 else "AM"
            
            update_screen(year, month, day, hour, minute, am_pm, colon_state, temp_f)
            colon_state = not colon_state
            last_display_update = current_time

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram terminated by user")
    except Exception as e:
        print("Error:", e)