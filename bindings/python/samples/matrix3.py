#!/usr/bin/env python
import time
import sys

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image

# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 32
options.cols = 32
options.chain_length = 14
options.parallel = 3
options.hardware_mapping = 'regular' # If you have an Adafruit HAT: 'adafruit-hat'
options.gpio_slowdown = 4  
options.multiplexing = 1
options.pixel_mapper_config = "U-mapper"

matrix = RGBMatrix(options = options)

# Make image fit our screen.
x1 = 100
y1 = 100
x2 = 125
y2 = 125
x3 = 0
y3 = 0
color1 = 16448250
color2 = 1745404 #Das passende Orange
color3 = 1745404 #Das passende Orange


matrix.SetPixelsthreeCrosshairsmall(x1,y1,x2,y2,x3,x3,color1,color2,color3)
try:
    print("Press CTRL-C to stop.")
    while True:
        time.sleep(100)
except KeyboardInterrupt:
    sys.exit(0)
