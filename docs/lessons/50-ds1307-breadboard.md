# Using the DS1307 IC On A Breadboard

You can use the DS1307 IC directly on a breadboard without a development board. 
Here's what you'll need:

1.  DS1307 IC (8-pin DIP package)
2.  32.768 kHz crystal oscillator
3.  CR2032 battery holder and battery (for backup power)
4.  Two 4.7kΩ pull-up resistors (for I2C)
5.  0.1µF decoupling capacitor
6.  Standard through-hole breadboard

The basic connections are:

```
DS1307 Pinout:
Pin 1 (X1) -> Crystal
Pin 2 (X2) -> Crystal
Pin 3 (VBAT) -> Battery positive
Pin 4 (GND) -> Ground
Pin 5 (SDA) -> I2C Data (needs pull-up)
Pin 6 (SCL) -> I2C Clock (needs pull-up)
Pin 7 (SQW) -> Optional square wave output
Pin 8 (VCC) -> 5V power`

```

The biggest advantages of using the raw IC are:

-   Lower cost than module boards
-   Smaller footprint
-   More control over the circuit design
-   Better understanding of the RTC system

Just remember that the DS1307 requires 5V power 
(unlike its successor DS3231 which can work with 3.3V), 
so make sure your microcontroller's I2C lines can 
handle 5V or use a level shifter if necessary.
