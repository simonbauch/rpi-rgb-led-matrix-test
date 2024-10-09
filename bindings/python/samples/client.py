import asyncio, telnetlib3
import time


async def shell(reader, writer):
    x1 = 0
    y1 = 0
    x2 = 100
    y2 = 20
    x3 = 66
    y3 = 88
    mode = 2
    while True:
        # read stream until '?' mark is found
        outp = await reader.read(1024)
        if not outp:
            # End of File
            break
        elif 'ok' in outp:
            if mode == 0: 
                if x1<10:       #Daten ins Format bringen
                    x1s="00"+str(x1)
                elif x1<100:
                    x1s="0"+str(x1)
                else:
                    x1s=str(x1)
                if y1<10:
                    y1s="00"+str(y1)
                elif y1<100:
                    y1s="0"+str(y1)
                else:
                    y1s=str(y1)
            
                if x2<10:       #Daten ins Format bringen
                    x2s="00"+str(x2)
                elif x2<100:
                    x2s="0"+str(x2)
                else:
                    x2s=str(x2)
                if y2<10:
                    y2s="00"+str(y2)
                elif y2<100:
                    y2s="0"+str(y2)
                else:
                    y2s=str(y2)
            
                if x3<10:       #Daten ins Format bringen
                    x3s="00"+str(x3)
                elif x3<100:
                    x3s="0"+str(x3)
                else:
                    x3s=str(x3)
                if y3<10:
                    y3s="00"+str(y3)
                elif y3<100:
                    y3s="0"+str(y3)
                else:
                    y3s=str(y3)
            
                out = "0C;"+x1s+";"+y1s+";"+x2s+";"+y2s+";"+x3s+";"+y3s+";xxx;xxx;xxx;xxx;xxx;xxx;ok"
                print(out)
                writer.write(out)
                if  x1 > 224:
                    x1=0
                else:
                    x1 = x1 + 1
                if  y1 > 160:
                    y1=0
                else:
                    y1 = y1 + 1
            
                if  x2 > 224:
                    x2=0
                else:
                    x2 = x2 + 1
                if  y2 > 160:
                    y2=0
                else:
                    y2 = y2 + 1
            
                if  x3 > 224:
                    x3=0
                else:
                    x3 = x3 + 1
                if  y3 > 160:
                    y3=0
                else:
                    y3 = y3 + 1
                #time.sleep(0.05)

            elif mode == 1: #Change / Set colors 
                mode = 0
                color1 = 9999999
                color2 = 872574
                color3 = 100909
                color1_s = "000000000000"+str(color1)
                color2_s = "000000000000"+str(color2)
                color3_s = "000000000000"+str(color3)
                lenght1 = len(color1_s)
                lenght2 = len(color2_s)
                lenght3 = len(color3_s)
                data1 = color1_s[lenght1-3:lenght1]
                data2 = color1_s[lenght1-6:lenght1-3]
                data3 = color1_s[lenght1-9:lenght1-6]
                data4 = color1_s[lenght1-12:lenght1-9]
                print (data1)
                print (data2)
                print (data3)
                print (data4)
                data5 = color2_s[lenght2-3:lenght2]
                data6 = color2_s[lenght2-6:lenght2-3]
                data7 = color2_s[lenght2-9:lenght2-6]
                data8 = color2_s[lenght2-12:lenght2-9]
                print (data5)
                print (data6)
                print (data7)
                print (data8)
                data9 = color3_s[lenght3-3:lenght3]
                data10 = color3_s[lenght3-6:lenght3-3]
                data11 = color3_s[lenght3-9:lenght3-6]
                data12 = color3_s[lenght3-12:lenght3-9]
                print (data9)
                print (data10)
                print (data11)
                print (data12)
                out = "1A;"+data1+";"+data2+";"+data3+";"+data4+";"+data5+";"+data6+";"+data7+";"+data8+";"+data9+";"+data10+";"+data11+";"+data12+";ok"
                print(out)
                writer.write(out)
            elif mode == 2: #Set panel size: 2A: Large 2B:Small
                mode = 1
                out = "2A;xxx;xxx;xxx;xxx;xxx;xxx;xxx;xxx;xxx;xxx;xxx;xxx;ok"
                print(out)
                writer.write(out)
            elif mode == 3: #Reset / Delete Panel class 
                mode = 1
                out = "2C;xxx;xxx;xxx;xxx;xxx;xxx;xxx;xxx;xxx;xxx;xxx;xxx;ok"
                print(out)
                writer.write(out)
        # display all server output
        print(outp, flush=True)

    # EOF
    print()

loop = asyncio.get_event_loop()
coro = telnetlib3.open_connection('10.42.0.105', 6023, shell=shell)
reader, writer = loop.run_until_complete(coro)
loop.run_until_complete(writer.protocol.waiter_closed)