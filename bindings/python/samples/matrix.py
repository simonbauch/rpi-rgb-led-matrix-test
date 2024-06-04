#!/usr/bin/env python
import time
import sys

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image

# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 32
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'regular' # If you have an Adafruit HAT: 'adafruit-hat'
options.gpio_slowdown = 4  
options.multiplexing=1

matrix = RGBMatrix(options = options)

# Make image fit our screen.
x = 1
y = 1
while True:
    x=x+1
    y=y+1
    if x==32:
        x=1
    if y==32:
        y=1
    matrix.SetPixelsCrosshair(x, y)
    time.sleep(100)

try:
    print("Press CTRL-C to stop.")
    while True:
        time.sleep(100)
except KeyboardInterrupt:
    sys.exit(0)
