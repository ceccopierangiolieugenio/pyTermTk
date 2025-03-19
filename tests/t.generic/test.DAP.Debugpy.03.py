import asyncio
from dap import AsyncServer

async def main():
    print("Eugenio")
    server = AsyncServer("debugpy", port=64321)
    # server = AsyncServer("debugpy", port=53430)
    # server = AsyncServer("debugpy", port=12345)
    print("Parodi")
    try:
        await server.start()
        print(f"a - {server}")
    except asyncio.CancelledError:
        print(f"b - {server}")
        await server.stop()
        print(f"c - {server}")

if __name__ == "__main__":
    asyncio.run(main())
    print('END')
