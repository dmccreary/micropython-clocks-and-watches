# Drawing Watch Faces

An analog watch ususally has hands that
are drawn from the center to the edge
of the display.

For simple lines, we can use the display.line() function.

For thinker lines we can use the display.rect() function.

Some watches have more complex hands that are composed of 
multiple geometries such as triangles.

For most modern display drivers we can use the MicroPython poly() function to draw polygons on the screen.
These are part of the MicroPython framebuf function.

Some older drivers don't yet support these functions, so we might have to craft our own functions.

## References

[Instructables on Filled Circles and Triangles by TonyGo2](https://www.instructables.com/Drawing-Filled-Circles-and-Triangles-With-MicroPyt/)

