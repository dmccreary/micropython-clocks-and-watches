# Display Alarm Icon

```python
from array import array

def draw_alarm_icon(display, x, y, alarm_hour, alarm_minute, size=24):
    """
    Draw an alarm bell icon with time display using polygons.
    
    Args:
        display: SSD1306 display instance
        x, y: Top-left position for the icon
        alarm_hour: Hour of the alarm (1-12)
        alarm_minute: Minute of the alarm (0-59)
        size: Base size of the icon (default 24 pixels)
    """
    # Scale factors
    scale = size / 24  # Base size is 24 pixels
    
    # Bell body coordinates (scaled from base design)
    bell_body = array('B', [
        int(4 * scale),  int(0 * scale),    # Top left of dome
        int(20 * scale), int(0 * scale),    # Top right of dome
        int(24 * scale), int(12 * scale),   # Bottom right curve
        int(22 * scale), int(18 * scale),   # Right side
        int(2 * scale),  int(18 * scale),   # Left side
        int(0 * scale),  int(12 * scale),   # Bottom left curve
    ])
    
    # Bell base coordinates
    bell_base = array('B', [
        int(2 * scale),  int(18 * scale),   # Top left
        int(22 * scale), int(18 * scale),   # Top right
        int(20 * scale), int(20 * scale),   # Bottom right
        int(4 * scale),  int(20 * scale),   # Bottom left
    ])
    
    # Clapper coordinates
    clapper = array('B', [
        int(11 * scale), int(20 * scale),   # Top
        int(13 * scale), int(20 * scale),   # Top right
        int(14 * scale), int(24 * scale),   # Bottom right
        int(10 * scale), int(24 * scale),   # Bottom left
    ])
    
    # Sound wave lines (using array for consistency)
    left_wave = array('B', [
        int(0 * scale),  int(12 * scale),
        int(-3 * scale), int(12 * scale),
        int(-4 * scale), int(14 * scale),
        int(-3 * scale), int(16 * scale),
    ])
    
    right_wave = array('B', [
        int(24 * scale), int(12 * scale),
        int(27 * scale), int(12 * scale),
        int(28 * scale), int(14 * scale),
        int(27 * scale), int(16 * scale),
    ])
    
    # Draw the components
    display.poly(x, y, bell_body, 1, 1)  # Filled bell body
    display.poly(x, y, bell_base, 1, 1)  # Filled bell base
    display.poly(x, y, clapper, 1, 1)    # Filled clapper
    
    # Draw the sound waves
    if size >= 20:  # Only draw waves if icon is large enough
        display.poly(x, y, left_wave, 1, 0)   # Left sound wave
        display.poly(x, y, right_wave, 1, 0)  # Right sound wave
    
    # Draw the alarm time below the bell
    time_str = f"{alarm_hour:2d}:{alarm_minute:02d}"
    # Center the time string under the bell
    text_x = x + (int(24 * scale) - len(time_str) * 6) // 2
    text_y = y + int(26 * scale)
    display.text(time_str, text_x, text_y, 1)

def demo_alarm_icons(display):
    """
    Demonstrate the alarm icon at different sizes and positions
    """
    # Clear the display
    display.fill(0)
    
    # Draw three different sized bells
    draw_alarm_icon(display, 0, 0, 7, 30, size=20)    # Small bell
    draw_alarm_icon(display, 35, 0, 8, 15, size=28)   # Medium bell
    draw_alarm_icon(display, 80, 0, 6, 45, size=36)   # Large bell
    
    # Update the display
    display.show()

# Example usage:
"""
oled = ssd1306.SSD1306_SPI(128, 64, spi, DC, RES, CS)
demo_alarm_icons(oled)
"""
```