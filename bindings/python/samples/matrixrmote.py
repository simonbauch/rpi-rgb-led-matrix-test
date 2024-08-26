#!/usr/bin/env python
import time
import sys
import asyncio, telnetlib3

from rgbmatrix import RGBMatrix, RGBMatrixOptions

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

x1 = 10
y1 = 10
x2 = 125
y2 = 125
color1 = 16448250
color2 = 1745404 #Das passende Orange

matrix.SetPixelstwoCrosshair(x1,y1,x2,y2,color1,color2)

async def shell(reader, writer):
    writer.write('\r\nWould you like to play a game? ')
    inp = await reader.read(1)
    if inp:
        writer.echo(inp)
        writer.write('\r\nThey say the only way to win '
                     'is to not play at all.\r\n')
        await writer.drain()
    writer.close()

loop = asyncio.get_event_loop()
coro = telnetlib3.create_server(port=6023, shell=shell)
server = loop.run_until_complete(coro)
loop.run_until_complete(server.wait_closed())

try:
    print("Press CTRL-C to stop.")
    while True:
        time.sleep(100)
except KeyboardInterrupt:
    sys.exit(0)
