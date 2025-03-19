import asyncio
from dap_python import DebugAdapterClient

async def main():
    # Create a Debug Adapter Client
    client = DebugAdapterClient()

    # Connect to the debug server
    await client.connect('localhost', 5678)

    # Initialize the debug session
    await client.initialize()

    # Set a breakpoint
    await client.set_breakpoints('example.py', [10])

    # Launch the debug session
    await client.launch({
        'program': 'example.py'
    })

    # Continue execution
    await client.continue_()

    # Wait for the debug session to end
    await client.wait_for_termination()

# Run the main function
asyncio.run(main())
