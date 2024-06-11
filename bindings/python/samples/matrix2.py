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
x1 = 1
y1 = 1
x2 = 32
y2 = 16
color1 = 16448250
color2 = 16333250
while True:
    x1=x1+1
    y1=y1+1
    if x1==64:
        x1=1
    if y1==64:
        y1=1
    x1=x1+1
    x2=x2+1
    y2=y2+1
    if x2==64:
        x2=1
    if y2==64:
        y2=1
    matrix.Clear()
    matrix.SetPixelstwoCrosshair(x1,y1,x2,y2,color1,color2)
    time.sleep(0.01)

try:
    print("Press CTRL-C to stop.")
    while True:
        time.sleep(100)
except KeyboardInterrupt:
    sys.exit(0)
