import asyncio, telnetlib3

async def shell(reader, writer):
    while True:
        # read stream until '?' mark is found
        outp = await reader.read(1024)
        if not outp:
            # End of File
            break
        elif 'ok' in outp:
            # reply all questions with 'y'.
            writer.write('0A;128;128;xxx;xxx;xxx;xxx;xxx;xxx;xxx;xxx;xxx;xxx;ok')

        # display all server output
        print(outp, flush=True)

    # EOF
    print()

loop = asyncio.get_event_loop()
coro = telnetlib3.open_connection('10.42.0.111', 6023, shell=shell)
reader, writer = loop.run_until_complete(coro)
loop.run_until_complete(writer.protocol.waiter_closed)