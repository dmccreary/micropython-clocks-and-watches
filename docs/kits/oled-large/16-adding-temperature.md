# Adding Ambient Room Temperature

![](./display-temp.jpg)

The DS3231 RTC has one nice feature in that it can also
display the ambient temperature of the area it is in.

To do this we need to access the registers that hold the temperature information through the I2C bus.  Note that the DS3231 driver that we are using does not support getting access to the temperature.

## Sample Code

```python
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
```

This function will read directly from the DS3231 I2C memory ```readfrom_mem```.

Let's go through it step by step:

### Function Definition

First, we have a function called `read_temperature()` that's designed to read the temperature with pretty good accuracy (up to 0.25°C).  It returns the temperature in degrees Fahrenheit.

### Reading Memory Via the I2C Functions

Inside the function, it first tries to read two pieces of data:

```python
temp_msb = i2c.readfrom_mem(DS3231_ADDR, 0x11, 1)[0]
temp_lsb = i2c.readfrom_mem(DS3231_ADDR, 0x12, 1)[0]
```

- This is reading two adjacent memory locations from the DS3231 chip using the I2C protocol:
- The first address (0x11) contains the main temperature number
- The second box (0x12) contains extra detail for more accurate readings

### Converting Formats

Then it handles something called "2's complement" which is just a fancy way of dealing with negative temperatures:

```python
temp_c = temp_msb
if temp_msb & 0x80:  # Negative value
    temp_c = -((~temp_msb + 1) & 0xFF)
```

If the number shows it's negative (like when it's below freezing), this code converts it properly

### Getting The Fraction

Next, it adds the fractional part to get more precise readings:

```python
temp_c += ((temp_lsb >> 6) * 0.25)
```

This gives us those in-between temperatures, like 20.25°C or 20.75°C

### Converting Celsius to Fahrenheit

Then it converts the temperature from Celsius to Fahrenheit:

```python
temp_f = (temp_c * 9/5) + 32
```
This is the same formula you might use in math class: °F = (°C × 9/5) + 32

### Printing and Returning

Finally, it prints out both the raw data and the converted temperatures:

```python
print(f"Raw temp data - MSB: 0x{temp_msb:02X}, LSB: 0x{temp_lsb:02X}")
print(f"Temperature: {temp_c:.2f}°C, {temp_f:.2f}°F")
```
- It shows both Celsius and Fahrenheit with two decimal places
- The raw data is shown in hexadecimal (that's what the '0x' means)

If anything goes wrong while reading the temperature, it will run the following:

```python
except Exception as e:
    print("Error reading temperature:", e)
    return None
```
- Print out what went wrong
- Return `None` to indicate there was an error

Think of this like a digital thermometer that can read temperatures very precisely and give you the reading in both Celsius and Fahrenheit. The code is just the instructions for how to get that reading from the chip.
