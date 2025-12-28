# MIT License
#
# Copyright (c) 2021 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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
# SOFTWARE.

__all__ = []

from typing import Callable,Optional,Protocol

from TermTk.TTkCore.signal import pyTTkSignal, pyTTkSlot

class _TTkTimer_Interface(Protocol):
    '''Protocol defining the interface for timer implementations.'''

    timeout: pyTTkSignal

    def __init__(
            self,
            name: Optional[str] = None,
            excepthook: Optional[Callable[[Exception], None]] = None) -> None:
        '''Initialize timer with optional name and exception handler.

        :param name: Optional name for the timer
        :type name: str, optional
        :param excepthook: Optional callback for exception handling
        :type excepthook: Callable[[Exception], None], optional
        '''
        ...

    def quit(self) -> None:
        '''Stop the timer and cleanup resources.'''
        ...

    def run(self) -> None:
        '''Main timer loop (typically runs in a thread).'''
        ...

    def start(self, sec: float = 0.0) -> None:
        '''Start the timer with specified interval.

        :param sec: Interval in seconds
        :type sec: float
        '''
        ...

    def stop(self) -> None:
        '''Stop the timer without cleanup.'''
        ...