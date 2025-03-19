import asyncio
from dap import AsyncServer

async def debug_session():
    server = AsyncServer("debugpy", port=12345)
    await server.start()
    client = server.client

    client.launch()
    client.disconnect()
    server.stop()

asyncio.run(debug_session())
