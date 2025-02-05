## Architectural  Levels Zoom

[P5.js Version](./main.html)

[React Main](./react.html)

!!! prompt
    Create a MicroSim that shows different levels of Zoom. The highest level shows a single component and as you increase the Zoom level it shows more components.

    Level 1: Just the Clock as a rectangle centered on the canvas with the label "Clock" in a large font in the center Level 2: The architecture drawing now shows two rectangular components: a "Display" at the top and "Microcontroller" at the bottom. Each has a label in the center Level 3: The architecture show shows three components: The Display, the "SPI Bus "(as a vertical double sided arrow) and the "Microcontroller" below Level 4: The architecture now shows a "Display", "SPI Bus", "MicroController" and the "RTC" to the right of the Microcontroller Level 5: Same as Level 4 but add a "I2C Bus" between the "Microcontroller" and the "RTC" Level 6: Same as Level 5 but now add "Buttons" to the left of the "MicroContoller" Level 7: Same as Level 6 but now add "Power" below all the components Level 8: Same as Level 7 but now add "Speaker" to the left of the "Microcontroller" Level 9: Same as level 8 but now show the "Microcontroller" as also having "Core 1" and "Core 2" inside of it Level 10" Same as Level 9 but now have PIO as an additional component within the "Microcontroller"

## Response

I'll help create a MicroSim that shows different architectural zoom levels of your clock system. I'll use React with SVG for the visualization and add a slider to control the zoom level.

I've created an interactive visualization that shows the clock architecture at different zoom levels. You can use the slider at the bottom to adjust the zoom level from 1-10, revealing more details of the system architecture at each level:

1. Level 1 shows just the basic clock component
2. Level 2 adds the Display and Microcontroller
3. Level 3 shows the SPI bus connection
4. Level 4 adds the RTC component
5. Level 5 shows the I2C bus connection to the RTC
6. Level 6 adds the Buttons
7. Level 7 adds the Power system
8. Level 8 includes the Speaker
9. Level 9 shows the dual cores inside the Microcontroller
10. Level 10 adds the PIO within the Microcontroller

The visualization uses SVG for crisp rendering at any scale and includes:
- Color-coded components
- Labeled connections
- Proper arrow markers for buses
- A responsive layout that centers in the available space
- Smooth transitions between levels

You can adjust the zoom level using the slider below the diagram. Would you like me to modify any aspects of the visualization?