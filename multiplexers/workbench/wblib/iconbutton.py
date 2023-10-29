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

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.canvas import TTkCanvas
from TermTk.TTkCore.string import TTkString
from TermTk.TTkWidgets.widget import TTkWidget
from TermTk.TTkWidgets.scrollbar import TTkScrollBar

from .colors import *

__all__ = ['WBIconButton']

class WBIconButton(TTkWidget):
    IconTerminal    = 0x01
    IconPreferences = 0x02
    IconInputLog    = 0x03
    IconLogViewer    = 0x03

    _iconS = { IconTerminal: [
                    # TTkString("🬦"              "🬹🬹🬹🬹🬹🬹"                                           "🬓"),
                    TTkString("▗"              "▄▄▄▄▄▄"                                           "▖"),
                    TTkString("▐")+ TTkString(" C:\  ",fgORANGE+bgWHITE+TTkColor.BOLD)+ TTkString("▌",fgWHITE+bgBLACK),
                    TTkString("🬉")+ TTkString("🬎🬎🬎🬎🬎🬎", fgWHITE+bgBLACK)+ TTkString("🬄",fgWHITE+bgBLACK)],
                    # TTkString("┌──────┐"),
                    # TTkString("│ C:\  │"),
                    # TTkString("└──────┘")]
                IconPreferences: [
                    TTkString("   ┌───┐"),
                    TTkString("   │ ? │"),
                    TTkString("   └───┘")],
                IconInputLog: [
                    TTkString("┌────────┐"),
                    TTkString("│ ABC... │"),
                    TTkString("└────────┘")],
                IconLogViewer: [
                    TTkString("┌──────┐"),
                    TTkString("│ LOGS │"),
                    TTkString("└──────┘")],
                    }

    classStyle = {
                'default':     {'color': fgWHITE+bgBLUE},
                'disabled':    {'color': fgWHITE+bgBLUE},
                'focus':       {'color': fgWHITE+bgBLUE},
                'clicked':     {'color': fgWHITE+bgBLACK},
            }

    __slots__ = ('_text', '_icon', 'clicked')
    def __init__(self, text="", icon=IconTerminal, **kwargs):
        self.clicked = pyTTkSignal()
        self._text = text
        self._icon = WBIconButton._iconS[icon]
        super().__init__(**kwargs)
        self.getCanvas().setTransparent(True)
        self.resize(len(text),len(self._icon)+1)

    def mouseDoubleClickEvent(self, evt) -> bool:
        self.clicked.emit()
        return True

    def paintEvent(self, canvas: TTkCanvas):
        style = self.currentStyle()
        color = style['color']

        y=-1
        for y,l in enumerate(self._icon):
            canvas.drawTTkString(text=l, pos=(0,y),color=color)
        canvas.drawText(text=self._text, pos=(0,y+1),color=color)