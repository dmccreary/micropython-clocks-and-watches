from machine import Pin,I2C,SPI,PWM,ADC
import framebuf
import time
from LCD_1inch28 import LCD_1inch28, QMI8658

LCD = LCD_1inch28()
LCD.set_bl_pwm(65535)
qmi8658=QMI8658()
Vbat_Pin = 29
Vbat= ADC(Pin(Vbat_Pin))   

while(True):
    #read QMI8658
    xyz=qmi8658.Read_XYZ()
    
    LCD.fill(LCD.white)
    
    LCD.fill_rect(0,0,240,40,LCD.red)
    LCD.text('RP2040 1.28"',60,25,LCD.white)
    
    LCD.fill_rect(0,40,240,40,LCD.blue)
    LCD.text("Dan McCreary MicroPython",25,57,LCD.white)
    
    LCD.fill_rect(0,80,120,120,0x1805)
    LCD.text("ACC_X={:+.2f}".format(xyz[0]),20,100-3,LCD.white)
    LCD.text("ACC_Y={:+.2f}".format(xyz[1]),20,140-3,LCD.white)
    LCD.text("ACC_Z={:+.2f}".format(xyz[2]),20,180-3,LCD.white)

    LCD.fill_rect(120,80,120,120,0xF073)
    LCD.text("GYR_X={:+3.2f}".format(xyz[3]),125,100-3,LCD.white)
    LCD.text("GYR_Y={:+3.2f}".format(xyz[4]),125,140-3,LCD.white)
    LCD.text("GYR_Z={:+3.2f}".format(xyz[5]),125,180-3,LCD.white)
    
    LCD.fill_rect(0,200,240,40,0x180f)
    reading = Vbat.read_u16()*3.3/65535*2
    LCD.text("Vbat={:.2f}".format(reading),80,215,LCD.white)
    
    LCD.show()
    time.sleep(0.1)
