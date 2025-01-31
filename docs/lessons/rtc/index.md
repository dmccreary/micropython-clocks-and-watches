# Real Time Clocks

The DS3231 is a highly accurate real-time clock (RTC) integrated circuit that maintains precise time using an internal temperature-compensated crystal oscillator (TCXO).

Key features:

- Accuracy within ±2ppm (about 1 minute/year) across -40°C to +85°C
- Battery backup using CR2032 for continuous timekeeping
- I2C interface operating at 400kHz
- Built-in temperature sensor (±3°C accuracy)
- Two programmable time-of-day alarms

The device stores time data in BCD format across multiple registers:

0x00: Seconds
0x01: Minutes
0x02: Hours
0x03: Day
0x04: Date
0x05: Month
0x06: Year

**Example:** Reading hour register 0x02 returns value 0x15 in BCD, representing 15:00 (3:00 PM).

#### How Long Will The Battery Last

The typical operational duration of the backup coin-cell battery in real-time clock circuits ranges from 2 to 10 years, depending on temperature conditions and current draw. 

The DS3231 RTC module used in our kits draw 3μA at 
room temperature typically operates for 8 years on a single CR2032 battery.
The key factors affecting battery life are:

- Operating temperature (lower temps extend life)
- Current draw of the RTC (varies by model)
- Battery capacity (typical CR2032 = 220mAh)
- Additional features active (temperature sensing, alarms, etc.)