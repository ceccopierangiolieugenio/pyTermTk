# run the test which open the debubpy on the port 64321
#   tests/t.generic/test.generic.013.DAP.Debugpy.05.client.01.py

import asyncio
import json
import re
import uuid
import os, sys

sys.path.append(os.path.join(sys.path[0],'../../libs'))
import DAP as dap

class ClientDAP():
    __slots__ = ('_host', '_port',
                 '_seq',
                 '_reader', '_writer')
    _reader:asyncio.StreamReader
    _writer:asyncio.StreamWriter
    def __init__(self, host:str, port:int) -> None:
        self._host = host
        self._port = port
        self._seq = 1
        self._reader = None
        self._writer = None

    async def open(self) -> None:
        self._reader, self._writer = await asyncio.open_connection(self._host, self._port)

    async def close(self) -> None:
        self._writer.close()
        await self._writer.wait_closed()

    async def send_request(self, request) -> None:
        request.seq = self._seq
        self._seq += 1
        content = request.json()
        header = f"Content-Length: {len(content)}\r\n\r\n"
        message = header + content
        print("Sending:")
        print("  header:", header)
        print("  content:", content)
        self._writer.write(message.encode('utf-8'))
        await self._writer.drain()

    _header_re = re.compile(r'^Content-Length: (\d+)[\r\n]*', re.MULTILINE)

    async def receive_response(self) -> list[dict]:
        response = await self._reader.read(4096)
        response_string = response.decode('utf-8')
        ret = []
        while m:=self._header_re.search(response_string):
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


def sm_configuration_done() -> dap.ConfigurationDoneRequest:
    return dap.ConfigurationDoneRequest.parse_obj({
        'seq':0,
        'type':'request',
        'command':'configurationDone'
        })

def sm_initialize() -> dap.InitializeRequest:
    return dap.InitializeRequest.parse_obj({
        'seq': 0,
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
        })

def sm_attach() -> dap.AttachRequest:
    return dap.AttachRequest.parse_obj({
        'seq': 0,
        "command":"attach",
        "type":"request",
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
                "__sessionId":str(uuid.uuid4())
                },
    })

async def sm_loop(client:ClientDAP):
    while response := await client.receive_response():
        for content in response:
            if 'type' not in content: return
            elif content['type'] == 'event':
                if content['event'] == 'output':
                    print("Response:", content['body'])
                elif content['event'] == 'debugpyWaitingForServer':
                    await client.send_request(sm_configuration_done())
                elif content['event'] == 'terminated':
                    print("Terminated")
                    return
            elif content['type'] == 'response':
                if content['command'] == 'initialize':
                    await client.send_request(sm_attach())

async def main():
    host = 'localhost'
    port = 64321

    client = ClientDAP(host, port)

    await client.open()
    await client.send_request(sm_initialize())
    await sm_loop(client)
    await client.close()


if __name__ == "__main__":
    asyncio.run(main())