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

from enum import IntEnum,auto
from dataclasses import dataclass
import datetime as dt

from typing import Optional

from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.string import TTkString
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.signal import pyTTkSignal, pyTTkSlot
from TermTk.TTkCore.TTkTerm.inputkey import TTkKeyEvent
from TermTk.TTkCore.TTkTerm.inputmouse import TTkMouseEvent
from TermTk.TTkWidgets.widget import TTkWidget


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
    def clear(self) -> None:
        self.selected = _FieldSelected.NONE
        self.hovered = _FieldSelected.NONE
        self.secondDigit = False

class TTkTime(TTkWidget):
    ''' TTkTime:

    A widget for displaying and editing times. (`demo <https://ceccopierangiolieugenio.github.io/pyTermTk-Docs/sandbox/sandbox.html?filePath=demo/showcase/date_time.py>`__)

    ::

        12:30:45

    .. code:: python

        import TermTk as ttk

        root = ttk.TTk()

        ttk.TTkTime(parent=root) # Defaults to the current time

        root.mainloop()

    '''

    classStyle = {
                'default':     {'color':          TTkColor.fgbg("#888888","#222222")+TTkColor.UNDERLINE,
                                'colorSeparator': TTkColor.fgbg("#CCCC00","#222222"),
                                'hoverColor':     TTkColor.fgbg("#ffffff","#00AA66")+TTkColor.UNDERLINE,
                                'selectedColor':  TTkColor.fgbg("#ffffff","#008844")+TTkColor.UNDERLINE},
                'hover':       {'color':          TTkColor.fgbg("#AAAAAA","#000066")+TTkColor.UNDERLINE},
                'disabled':    {'color':          TTkColor.fg(  "#444444")+TTkColor.UNDERLINE,
                                'colorSeparator': TTkColor.fgbg("#666666","#222222")+TTkColor.UNDERLINE,
                                'selectedColor':  TTkColor.fgbg("#888888","#444444")+TTkColor.UNDERLINE},
                'focus':       {'color':          TTkColor.fgbg("#888888","#000066")+TTkColor.UNDERLINE}
            }

    __slots__ = ('_time', '_state', 'timeChanged')
    _time:dt.time
    _state:_TTkTimeWidgetState

    timeChanged:pyTTkSignal
    '''
    This signal is emitted whenever the time changes.

    :param time: The new time
    :type time: :py:class:`datetime.time`

    '''
    def __init__(self, *,
                 time:Optional[dt.time] = None,
                 # handleSeconds:bool=False,
                 **kwargs) -> None:
        '''
        Initializes the TTkTime widget.

        :param time: The initial time to display. If None, the current time is used.
        :type time: :class:`datetime.time`, optional
        '''
        if not time:
            time = dt.datetime.now().time().replace(microsecond=0)
        self.timeChanged = pyTTkSignal(dt.time)
        self._time = time
        self._state = _TTkTimeWidgetState()
        super().__init__(**kwargs|{'size':(8,1)})
        self.setFocusPolicy(TTkK.ClickFocus | TTkK.TabFocus)

        # sb_hour = TTkSpinBox(parent=self, pos=( 0,0), size=(4,1), value=time.hour   , maximum=24, minimum=1)
        # sb_min  = TTkSpinBox(parent=self, pos=( 7,0), size=(4,1), value=time.minute , maximum=60, minimum=1)
        # sb_sec  = TTkSpinBox(parent=self, pos=(14,0), size=(4,1), value=time.second , maximum=60, minimum=1)

    @staticmethod
    def _getFieldFromPos(x:int,y:int) -> _FieldSelected:
        '''
        Determines which time field is at a given coordinate.

        :param x: The horizontal position.
        :type x: int
        :param y: The vertical position.
        :type y: int
        :return: The field selected.
        :rtype: :py:class:`_FieldSelected`
        '''
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
        '''
        Sets the time based on the total number of seconds from midnight.

        :param uni: The total seconds from midnight.
        :type uni: int
        '''
        uni = max(0,min(24*3600-1,uni))
        self.setTime(time=dt.time(
            hour=uni//3600,
            minute=(uni//60)%60,
            second=uni%60)
        )

    def _addDelta(self, delta:int) -> None:
        '''
        Adds a delta (in seconds) to the current time.

        :param delta: The number of seconds to add (can be negative).
        :type delta: int
        '''
        if not delta:
            return
        uni = delta + self._time.hour * 3600 + self._time.minute * 60 + self._time.second
        self._setUni(uni=uni)

    def time(self) -> dt.time:
        '''
        Returns the current time of the widget.

        :return: The current time.
        :rtype: :py:class:`datetime.time`
        '''
        return self._time

    def setTime(self, time:dt.time) -> None:
        '''
        Sets the current time of the widget.

        :param time: The new time to set.
        :type time: :py:class:`datetime.time`
        '''
        if time != self._time:
            self._time = time
            self.timeChanged.emit(time)
            self.update()

    def focusOutEvent(self):
        self._state.clear()
        return super().focusOutEvent()

    def mousePressEvent(self, evt:TTkMouseEvent) -> bool:
        self._state.clear()
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
            if ( evt.key == TTkK.Key_Right or
                 (evt.key == TTkK.Key_Tab and evt.mod != TTkK.ShiftModifier)):
                 ret, self._state.selected = {
                     _FieldSelected.NONE    : (True,  _FieldSelected.HOURS  ),
                     _FieldSelected.HOURS   : (True,  _FieldSelected.MINUTES),
                     _FieldSelected.MINUTES : (True,  _FieldSelected.SECONDS),
                     _FieldSelected.SECONDS : (False, _FieldSelected.NONE   ),
                 }.get(selected, (False, _FieldSelected.NONE))
                 self.update()
                 return ret
            if ( evt.key == TTkK.Key_Left or
                 (evt.key == TTkK.Key_Tab and evt.mod == TTkK.ShiftModifier)):
                 ret, self._state.selected = {
                     _FieldSelected.NONE    : (True,  _FieldSelected.SECONDS),
                     _FieldSelected.SECONDS : (True,  _FieldSelected.MINUTES),
                     _FieldSelected.MINUTES : (True,  _FieldSelected.HOURS  ),
                     _FieldSelected.HOURS   : (False, _FieldSelected.NONE   ),
                 }.get(selected, (False, _FieldSelected.NONE))
                 self.update()
                 return ret

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
                self.setTime(time=dt.time(hour=h,minute=m,second=s))
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
                self.setTime(time=dt.time(hour=h,minute=m,second=s))
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
        super().leaveEvent(evt)
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
