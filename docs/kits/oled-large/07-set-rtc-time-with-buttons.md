# Set the DS3231 RTC using Buttons

!!! prompt
    Please create a new program that allows the user to set the time in the DS3231 RTC using the three buttons. Use the main-v1.py as your starting point and merge in the code from 08-button-mode-with-debounce.py to change the mode from:

    mode 0 - clock running
    mode 1 - set hour with hour digits on screen flashing every 500ms
    mode 2 - set minute with minute digits on screen flashing every 500ms
    mode 3 - set am/pm with am/pm text flashing every 500ms

## Response

Key changes made:

1. Integrated button handling with debounce from 08-button-mode-with-debounce.py
2. Added flashing display elements based on current mode 
3. Modified time adjustment logic to work with RTC
4. Simplified display code while maintaining core functionality
5. Added proper button pin configuration from config.py

Test the code by:

1. Connect buttons to specified GPIO pins
2. Press mode button to cycle through modes
3. Use increment/decrement buttons to adjust time
4. Verify display flashing in each mode

```python
