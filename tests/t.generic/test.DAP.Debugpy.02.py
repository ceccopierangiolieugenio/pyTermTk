import asyncio
import websockets
import json


from websockets.sync.client import connect

def hello():
    print('peppo 1')
    with connect("ws://localhost:12345") as websocket:
        print('peppo 2')
        websocket.send("Hello world!")
        message = websocket.recv()
        print(f"Received: {message}")

hello()


async def dap_client():
    print('pippo1')
    async with websockets.connect("ws://localhost:12345") as websocket:
        # Initialize the debug session
        print('pippo2')
        initialize_request = {
            "seq": 1,
            "type": "request",
            "command": "initialize",
            "arguments": {}
        }
        await websocket.send(json.dumps(initialize_request))
        response = await websocket.recv()
        print("Initialize response:", response)

        # Set a breakpoint
        set_breakpoints_request = {
            "seq": 2,
            "type": "request",
            "command": "setBreakpoints",
            "arguments": {
                "source": {"path": "example.py"},
                "breakpoints": [{"line": 10}]
            }
        }
        await websocket.send(json.dumps(set_breakpoints_request))
        response = await websocket.recv()
        print("Set breakpoints response:", response)

        # Launch the debug session
        launch_request = {
            "seq": 3,
            "type": "request",
            "command": "launch",
            "arguments": {
                "program": "example.py"
            }
        }
        await websocket.send(json.dumps(launch_request))
        response = await websocket.recv()
        print("Launch response:", response)

        # Continue execution
        continue_request = {
            "seq": 4,
            "type": "request",
            "command": "continue",
            "arguments": {}
        }
        await websocket.send(json.dumps(continue_request))
        response = await websocket.recv()
        print("Continue response:", response)

asyncio.run(dap_client())
