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
# SOFTWARE.

# __all__ = ['DebugTTkTerminal']
__all__ = []

# class DebugTTkTerminal(TTkWidget):
#     __slots__ = ('_terminal')
#     _terminal:TTkTerminal
#     def __init__(self, terminal, **kwargs) -> None:
#         self._terminal = terminal
#         super().__init__(**kwargs)

#     def paintEvent(self, canvas: TTkCanvas):
#         t = self._terminal
#         canvas.drawText(pos=(0,0), text=f"{t=}")
#         canvas.drawText(pos=(0,1), text=f"{t._terminalCursor=}")
#         canvas.drawText(pos=(0,2), text=f"{t._scrollingRegion=}")
#         canvas.drawText(pos=(0,3), text=f"{len(t._bufferedLines)=}")
