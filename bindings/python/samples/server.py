#!/usr/bin/env python
import time
import sys
import asyncio, telnetlib3

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

color1 = 1745404
color1_1 = 872574
color2 = 1745404 #Das passende Orange
color3 = 345212


state = True
async def shell(reader, writer):
    while state:
        writer.write('\r\nok\r\n')
        await writer.drain()
        inp = await reader.read(53)
        if inp:
            print(inp)
            mode = inp[0:2]
            print(mode)
            data1 = inp[3:6]
            print(data1)
            data2 = inp[7:10]
            print(data2)
            data3 = inp[11:14]
            print(data3)
            data4 = inp[15:18]
            print(data4)
            data5 = inp[19:22]
            print(data5)
            data6 = inp[23:26]
            print(data6)
            data7 = inp[27:30]
            print(data7)
            data8 = inp[31:34]
            print(data8)
            data9 = inp[35:38]
            print(data9)
            data10 = inp[39:42]
            print(data10)
            data11 = inp[43:46]
            print(data11)
            data12 = inp[47:50]
            print(data12)
            flag = inp[51:53]
            print(flag)
            if flag =='ok':  #Transmission mostly ok
                if mode == '0A':  #switch cases
                    #code for singel crosshair here
                    print('singl')
                    x1 = int(data1)
                    y1 = int(data2)
                    print(x1)
                    print(y1)
                    #matrix.Clear()
                    #matrix.SetPixelsCrosshair(x1-1, y1-1,color1_1)
                    matrix.SetPixelsCrosshair(x1, y1,color1)
                    #matrix.SetPixelsCrosshair(x1+1, y1+1,color1_1)
                    time.sleep(0.02)

                elif mode == '0B':
                    #code for double crosshair here
                    print('double')
                    x1 = int(data1)
                    y1 = int(data2)
                    x2 = int(data3)
                    y2 = int(data4)
                    print(x1)
                    print(y1)
                    print(x2)
                    print(y2)
                    matrix.Clear()
                    matrix.SetPixelstwoCrosshair(x1,y1,x2,y2,color1,color1_1)
                    time.sleep(0.01)
                elif mode == '0C':
                    #code for tripple crosshair here
                    
                    print('tripple')
                elif mode == '1A':
                    #code for farbsetzten here
                    print('color')
                elif mode == '00':
                    #code for test here
                    print('test')
                else:
                    print('command error')
                    writer.write('\r\ncommandfailok\r\n')
                    await writer.drain()
            else:
                print('command / data error')
                writer.write('\r\ncommandfailok\r\n')
                await writer.drain()


                

            
    writer.close()

loop = asyncio.get_event_loop()
coro = telnetlib3.create_server(port=6023, shell=shell)
server = loop.run_until_complete(coro)
loop.run_until_complete(server.wait_closed())