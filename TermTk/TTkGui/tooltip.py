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

__all__ = ['TTkToolTip']

# from TermTk.TTkCore.helper    import TTkHelper
from TermTk.TTkCore.log       import TTkLog
from TermTk.TTkCore.canvas    import TTkCanvas
from TermTk.TTkCore.cfg       import TTkCfg
from TermTk.TTkCore.color     import TTkColor
from TermTk.TTkCore.timer     import TTkTimer
from TermTk.TTkCore.helper    import TTkHelper
from TermTk.TTkCore.string    import TTkString
from TermTk.TTkWidgets.widget import TTkWidget
from TermTk.TTkCore.signal    import pyTTkSlot

class _TTkToolTipDisplayWidget(TTkWidget):
    __slots__ = ('_toolTip', '_x', '_y')
    def __init__(self, *args, **kwargs):
        TTkWidget.__init__(self, *args, **kwargs)
        self._toolTip = kwargs.get('toolTip',TTkString()).split('\n')
        w = 2+max([s.termWidth() for s in self._toolTip])
        h = 2+len(self._toolTip)
        self.resize(w,h)

    def mouseEvent(self, evt): return False

    def paintEvent(self, canvas):
        w,h = self.size()
        borderColor = TTkColor.fg("#888888")
        canvas.drawBox(pos=(0,0),size=(w,h), color=borderColor)
        canvas.drawChar(pos=(0,  0),  char='╭', color=borderColor)
        canvas.drawChar(pos=(w-1,0),  char='╮', color=borderColor)
        canvas.drawChar(pos=(w-1,h-1),char='╯', color=borderColor)
        canvas.drawChar(pos=(0,  h-1),char='╰', color=borderColor)
        for i,s in enumerate(self._toolTip,1):
            canvas.drawTTkString(pos=(1,i), text=s)

class TTkToolTip():
    toolTipTimer = TTkTimer()
    toolTip = TTkString()

    @pyTTkSlot()
    @staticmethod
    def _toolTipShow():
        # TTkLog.debug(f"TT:{TTkToolTip.toolTip}")
        TTkHelper.toolTipShow(_TTkToolTipDisplayWidget(toolTip=TTkToolTip.toolTip))

    @staticmethod
    def trigger(toolTip):
        # TTkToolTip.toolTipTimer.stop()
        TTkToolTip.toolTip = toolTip
        TTkToolTip.toolTipTimer.start(TTkCfg.toolTipTime)

    @staticmethod
    def reset():
        TTkToolTip.toolTipTimer.stop()

TTkToolTip.toolTipTimer.timeout.connect(TTkToolTip._toolTipShow)
TTkHelper.toolTipTrigger = TTkToolTip.trigger
TTkHelper.toolTipReset = TTkToolTip.reset