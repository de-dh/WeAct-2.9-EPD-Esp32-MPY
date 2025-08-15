# WeAct-2.9-EPD-Esp32-MPY

## Summary

Example configuration of [Peter Hinch's nano-gui](https://github.com/peterhinch/micropython-nano-gui) for the WeAct Studio 2.9' Black and White E-Paper-Display for Esp32 using Micropython.
Tested on an Esp32-WROVER-E using `MicroPython v1.25.0 on 2025-04-15; Generic ESP32 module with ESP32`.
Only the neccessary files from nano-gui are included (no addidtional drivers or demo folder).


The following is demonstrated in the demo:

- Using Writer class to draw text with custom fonts and font-sizes (compiled with [Peter Hinch's font-to-py](https://github.com/peterhinch/micropython-font-to-py))
- Using primitive drawing functions of the framebuffer class (native to micropython): Text and Rects.
- Loading small [.pbm images](https://en.wikipedia.org/wiki/Netpbm) from memory.
- Updating the display's content: Showing two different screens.

## Setup

1. Download all files (except the `/doc` folder) and upload them to the root of your Micropython device.
2. Adjust the Pin configuration in `color_setup.py` to match your display.
3. Run `main.py`.


The result should look like that ("screenshots" of the display's framebuffer):

![Screenshot of the first screen.](doc/snapshot_1.jpg)
![Screenshot of the second screen.](doc/snapshot_2.jpg)
