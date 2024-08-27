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
options.drop_privileges=False

matrix = RGBMatrix(options = options)

color1 = 1745005
color1_1 = 872574
color2 = 1745404 #Das passende Orange
color3 = 1990099


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
                    matrix.Clear()
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
                    x1 = int(data1)
                    y1 = int(data2)
                    x2 = int(data3)
                    y2 = int(data4)
                    x3 = int(data5)
                    y3 = int(data6)
                    print(x1)
                    print(y1)
                    print(x2)
                    print(y2)
                    print(x3)
                    print(y3)
                    matrix.Clear()
                    matrix.SetPixelsthreeCrosshair(x1,y1,x2,y2,x3,y3,color1,color2,color3)
                    time.sleep(0.01)
                elif mode == '1A':
                    color_1set = data4+data3+data2+data1
                    color_2set = data8+data7+data6+data5
                    color_3set = data12+data11+data10+data9
                    color1 = int(color_1set)
                    color2 = int(color_2set)
                    color3 = int(color_3set)
                    print('color')
                    print(color1)
                    print(color2)
                    print(color3)
                elif mode == '00':
                    #code for test here
                    print('test')
                    x = 1
                    y = 1
                    color_tst = 1745404 #das oragne
                    while x<223 and y<159:
                        x=x+1
                        y=y+1
                        if x==224:
                            x=1
                        if y==160:
                            y=1
                        matrix.Clear()
                        matrix.SetPixelsCrosshair(x, y,color_tst)
                        time.sleep(0.01)
                elif mode == '2A':
                    print("Set large Mode")
                    options2 = RGBMatrixOptions()
                    options2.rows = 32
                    options2.cols = 32
                    options2.chain_length = 14
                    options2.parallel = 3 #
                    options2.hardware_mapping = 'regular' # If you have an Adafruit HAT: 'adafruit-hat'
                    options2.gpio_slowdown = 4  
                    options2.multiplexing = 1
                    options2.pixel_mapper_config = "U-mapper"
                    options2.drop_privileges=True
                    matrix = RGBMatrix(options = options2)
                    
                elif mode == '2B':
                    print("Set to small mode")
                    #MAtrix zerstören und mit neuen Options erneut erstellen
                    options3 = RGBMatrixOptions()
                    options3.rows = 32
                    options3.cols = 32
                    options3.chain_length = 10
                    options3.parallel = 3 #
                    options3.hardware_mapping = 'regular' # If you have an Adafruit HAT: 'adafruit-hat'
                    options3.gpio_slowdown = 4  
                    options3.multiplexing = 1
                    options3.pixel_mapper_config = "U-mapper"
                    options3.drop_privileges=True
                    matrix = RGBMatrix(options = options3)
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