# Drawing Analog Hands

Drawing a analog hand requirs drawing a line from the center of the screen to a point on the
edge of the circle.  The point positon varies periodically, just like the sine and cosine
functions vary.  We can demonstrate this will a counter that goes from 0 to 360 degrees.

Consider the following:

1. Since the sine(0) = 0 we can use that function for the displacement from the center on the x-axis.
2. Since the cosine(0) = 1, we can use that as the negative Y displacement from the center.  Remember
in drawing pixels, (0,0) is in the upper-left corner of the screen.


There is one other bit of math we need to review.  The sine() and cosine() function take in a number
called ```radians``` which is usually a number between 0 and two times Pi.  They then return
a value between 0 and 1.  We need multiple both of these values by the length of the watch hand
to get to the right part of the watch face.

```py
from utime import sleep
from LCD_1inch28 import LCD_1inch28
import math

LCD = LCD_1inch28()

CENTER = 120
HAND_LENGTH = 100

# our counter will range from 0 to 59
# A full circle is 2*Pi radians
TWO_PI = 3.145175*2
counter = 0
while True:
    radians = (counter/60)*TWO_PI
    x = int(math.sin(radians)*HAND_LENGTH)
    y = -int(math.cos(radians)*HAND_LENGTH)
    print(radians, x, y)
    LCD.fill(LCD.black)
    LCD.line(CENTER, CENTER, CENTER+x,CENTER+y, LCD.white)
    LCD.show()
    sleep(1)
    counter += 1
    # if we are at 60 we start over
    if counter > 59:
        counter = 0
```

You should now see a narrow white line moving much like a second hand on a watch!

## Adding bling to your hands

Although drawing a single white line is a clean efficent design, many people like
to add other features such as an arrow head at the tip of the hand.  To do this
we can use the poly function to draw the arrow.  To get this right, we also
need to orient the arrow in the right direction.

## Drawing a Triangle

We can use the MicroPython standard [poly](https://docs.micropython.org/en/latest/library/framebuf.html) function to draw a triangle.  The poly 

```FrameBuffer.poly(x, y, coords, c[, f])``

This will draw an arbitrary polygon at the given x, y location using the given color (c).

The coords must be specified as a array of integers, e.g. array('h', [x0, y0, x1, y1, ... xn, yn]).

The optional f parameter can be set to True to fill the polygon. Otherwise just a one pixel outline is drawn.

Let's start with drawing a basic triangle in the center of the screen like this:

LCD.

```py
# draw a triangle on a blue background
from utime import sleep
from LCD_1inch28 import LCD_1inch28
import math
from array import array
LCD = LCD_1inch28()

CENTER = 120
NO_FILL = 0 # just the border is drawn
FILL = 1 # all pixels within the polygon are drawn
# draw a blue background
LCD.fill(LCD.blue)

# distance from the center to the tip of the traiangle
d = 50
my_array = array('B', [CENTER-d,CENTER+d, CENTER,CENTER-d, CENTER+d,CENTER+d])
LCD.poly(0,0, my_array, LCD.white, FILL)
LCD.show()
print('done')
```

## Drawing a Triangle Rotating

Now we will modify the draw triangle program to rotate each of the three points.
We do this by passing the CENTER and either a positve or negative value
of the x and y which varies as we move around the circle.

Here is the line that is the most difficult to understand:

```py
my_array = array('B', [CENTER-x,CENTER-y, CENTER+y,CENTER-x, CENTER+x,CENTER+y])
```

Note that the first point is in the lower left corner:

```py
(CENTER-x, CENTER-y)
```

The second point is at the top of the trainagle and the X is initially zero (sine(0) = y)

```py
(CENTER+y, CENTER-x)
```

The third point is to the lower right where we need to add to both the X and Y:

```py
(CENTER+x, CENTER-y)
```

Here is the full program:

```py
# draw rotating triangle
from utime import localtime, sleep
from LCD_1inch28 import LCD_1inch28
from array import array
import math
TWO_PI = 3.145175*2

LCD = LCD_1inch28()

CENTER = 120
NO_FILL = 0 # just the border is drawn
FILL = 1 # all pixels within the polygon are drawn

# distance from the center to the tip of the traiangle
d = 50

counter = 0
while True:
    LCD.fill(LCD.blue)
    radians = (counter/60)*TWO_PI
    x = int(math.cos(radians)*d)
    y = int(math.sin(radians)*d)
    
    # the three points of the triangle are rotated in a circle
    my_array = array('B', [CENTER-x,CENTER-y, CENTER+y,CENTER-x, CENTER+x,CENTER+y])
    print(CENTER-x, CENTER+y)
    
    LCD.poly(0,0, my_array, LCD.white, FILL)
    LCD.show()
    sleep(.1)
    counter += 1
    # if we are at 60 we start over
    if counter > 59:
        counter = 0
```

You might have to stare at the code and the drawing for a while to get this figured out.

## Create a Draw Triangle Function

Now we are ready to package our triangle drawing experiment into a single function to make
it easier to use.  We will pass in four parameters:

1. The center of the triangle's X and Y coordinates
2. The size of the triangle measured from the center to the tip
3. The number of seconds on the clock (0 to 59) which we will convert to radians.  This
becomes the agle of the triangle.

```py
def drawTriangle(x, y, size, seconds):
    radians = (seconds/60)*TWO_PI
    # calculate the offsets
    xo = int(math.cos(radians)*size)
    yo = int(math.sin(radians)*size)
    # build the array - use B if we have under 255 and h if over 255
    arr = array('B', [x-xo,y-yo,  x+yo,y-xo,  x+xo,y+yo])
    LCD.poly(0,0, arr, LCD.white, FILL)
```

## Full Program

```py
from utime import localtime, sleep
from LCD_1inch28 import LCD_1inch28
from array import array
import math
TWO_PI = 3.145175*2

LCD = LCD_1inch28()

CENTER = 120
NO_FILL = 0 # just the border is drawn
FILL = 1 # all pixels within the polygon are drawn
HAND_LENGTH = 100
TRIANGLE_SIZE = 10

def drawTriangle(x, y, size, seconds):
    radians = (seconds/60)*TWO_PI
    # calculate the offsets
    xo = int(math.cos(radians)*size)
    yo = int(math.sin(radians)*size)
    # build the array - use B if we have under 255 and h if over 255
    arr = array('B', [x-xo,y-yo,  x+yo,y-xo,  x+xo,y+yo])
    LCD.poly(0,0, arr, LCD.white, FILL)

counter = 0
while True:
    LCD.fill(LCD.blue)
    radians = (counter/60)*TWO_PI
    x = int(math.sin(radians)*HAND_LENGTH)
    y = -int(math.cos(radians)*HAND_LENGTH)
    LCD.line(CENTER, CENTER, CENTER+x,CENTER+y, LCD.white)
    drawTriangle(CENTER+x, CENTER+y, TRIANGLE_SIZE, counter)
    LCD.show()
    sleep(.1)
    counter += 1
    # if we are at 60 we start over
    if counter > 59:
        counter = 0```

## Drawing X and Y Axis

```py
# draw thin blue axis lines through the center
# vertical line
LCD.line(CENTER, 0, CENTER, 2*CENTER, blue)
# horizontal line
LCD.line(0, CENTER, 2*CENTER, CENTER, blue)
```