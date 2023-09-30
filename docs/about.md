# About the Clock and Watches Project

## Early Arduino Beginnings
I have been building clock and time related projects for the Twin Cities CoderDojo
group since 2013.  We started building simple stopwatches using the $32 Arduino
Uno microcontrollers that used seven-segment displays.  Our stopwatch lab
was very popular.

When we tried to use
the graphic displays, we frequently ran into the framebuffer memory limitation
of the Arduino at 2K.

We also tried to use LCD displays to show the time and date.  These displays
suffer from the fact that as the voltage of the battery drops, the screen
contrast also needs to constantly be adjusted.

These devices had to be programmed using "C".  Although C is popular
among people with a strong computer science background, we found
that most of our students wnated to learn Python.  That became
the most popular computer language for students [around 2017](https://flatironschool.com/blog/python-popularity-the-rise-of-a-global-programming-language/).

It was truly difficult for us to adapt to this change back in 2018.  We tried
many options to make C and Arduino more acceptable to our students.  But
in 2020 we finally started to convert all our old Arduino lesson plans
to use [Python](https://www.coderdojotc.org/python/) and [MicroPython](https://www.coderdojotc.org/micropython/).

## The Pico Revolution

All this [changed radically](https://dmccreary.medium.com/how-a-small-charity-is-upsetting-the-trillion-dollar-silicon-chip-industry-ad8062e8c627) when we started to use the Raspberry Pi Pico in [March of 2021](https://www.raspberrypi.com/news/raspberry-pi-pico-vertical-innovation/).
The Pico had a wopping 264K or about 100x the memory of the Adruino Uno.  This
allowed us to start to use low-cost OLED displays.  The $4 price point was
also about 1/5th of what were were paying for the Arduino Uno.  Finally
we had an easy-to-use Python environment that didn't require long compilation.
The kids LOVED this new system.

## The Thonny IDE

The Raspberry Pi Foundation also promoted (and funded) a simple Integrated Development Envionrment (IDE) called [Thonny](https://thonny.org/).  Thonny allows us to simply plug the board into a USB and it will "almost" automatilly
download the right Raspberry Pi firmware to get students started quickly. We highly recommend Thonny in
all our coding clubs.

## Syncronizing Clocks with the Pico W using WiFi

Our clocks were wonderful to watch but the time had to be set manually when they were not hooked up to
a USB port of a computer running Thonny.  This all changed with the Raspberry Pi Foundation
released the [Raspberry Pi Pico](https://www.raspberrypi.com/news/raspberry-pi-pico-w-your-6-iot-platform/) in the summer of 2022.

The $6 Pico W board finally started to catch up with the incumbent [ESP-32](https://en.wikipedia.org/wiki/ESP32) series
of microcontrollers that had supported WiFi.  The ESP-32 was the sucessor to the groundbreaking [ESP8266](https://en.wikipedia.org/wiki/ESP8266) that was introduce way back in Auguest of 2014.  We have several advanced students that use these
processors, but they do require you to use much more advanced toolchains.

## Progess in Better Displays

Unfortunatly, the under 1-inch OLED displays that were low-cost were often too small to read
from more than a few feet away.  We started to purchase the 2.24" OLEDs and we started
to have lots of great feedback by these large, bright high-contrast displays.  As a rule,
we now only include displays that are 2-inches or higher.

In the past 10-years the Smart Watch industry pushed manufactures to build lower-cost displays that
were over two inches and also included 16-bit color.  The key limitation with most of these
displays is that they only run on slow SPI interfaces.  When the drivers
required that every pixel on the screen is updated, to make even a small single pixel change
we need to deal with slower drawing times and flicker.

Now companies like Lilygo have figured out how to increase the speed of the slower SPI
interfaces to provide great flicker-free draw times.  Draw times on the
Liligo displays are well over our 30-frames-per second goal.

Although we still struggle with some limitations of slower SPI, memory and buggy micropython
drivers that don't take advantage
of the chips that drive the displays, we are well on our way to allowing
all students to customizd their own clocks and watches with MicroPython.

## I2C vs SPI

I should also mention that there are also displays that use I2C interfaces.  These
interfaces are ideal when you don't have fast drawing requirements since they only
use four wires.  These are easier for students to connect.  SPI interfaces
requred up to 7-wires that make them harder for students with old breadboards
where the wires come lose.  We overcame this by providing a small wire harness
that uses a Dupont ribbon cable that is hot-glued on both ends to prevent the wires
from coming lose.

## Where We Are Today

Althoug there are now some complete watches you can purchase that can be
worn on your wrist, the Python tools are not yet easy to use.  We still
lack a consitent way of manageing mutiple size fonts in the MicroPython
runtime and there are many different drawing primitives in older
display drivers that have not upgraded to the version 20 runtime.
But I think we have made great progress over the last two years and
I look forward to the day where many of our students are
wearing watches that they can customize with Python!

If you have any ideas on how we can get low-cost but fun projects into our
MicroPython classrooms, please let us know!  My LinkedIn account is below:

- [Dan McCreary on LinkedIn](https://www.linkedin.com/in/danmccreary/)