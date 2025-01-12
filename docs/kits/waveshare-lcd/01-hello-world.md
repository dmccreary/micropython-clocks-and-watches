# Waveshare Hello World

## Step 1: Load the Library

## Step 2: Load a Test Program

```py
from LCD_1inch28 import LCD_1inch28

LCD = LCD_1inch28()  
LCD.set_bl_pwm(65535)

LCD.fill(LCD.black)    
LCD.text("Hello world!", 50, 100, LCD.white)
LCD.show()
```

You should see "Hello world!" in a small white font near the center of the screen.

!!! Challenges
    1. Can you move the text around the screen by changing the x and y starting position of the text?
    2. Can you change the background fill from black to another color?
    3. Can you change the color of the text from white to be another color?
    4. Can you change the font size? (hint: this is not easy!)