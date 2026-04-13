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

__all__ = ['TTkTextEditRuler']

from typing import List,Optional,Dict

from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.string import TTkString, TTkStringType
from TermTk.TTkCore.canvas import TTkCanvas
from TermTk.TTkCore.TTkTerm.inputmouse import TTkMouseEvent

from TermTk.TTkGui.TTkTextWrap.text_wrap import TTkTextWrap

from TermTk.TTkAbstract.abstractscrollview import TTkAbstractScrollView

class TTkTextEditRuler(TTkAbstractScrollView):
    class MarkRuler():
        class States(int):
            NONE      = 0x00
            FLAGGED   = 0x01
            UNFLAGGED = NONE

        # class MarkRulerType(int):
        #     ALLOW_EMPTY  = 0x01
        #     SINGLE_STATE = 0x02
        #     MULTI_STATE  = 0x04

        __slots__ = ('_markers','_states','_width','_lines','_defaultState')
        def __init__(self,
                markers:dict[int,TTkString]) -> None:
            self._lines:Dict[int,int] = {}
            self._markers = markers
            self._states = len(markers)
            self._defaultState = next(iter(markers))
            self._width = max(v.termWidth() for v in markers.values())

        def width(self) -> int:
            return self._width

        def nextState(self, state:int) -> int:
            return (state+1)%self._states

        def setState(self, line:int, state:int) -> None:
            if state == self._defaultState:
                if line in self._lines:
                    del self._lines[line]
            self._lines[line] = state

        def getState(self, line:int) -> int:
            return self._lines.get(line, self._defaultState)

        def getTTkStr(self, line:int) -> TTkString:
            state=self._lines.get(line, self._defaultState)
            return self._markers.get(state, TTkString())

    classStyle = {
                'default':     {
                    'color': TTkColor.fg("#88aaaa")+TTkColor.bg("#333333"),
                    'wrapColor': TTkColor.fg("#888888")+TTkColor.bg("#333333"),
                    'separatorColor': TTkColor.fg("#444444")},
                'disabled':    {
                    'color': TTkColor.fg('#888888'),
                    'wrapColor': TTkColor.fg('#888888'),
                    'separatorColor': TTkColor.fg("#888888")},
            }

    __slots__ = ('_textWrap','_startingNumber', '_markRuler', '_markRulerSizes')
    def __init__(self, startingNumber=0, **kwargs) -> None:
        self._startingNumber:int = startingNumber
        self._textWrap:Optional[TTkTextWrap] = None
        self._markRuler:List[TTkTextEditRuler.MarkRuler] = []
        self._markRulerSizes:List[int] = []
        super().__init__(**kwargs)
        self.setMaximumWidth(2)

    def _wrapChanged(self) -> None:
        if not self._textWrap:
            return
        dt = max(1,self._textWrap.documentLineCount()-1)
        off  = self._startingNumber
        width = 2+max(len(str(int(dt+off))),len(str(int(off))))
        width += sum(self._markRulerSizes)
        self.setMaximumWidth(width)
        self.update()

    def addMarkRuler(self, markRuler:MarkRuler) -> None:
        self._markRuler.append(markRuler)
        self._markRulerSizes.append(markRuler.width())
        self._wrapChanged()

    def setTextWrap(self, tw:TTkTextWrap) -> None:
        if self._textWrap:
            self._textWrap.wrapChanged.disconnect(self._wrapChanged)
        self._textWrap = tw
        tw.wrapChanged.connect(self._wrapChanged)
        self._wrapChanged()

    def viewFullAreaSize(self) -> tuple[int,int]:
        if self._textWrap:
            return 5, self._textWrap.size()
        else:
            return self.size()

    def mousePressEvent(self, evt:TTkMouseEvent) -> bool:
        if not self._markRuler:
            return True
        ox, oy = self.getViewOffsets()
        w, h = self.size()
        mx,my = evt.x+ox, evt.y+oy
        for mk in self._markRuler:
            mx -= mk.width()
            if mx < 0:
                break
        if self._textWrap:
            rows = self._textWrap.screenRows(my, 1)
        else:
            rows = []
        if rows:
            dt = rows[0][0]
            mk.setState(dt, mk.nextState(mk.getState(dt)))
        else:
            mk.setState(my, mk.nextState(mk.getState(my)))
        self.update()
        return True

    def paintEvent(self, canvas: TTkCanvas) -> None:
        if not self._textWrap: return
        _, oy = self.getViewOffsets()
        w, h = self.size()
        off  = self._startingNumber
        leftOff = sum(self._markRulerSizes)
        rows = self._textWrap.screenRows(oy, h)

        style = self.currentStyle()
        color = style['color']
        wrapColor = style['wrapColor']
        separatorColor = style['separatorColor']

        if self._textWrap:
            for i, row in enumerate(rows):
                dt = row.line
                fr = row.start
                if fr:
                    canvas.drawText(pos=(leftOff,i), text='<', width=w, color=wrapColor)
                else:
                    canvas.drawText(pos=(leftOff,i), text=f"{dt+off}", width=w, color=color)
                canvas.drawChar(pos=(w-1,i), char='▌', color=separatorColor)
        else:
            for y in range(h):
                canvas.drawText(pos=(leftOff,y), text=f"{y+oy+off}", width=w, color=color)
                canvas.drawChar(pos=(w-1,y), char='▌', color=separatorColor)

        ox = 0
        for mk in self._markRuler:
            if self._textWrap:
                for i, row in enumerate(rows):
                    dt = row.line
                    fr = row.start
                    if not fr:
                        canvas.drawText(pos=(ox,i), text=mk.getTTkStr(dt+off))
            else:
                for y in range(h):
                    canvas.drawText(pos=(ox,y), text=mk.getTTkStr(y+oy+off))
            ox += mk.width()
