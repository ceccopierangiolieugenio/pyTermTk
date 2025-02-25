# MIT License
#
# Copyright (c) 2023 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE

__all__ = ['TTkAsyncio']

import asyncio

import logging
logging.basicConfig(level=logging.DEBUG)


class TTkAsyncio():
    loop = asyncio.get_event_loop()
    Queue = asyncio.Queue
    Event = asyncio.Event
    Lock = asyncio.Lock
    sleep = asyncio.sleep

    @staticmethod
    def run(coro):
        asyncio.set_event_loop(TTkAsyncio.loop)
        # asyncio.run(coro)
        TTkAsyncio.loop.run_until_complete(coro)
        TTkAsyncio.loop.close()

    @staticmethod
    def create_task(*args, **kwargs):
        if TTkAsyncio.loop.is_running():
            # asyncio.set_event_loop(TTkAsyncio.loop)
            TTkAsyncio.loop.create_task(*args, **kwargs)