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

class TTkAsyncio():
    loop = asyncio.get_event_loop()
    Queue = asyncio.Queue
    QueueShutDown = asyncio.QueueShutDown
    Event = asyncio.Event
    Lock = asyncio.Lock
    sleep = asyncio.sleep
    ensure_future = asyncio.ensure_future
    gather = asyncio.gather

    @staticmethod
    def quit():
        pass

    @staticmethod
    def run(coro):
        asyncio.set_event_loop(TTkAsyncio.loop)
        # asyncio.run(coro)
        TTkAsyncio.loop.run_until_complete(coro)
        TTkAsyncio.loop.close()

    @staticmethod
    def create_task(*args, **kwargs):
        return TTkAsyncio.loop.create_task(*args, **kwargs)

    def call_soon_threadsafe(*args, **kwargs):
        return TTkAsyncio.loop.call_soon_threadsafe(TTkAsyncio.loop.create_task, *args, **kwargs)

    def add_signal_handler(*args, **kwargs):
        return TTkAsyncio.loop.add_signal_handler(*args, **kwargs)