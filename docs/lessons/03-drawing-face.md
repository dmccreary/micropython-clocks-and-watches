# Drawing Watch Faces

An analog watch ususally has hands that
are drawn from the center to the edge
of the display.

The lines or marks that indicate the hours are often referred to as "hour indices" or "hour markers."

The smaller lines that indicate the minutes are called "minute indices" or "minute markers."

For simple lines, we can use the ```line(x1,y1, x2,y2,color)``` function which draws
a sinle pixel line from the starting point at (x1,y1) to the end pint at (x2,y2) using the fifth
color parameter.  For monochrome clocks the color 1 is whtie and 0 is black.

For thinker lines we can use the display.rect() function.

Some watches have more complex hands that are composed of 
multiple geometries such as triangles.

For most modern display drivers we can use the MicroPython poly() function to draw polygons on the screen.
These are part of the MicroPython framebuf function.

Some older drivers don't yet support these functions, so we might have to craft our own functions.

## References

[Instructables on Filled Circles and Triangles by TonyGo2](https://www.instructables.com/Drawing-Filled-Circles-and-Triangles-With-MicroPyt/)

