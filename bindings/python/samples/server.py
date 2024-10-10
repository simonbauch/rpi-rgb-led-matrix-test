color1_1 = 872574
color2 = 1745404 #Das passende Orange
color3 = 1990099
fail = 1
matrixset = 0

state = True
async def shell(reader, writer):
while state:
writer.write('\r\nok\r\n')
await writer.drain()
inp = await reader.read(53)
        if fail==1: # delete Matrix in case of error 
            try:
                __dealloc__(matrix)
                fail = 0
            except:    
                fail = 0
if inp:
print(inp)
mode = inp[0:2]
@@ -142,33 +136,36 @@ async def shell(reader, writer):
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
                    if matrixset == 0:    
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
                        matrixset=1

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
                    if matrixset == 0:    
                        print("Set to small mode")
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
                        matrixset = 1
elif mode == '2C':
print("Delete Matirx")
del matrix
@@ -182,11 +179,10 @@ async def shell(reader, writer):
await writer.drain()

writer.close()
def connectionLost():
    fail=1


loop = asyncio.get_event_loop()
coro = telnetlib3.create_server(port=6023, shell=shell)
coro.connection_lost(connectionLost)
#coro.connection_lost(connectionLost)
server = loop.run_until_complete(coro)
loop.run_until_complete(server.wait_closed())