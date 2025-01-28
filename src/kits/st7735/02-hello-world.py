# ST7735 LCD Test
import machine
import ST7735

spi = machine.SPI(0, baudrate=8000000)
d = ST7735.ST7735(spi, rst=4, ce=6, dc=5)
d.reset()
d.begin()
d.set_rotation(1)
d._bground = 0xffff
 # white
d.fill_screen(d._bground)
 # make background all white
d._color = 0x0000 # black ink
d.p_string(10,10,'Hello World!')

