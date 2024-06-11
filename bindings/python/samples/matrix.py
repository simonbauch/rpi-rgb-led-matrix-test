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
x = 1
y = 1
color = 16448250
while True:
    x=x+1
    y=y+1
    if x==64:
        x=1
    if y==64:
        y=1
    matrix.Clear()
    matrix.SetPixelsCrosshair(x, y,color)
    time.sleep(0.01)

try:
    print("Press CTRL-C to stop.")
    while True:
        time.sleep(100)
except KeyboardInterrupt:
    sys.exit(0)
