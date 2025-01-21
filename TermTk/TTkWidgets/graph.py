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

__all__ = ['TTkGraph']

# inspired by:
# https://grafana.com/docs/grafana/latest/panels/visualizations/graph-panel/
# And of course:
# https://github.com/aristocratos/bpytop

from TermTk.TTkCore.cfg import TTkCfg
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkWidgets.widget import TTkWidget

class TTkGraph(TTkWidget):
    __slots__ = ('_data', '_maxData', '_offset', '_direction', '_align', '_color')
    def __init__(self, *,
                 color:TTkColor=TTkColor.RST,
                 maxData:int=0x1000,
                 direction:int=TTkK.RIGHT,
                 align:TTkK.Alignment=TTkK.CENTER,
                 **kwargs) -> None:
        self._data = [[0]]
        self._offset = 0
        self._color = color
        self._align = align
        self._maxData = maxData
        self._direction = direction
        super().__init__(**kwargs)

    def color(self):
        return self._color

    def setColor(self, color):
        if self._color != color:
            self._color = color
            self.update()

    def addValue(self, values):
        self._data.append(values)
        self.update()

    def paintEvent(self, canvas):
        if not self._data: return
        w,h = self.size()
        x=0
        if   self._align == TTkK.CENTER:
            y = h//2
        elif self._align == TTkK.TOP:
            y = 0
        else:
            y = h
        v1,v2 = [0],[0]
        i=0
        data = self._data[-w*2:]
        # TTkLog.debug(data)
        # TODO: use deep unpacking technique to grab couples of values
        # https://mathspp.com/blog/pydonts/enumerate-me#deep-unpacking
        mv = max(max(map(max,data)),-min(map(min,data)))
        zoom = 2*h/mv if mv>0 else 1.0
        for i in range(len(data)):
            v2 = v1
            v1 = data[i]
            if i%2==0:
                if self._direction == TTkK.RIGHT:
                    canvas.drawHChart(pos=(x+i//2,y),values=(v2,v1), zoom=zoom, color=self._color.modParam(val=-y))
                else:
                    canvas.drawHChart(pos=(w-(x+i//2),y),values=(v1,v2), zoom=zoom, color=self._color.modParam(val=-y))
        if i%2==1:
            if self._direction == TTkK.RIGHT:
                canvas.drawHChart(pos=(x+i//2+1,y),values=(v1,v1), zoom=zoom, color=self._color.modParam(val=-y))
            else:
                canvas.drawHChart(pos=(w-(x+i//2+1),y),values=(v1,v1), zoom=zoom, color=self._color.modParam(val=-y))
