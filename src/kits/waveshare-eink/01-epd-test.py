import pycom
pycom.heartbeat(False)

from machine import Pin
import epd1in54b

mosi = Pin(0)
clk = Pin(1)
reset = Pin(2)
dc = Pin(3)
busy = Pin(4)
cs = Pin(5)



epd = epd1in54b.EPD(reset, dc, busy, cs, clk, mosi)
epd.init()

# initialize the frame buffer
fb_size = int(epd.width * epd.height / 8)
frame_black = bytearray(fb_size)
frame_red = bytearray(fb_size)

epd.clear_frame(frame_black, frame_red)

# For simplicity, the arguments are explicit numerical coordinates
epd.draw_rectangle(frame_black, 10, 60, 50, 110, epd1in54b.COLORED)
epd.draw_line(frame_black, 10, 60, 50, 110, epd1in54b.COLORED)
epd.draw_line(frame_black, 50, 60, 10, 110, epd1in54b.COLORED)
epd.draw_circle(frame_black, 120, 80, 30, epd1in54b.COLORED)
epd.draw_filled_rectangle(frame_red, 10, 130, 50, 180, epd1in54b.COLORED)
epd.draw_filled_rectangle(frame_red, 0, 6, 200, 26, epd1in54b.COLORED)
epd.draw_filled_circle(frame_red, 120, 150, 30, epd1in54b.COLORED)

# write strings to the buffer
epd.display_string_at(frame_red, 48, 10, "e-Paper Demo", font12, epd1in54b.UNCOLORED)
epd.display_string_at(frame_black, 20, 30, "Hello Pycom!", font20, epd1in54b.COLORED)
# display the frame
epd.display_frame(frame_black, frame_red)
