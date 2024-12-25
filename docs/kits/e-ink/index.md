# E-Ink Displays

!!! prompt
    Please suggest a low-cost e-ink display that has strong support for a microPython driver.

    ChatGPT

    Thought about e-ink display and MicroPython for 5 seconds

    If you're looking for a budget-friendly e-ink module that's well-documented and easy to use in MicroPython projects, a great place to start is with the smaller Waveshare e-Paper displays. Specifically, the **Waveshare 1.54-inch e-Paper** module is often cited for its low cost and good MicroPython support. Here are some details:

# ChatGPT Response

1) Waveshare 1.54-inch e-Paper Module

**Why it's a good pick**

-   **Affordability**: Often in the $15--$25 range, depending on where you purchase.
-   **MicroPython libraries**: Strong community support and official Waveshare repositories on GitHub. There are also third-party MicroPython drivers floating around that make it easier to integrate.
-   **Multiple variants**: You can find "red/black/white" or "black/white" only variants. The simpler (black/white) ones tend to be cheaper.
-   **Low power consumption**: Typical for e-ink, so it's great for battery-powered projects.

**Where to find drivers**

-   [Waveshare's official GitHub](https://github.com/waveshare) has examples in C, Arduino, and sometimes MicroPython.
-   Look for community forks or repos titled similarly to `micropython-waveshare-epaper` (there are a few) for more up-to-date drivers.

**Key specs**

-   Resolution: ~200 × 200 pixels (for the 1.54" black/white version)
-   Interfaces: SPI, typically 3.3 V (works well with ESP8266, ESP32, etc.)
-   Refresh time: ~2 seconds for a full refresh; partial refresh also possible on some models.

* * * *

2) Waveshare 2.13-inch e-Paper (Slightly Larger Option)
-------------------------------------------------------

If you need a bit more display real estate, the **2.13-inch** Waveshare e-Paper module is another solid choice. It's still relatively low cost (somewhere around $25--$30) but gives you higher resolution (around 250 × 122 or 212 × 104, depending on the version) for more text or small graphics.

-   Strong MicroPython support (similarly to the 1.54-inch).
-   Typically uses the same library approach from Waveshare, so upgrading the size is straightforward.

* * * *

3) LilyGo T5 Series (All-in-One Board)
--------------------------------------

Another cost-effective route (if you don't mind an all-in-one solution rather than a separate module) is the **LilyGo T5** board series. These boards come with an ESP32 already integrated and a small e-ink display (like 1.54", 2.13", 2.7", 4.7" versions).

-   Pros:
    -   ESP32 + e-ink combined in one board
    -   Some have built-in battery circuitry
    -   Often includes MicroPython support or ready-to-flash firmware
-   Cons:
    -   Slightly more expensive than just a raw display
    -   Tied to LilyGo's board layout and pins

If you already have a microcontroller board and want to keep costs low, a stand-alone Waveshare display will likely be cheaper. However, if you're starting from scratch, the LilyGo T5 might save you some setup time (fewer wiring hassles, etc.).

* * * *

Summary
-------

-   **Best Overall Low-Cost**:
    **Waveshare 1.54-inch e-Paper** module. It's consistently among the cheapest e-ink modules, with decent resolution for text/graphics and ample MicroPython support from both the official Waveshare examples and the community.

-   **Slightly Larger Screen**:
    **Waveshare 2.13-inch e-Paper** offers more room but at a slightly higher price.

-   **All-in-One Alternative**:
    **LilyGo T5** boards combine an ESP32 and e-ink, and often come with MicroPython pre-installed or easily flashed.

All of these displays have active communities, plenty of tutorials, and code examples you can adapt for MicroPython, making them a great fit if you're just getting started with e-ink in your microcontroller projects.

o1