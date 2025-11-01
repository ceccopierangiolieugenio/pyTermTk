# MIT License
#
# Copyright (c) 2025 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

__all__ = ['TTkTime']

from enum import IntEnum,Enum,auto
from dataclasses import dataclass
import datetime

from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.string import TTkString
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.TTkTerm.inputkey import TTkKeyEvent
from TermTk.TTkCore.TTkTerm.inputmouse import TTkMouseEvent
from TermTk.TTkLayouts import TTkGridLayout, TTkLayout
from TermTk.TTkWidgets.widget import TTkWidget
from TermTk.TTkWidgets.container import TTkContainer
from TermTk.TTkWidgets.spinbox import TTkSpinBox


class _FieldSelected(IntEnum):
    NONE = auto()
    HOURS = auto()
    MINUTES = auto()
    SECONDS = auto()


@dataclass
class _TTkTimeWidgetState():
    selected:_FieldSelected=_FieldSelected.NONE
    hovered:_FieldSelected=_FieldSelected.NONE
    secondDigit:bool = False
    def reset(self) -> None:
        self.selected = _FieldSelected.NONE
        self.hovered = _FieldSelected.NONE
        self.secondDigit = False

class TTkTime(TTkContainer):

    classStyle = {
                'default':     {'color':          TTkColor.fgbg("#888888","#222222")+TTkColor.UNDERLINE,
                                'colorSeparator': TTkColor.fgbg("#CCCC00","#222222")+TTkColor.UNDERLINE,
                                'hoverColor':     TTkColor.fgbg("#ffffff","#00AA66")+TTkColor.UNDERLINE,
                                'selectedColor':  TTkColor.fgbg("#ffffff","#008844")+TTkColor.UNDERLINE},
                'disabled':    {'color':          TTkColor.fg(  "#444444")+TTkColor.UNDERLINE,
                                'colorSeparator': TTkColor.fgbg("#666666","#222222")+TTkColor.UNDERLINE,
                                'selectedColor':  TTkColor.fgbg("#888888","#444444")+TTkColor.UNDERLINE},
                'focus':       {'color':          TTkColor.fgbg("#AAAAAA","#000066")+TTkColor.UNDERLINE}
            }

    __slots__ = ('_time', '_handleSeconds', '_state')
    _time:datetime.time
    _handleSeconds:bool
    _state:_TTkTimeWidgetState
    def __init__(self, *,
                 time:datetime.time,
                 handleSeconds:bool=False,
                 **kwargs) -> None:
        self._time = time
        self._state = _TTkTimeWidgetState()
        self._handleSeconds = handleSeconds
        _layout=TTkLayout()
        super().__init__(**kwargs|{'layout':_layout, 'size':(18,1)})
        self.setFocusPolicy(TTkK.ClickFocus | TTkK.TabFocus)

        # sb_hour = TTkSpinBox(parent=self, pos=( 0,0), size=(4,1), value=time.hour   , maximum=24, minimum=1)
        # sb_min  = TTkSpinBox(parent=self, pos=( 7,0), size=(4,1), value=time.minute , maximum=60, minimum=1)
        # sb_sec  = TTkSpinBox(parent=self, pos=(14,0), size=(4,1), value=time.second , maximum=60, minimum=1)

    @staticmethod
    def _getFieldFromPos(x:int,y:int) -> _FieldSelected:
        if y != 0:
            return _FieldSelected.NONE
        if 0 <= x < 2:
            return _FieldSelected.HOURS
        elif 3 <= x < 5:
            return _FieldSelected.MINUTES
        elif 6 <= x < 8:
            return _FieldSelected.SECONDS
        return _FieldSelected.NONE

    def _setUni(self, uni:int) -> None:
        uni = max(0,min(24*3600-1,uni))
        self._time = datetime.time(
            hour=uni//3600,
            minute=(uni//60)%60,
            second=uni%60)
        self.update()

    def _addDelta(self, delta:int) -> None:
        if not delta:
            return
        uni = delta + self._time.hour * 3600 + self._time.minute * 60 + self._time.second
        self._setUni(uni=uni)

    def focusOutEvent(self):
        self._state.reset()
        self.update
        return super().focusOutEvent()

    def mousePressEvent(self, evt:TTkMouseEvent) -> bool:
        self._state.reset()
        self._state.selected = TTkTime._getFieldFromPos(evt.x, evt.y)
        self.update()
        return True

    def keyEvent(self, evt:TTkKeyEvent) -> bool:
        selected = self._state.selected
        if evt.type == TTkK.SpecialKey:
            self._state.secondDigit = False
            self._state.selected = selected

            # Tab, Right, Left
            # Switch between digits
            if ( evt.key in (TTkK.Key_Tab, TTkK.Key_Right)):
                 if selected == _FieldSelected.NONE:
                    self._state.selected = _FieldSelected.HOURS
                    self.update()
                    return True
                 if selected == _FieldSelected.HOURS:
                    self._state.selected = _FieldSelected.MINUTES
                    self.update()
                    return True
                 if selected == _FieldSelected.MINUTES:
                    self._state.selected = _FieldSelected.SECONDS
                    self.update()
                    return True
                 if selected == _FieldSelected.SECONDS:
                    self._state.selected = _FieldSelected.NONE
                    self.update()
                    return False
            if ( evt.key == TTkK.Key_Left or
                 (evt.key == TTkK.Key_Tab and evt.mod == TTkK.ShiftModifier)):
                 if selected == _FieldSelected.HOURS:
                    self._state.selected = _FieldSelected.NONE
                    self.update()
                    return False
                 if selected == _FieldSelected.MINUTES:
                    self._state.selected = _FieldSelected.HOURS
                    self.update()
                    return True
                 if selected == _FieldSelected.SECONDS:
                    self._state.selected = _FieldSelected.MINUTES
                    self.update()
                    return True
                 if selected == _FieldSelected.NONE:
                    self._state.selected = _FieldSelected.SECONDS
                    self.update()
                    return True

            delta = 0
            if selected == _FieldSelected.HOURS:
                delta = 3600
            elif selected == _FieldSelected.MINUTES:
                delta = 60
            elif selected == _FieldSelected.SECONDS:
                delta = 1

            if evt.key == TTkK.Key_Up:
                self._addDelta(delta)
                return True
            elif evt.key == TTkK.Key_Down:
                self._addDelta(-delta)
                return True

            if evt.key in (TTkK.Key_Delete, TTkK.Key_Backspace):
                h = self._time.hour
                m = self._time.minute
                s = self._time.second
                if selected == _FieldSelected.HOURS:
                    h = 0
                elif selected == _FieldSelected.MINUTES:
                    m = 0
                elif selected == _FieldSelected.SECONDS:
                    s = 0
                self._time = datetime.time(hour=h,minute=m,second=s)
                self.update()
                return True

            if evt.key == TTkK.Key_Enter:
                self._state.selected = _FieldSelected.NONE
                return True
        else:
            if '0' <= evt.key <= '9':
                value = int(evt.key)
                secondDigit = self._state.secondDigit
                self._state.secondDigit = not secondDigit
                h = self._time.hour
                m = self._time.minute
                s = self._time.second
                if selected == _FieldSelected.HOURS:
                    h = (value + h*10) if secondDigit else value
                    h = max(0,min(23,h))
                elif selected == _FieldSelected.MINUTES:
                    m = (value + m*10) if secondDigit else value
                    m = max(0,min(59,m))
                elif selected == _FieldSelected.SECONDS:
                    s = (value + s*10) if secondDigit else value
                    s = max(0,min(59,s))
                self._time = datetime.time(hour=h,minute=m,second=s)
                self.update()
            return True
        return False

    def mouseMoveEvent(self, evt:TTkMouseEvent) -> bool:
        self._state.hovered = TTkTime._getFieldFromPos(evt.x, evt.y)
        self.update()
        return True

    def leaveEvent(self, evt:TTkMouseEvent) -> bool:
        self._state.hovered = _FieldSelected.NONE
        self.update()
        return True

    def wheelEvent(self, evt:TTkMouseEvent) -> bool:
        self._state.secondDigit = False
        selected = TTkTime._getFieldFromPos(evt.x, evt.y)
        delta = 0
        if selected == _FieldSelected.HOURS:
            delta = 1 * 3600
        elif selected == _FieldSelected.MINUTES:
            delta = 5 * 60
        elif selected == _FieldSelected.SECONDS:
            delta = 5
        if delta:
            if evt.evt in (TTkK.WHEEL_Up, TTkK.WHEEL_Left):
                self._addDelta(delta=delta)
            elif evt.evt in (TTkK.WHEEL_Down, TTkK.WHEEL_Right):
                self._addDelta(delta=-delta)
        return True

    def paintEvent(self, canvas):
        style = self.currentStyle()

        color       = style['color']
        colorSep    = style['colorSeparator']
        hoverColor  = style['hoverColor']
        selectColor = style['selectedColor']

        hours   = TTkString(f"{self._time.hour:>2}",   color=hoverColor if self._state.hovered == _FieldSelected.HOURS   else selectColor if self._state.selected == _FieldSelected.HOURS   else color)
        min     = TTkString(f"{self._time.minute:02}", color=hoverColor if self._state.hovered == _FieldSelected.MINUTES else selectColor if self._state.selected == _FieldSelected.MINUTES else color)
        seconds = TTkString(f"{self._time.second:02}", color=hoverColor if self._state.hovered == _FieldSelected.SECONDS else selectColor if self._state.selected == _FieldSelected.SECONDS else color)
        sep = TTkString(":", colorSep)
        canvas.drawTTkString(pos=(0,0), text=hours+sep+min+sep+seconds)
        # a = f"{hours:>5}"