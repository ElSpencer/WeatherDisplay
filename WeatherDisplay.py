#!/usr/bin/env python3
import sys
import time

from PIL import Image, ImageDraw, ImageFont

import st7789

MESSAGE = "Hello World! How are you today?"

print(
    f"""
scrolling-test.py - Display scrolling text.

If you're using Breakout Garden, plug the 1.3" LCD (SPI)
breakout into the front slot.

Usage: {sys.argv[0]} "<message>" <display_type>

Where <display_type> is one of:

  * square - 240x240 1.3" Square LCD
  * round  - 240x240 1.3" Round LCD (applies an offset)
  * rect   - 240x135 1.14" Rectangular LCD (applies an offset)
  * dhmini - 320x240 2.0" Display HAT Mini
"""
)

# try:
#     MESSAGE = sys.argv[1]
# except IndexError:
#     pass

try:
    display_type = sys.argv[1]
except IndexError:
    display_type = "square"


# Create ST7789 LCD display class.

if display_type in ("square", "rect", "round"):
    disp = st7789.ST7789(
        height=135 if display_type == "rect" else 240,
        rotation=0 if display_type == "rect" else 90,
        port=0,
        cs=st7789.BG_SPI_CS_FRONT,  # BG_SPI_CS_BACK or BG_SPI_CS_FRONT
        dc=9,
        backlight=19,  # Breakout Garden: 18 for back slot, 19 for front slot.
                       # NOTE: Change this to 13 for Pirate Audio boards
        spi_speed_hz=80 * 1000 * 1000,
        offset_left=0 if display_type == "square" else 40,
        offset_top=53 if display_type == "rect" else 0,
    )

elif display_type == "dhmini":
    disp = st7789.ST7789(
        height=240,
        width=320,
        rotation=180,
        port=0,
        cs=1,
        dc=9,
        backlight=13,
        spi_speed_hz=60 * 1000 * 1000,
        offset_left=0,
        offset_top=0,
    )

else:
    print("Invalid display type!")

# Initialize display.
disp.begin()

WIDTH = disp.width
HEIGHT = disp.height


img = Image.new("RGB", (WIDTH, HEIGHT), color=(0, 0, 0))

draw = ImageDraw.Draw(img)

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)

#size_x, size_y = textsize(MESSAGE, font)
#
# text_x = disp.width
# text_y = (disp.height - size_y) // 2
#getting the starting points for the three lines
third = disp.width/3
l1_y=0
l2_y=third
l3_y = 2*third

#getting the text for the three lines
l1_text = "28.8"
l2_text = "56.3 %"
l3_text = "12 kPa"
while True:
    draw.rectangle((0, 0, disp.width, disp.height), (0, 0, 0))
    draw.text((0, l1_y), l1_text, font=font, fill=(255, 255, 255))
    draw.text((0, l2_y), l2_text, font=font, fill=(255, 255, 255))
    draw.text((0, l3_y), l3_text, font=font, fill=(255, 255, 255))
    disp.display(img)
# t_start = time.time()
#
# while True:
#     x = (time.time() - t_start) * 100
#     x %= size_x + disp.width
#     draw.rectangle((0, 0, disp.width, disp.height), (0, 0, 0))
#     draw.text((int(text_x - x), text_y), MESSAGE, font=font, fill=(255, 255, 255))
#     disp.display(img)
