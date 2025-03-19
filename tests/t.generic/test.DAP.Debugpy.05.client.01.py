import asyncio
import json
import re

async def send_request(writer, request):
    content = json.dumps(request)
    header = f"Content-Length: {len(content)}\r\n\r\n"
    message = header + content
    print("Sending:")
    print("  header:", header)
    print("  content:", content)
    writer.write(message.encode('utf-8'))
    await writer.drain()


header_re = re.compile(r'^Content-Length: (\d+)[\r\n]*', re.MULTILINE)

async def receive_response(reader):
    response = await reader.read(4096)
    response_string = response.decode('utf-8')
    while m:=header_re.search(response_string):
        header = m.group(0)
        header_length = len(header)
        content_length = int(m.group(1))
        content = response_string[header_length:header_length+content_length]
        response_string = response_string[header_length+content_length:]
        print("Received:")
        print("  header length:", header_length)
        # print("  content:", content)
        print("  json:", json.loads(content))
    return {}

async def main():
    host = 'localhost'
    port = 64321

    reader, writer = await asyncio.open_connection(host, port)
    print("Connected to the debug adapter server.")

    # Example request: Initialize
    initialize_request = {
        'seq': 1,
        'type': 'request',
        'command': 'initialize',
        'arguments': {
            'clientID': 'example-client',
            'adapterID': 'debugpy',
            'pathFormat': 'path',

            "locale": "en",

            'linesStartAt1': True,
            'columnsStartAt1': True,

            'supportsVariableType': True,
            'supportsVariablePaging': True,
            'supportsRunInTerminalRequest': True,
            "supportsRunInTerminalRequest": True,
            "supportsProgressReporting": True,
            "supportsInvalidatedEvent": True,
            "supportsMemoryReferences": True,
            "supportsArgsCanBeInterpretedByShell": True,
            "supportsMemoryEvent": True,
            "supportsStartDebuggingRequest": True,
            "supportsANSIStyling": True
        }
    }

    await send_request(writer, initialize_request)
    response = await receive_response(reader)
    print("Response 1:", response)

    response = await receive_response(reader)
    print("Response 2:", response)

    response = await receive_response(reader)
    print("Response 3:", response)

    # Close the connection
    writer.close()
    await writer.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())