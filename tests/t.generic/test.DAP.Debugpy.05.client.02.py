# run the test which open the debubpy on the port 64321
#   tests/t.generic/test.generic.013.DAP.Debugpy.05.client.01.py

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
    ret = []
    while m:=header_re.search(response_string):
        header = m.group(0)
        header_length = len(header)
        content_length = int(m.group(1))
        content = response_string[header_length:header_length+content_length]
        response_string = response_string[header_length+content_length:]
        print("Received:")
        print("  header length:", header_length)
        # print("  content:", content)
        print("  json:", jcontent:=json.loads(content))
        ret.append(jcontent)
    return ret


def sm_initialize():
    return {
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

def sm_attach():
    return {
        "command":"attach",
        "arguments":{
            "name":"Python Debugger: Attach",
            "type":"debugpy",
            "request":"attach",
            "connect":{
                "host":"localhost",
                "port":64321},
                "__configurationTarget":6,
                "clientOS":"unix",
                "debugOptions":["RedirectOutput","ShowReturnValue"],
                "justMyCode":True,
                "showReturnValue":True,
                "workspaceFolder":"/Users/epd02/github/Varie/pyTermTk.003",
                # "__sessionId":"7a6b4b23-74ac-41b3-8f89-4b13e9061b5d"
                "__sessionId":"aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
                },
            "type":"request",
            "seq": 2
    }

async def sm_loop(reader, writer):
    while response := await receive_response(reader):
        for content in response:
            if 'type' not in content: return
            if content['type'] == 'event':
                if content['event'] == 'output':
                    print("Response:", content['body'])
                if content['event'] == 'debugpyWaitingForServer':
                    print("Terminated")
                    return
            if content['type'] == 'response':
                if content['command'] == 'initialize':
                    await send_request(writer, sm_attach())

async def main():
    host = 'localhost'
    port = 64321

    reader, writer = await asyncio.open_connection(host, port)
    print("Connected to the debug adapter server.")

    await send_request(writer, sm_initialize())

    await sm_loop(reader, writer)

    # Close the connection
    writer.close()
    await writer.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())