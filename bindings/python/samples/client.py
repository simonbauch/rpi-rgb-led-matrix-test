import asyncio, telnetlib3
import time


async def shell(reader, writer):
    x1 = 0
    y1 = 0
    while True:
        # read stream until '?' mark is found
        outp = await reader.read(1024)
        if not outp:
            # End of File
            break
        elif 'ok' in outp:
            
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
            
            out = "0B;"+x1s+";"+y1s+";060;100;xxx;xxx;xxx;xxx;xxx;xxx;xxx;xxx;ok"
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
            time.sleep(0.05)
                

        # display all server output
        print(outp, flush=True)

    # EOF
    print()

loop = asyncio.get_event_loop()
coro = telnetlib3.open_connection('10.42.0.111', 6023, shell=shell)
reader, writer = loop.run_until_complete(coro)
loop.run_until_complete(writer.protocol.waiter_closed)