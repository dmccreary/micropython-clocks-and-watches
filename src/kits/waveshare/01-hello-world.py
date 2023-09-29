from utime import localtime, sleep
from LCD_1inch28 import LCD_1inch28

LCD = LCD_1inch28()
# turn the backlight on max
LCD.set_bl_pwm(65535)

# make the background black
LCD.fill(LCD.black)
# put the string "Hello world!" in the frame buffer at x=50 and y=100
LCD.text("Hello world!", 50, 100, LCD.white)
# copy the frame buffer to the screen
LCD.show()
