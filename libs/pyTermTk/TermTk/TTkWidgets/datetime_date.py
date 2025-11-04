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

__all__ = ['TTkDate']

from enum import IntEnum,Enum,auto
from dataclasses import dataclass
import datetime
import calendar
from typing import Optional

from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.string import TTkString
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.helper import TTkHelper
from TermTk.TTkCore.signal import pyTTkSignal, pyTTkSlot
from TermTk.TTkCore.TTkTerm.inputkey import TTkKeyEvent
from TermTk.TTkCore.TTkTerm.inputmouse import TTkMouseEvent
from TermTk.TTkLayouts import TTkGridLayout, TTkLayout
from TermTk.TTkWidgets.widget import TTkWidget
from TermTk.TTkWidgets.datetime_date_form import TTkDateForm
from TermTk.TTkWidgets.container import TTkContainer
from TermTk.TTkWidgets.spinbox import TTkSpinBox
from TermTk.TTkWidgets.resizableframe import TTkResizableFrame

class _FieldSelected(IntEnum):
    NONE = auto()
    YEARS = auto()
    MONTHS = auto()
    DAYS = auto()
    CAL = auto()


@dataclass
class _TTkTimeWidgetState():
    selected:_FieldSelected=_FieldSelected.NONE
    hovered:_FieldSelected=_FieldSelected.NONE
    digit:int = 0
    def clear(self) -> None:
        self.selected = _FieldSelected.NONE
        self.hovered = _FieldSelected.NONE
        self.digit = 0

class TTkDate(TTkWidget):
    ''' TTkDate:

    A widget for displaying and editing dates.

    ::

        2025/11/04 📅

    .. code:: python

        import TermTk as ttk

        root = ttk.TTk(mouseTrack=True)

        ttk.TTkDate(parent=root) # Defaults to the current date

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

    __slots__ = (
        '_date',
        '_maxOrdinal', '_minOrdinal',
        '_state', 'dateChanged')
    _date:datetime.date
    _state:_TTkTimeWidgetState

    dateChanged:pyTTkSignal
    '''
    This signal is emitted whenever the date changes.

    :param date: The new date
    :type date: :py:class:`datetime.date`
    '''

    def __init__(self, *,
                 date:Optional[datetime.date]=None,
                 handleSeconds:bool=False,
                 **kwargs) -> None:
        '''
        Initializes the TTkDate widget.

        :param date: The initial date to display. If None, the current date is used.
        :type date: :py:class:`datetime.date`, optional
        '''
        if not date:
            date = datetime.date.today()
        self.dateChanged = pyTTkSignal(datetime.date)
        self._date = date
        self._maxOrdinal = datetime.date(year=2100,month=12,day=31).toordinal()
        self._minOrdinal = datetime.date(year=1900, month=1, day=1).toordinal()
        self._state = _TTkTimeWidgetState()
        _layout=TTkLayout()
        super().__init__(**kwargs|{'layout':_layout, 'size':(13,1)})
        self.setFocusPolicy(TTkK.ClickFocus | TTkK.TabFocus)

    @staticmethod
    def _getFieldFromPos(x:int,y:int) -> _FieldSelected:
        '''
        Determines which date field is at a given coordinate.

        :param x: The horizontal position.
        :type x: int
        :param y: The vertical position.
        :type y: int
        :return: The field selected.
        :rtype: :py:class:`_FieldSelected`
        '''
        if y != 0:
            return _FieldSelected.NONE
        if 0 <= x < 4:
            return _FieldSelected.YEARS
        elif 5 <= x < 7:
            return _FieldSelected.MONTHS
        elif 8 <= x < 10:
            return _FieldSelected.DAYS
        elif 11 <= x < 13:
            return _FieldSelected.CAL
        return _FieldSelected.NONE

    def _addDelta(self, delta:int) -> None:
        '''
        Adds a delta (in days) to the current date, respecting the min/max ordinal bounds.

        :param delta: The number of days to add (can be negative).
        :type delta: int
        '''
        if not delta:
            return
        ordinal = self._date.toordinal() + delta
        ordinal = max(self._minOrdinal,min(self._maxOrdinal,ordinal))
        self.setDate(date=datetime.date.fromordinal(ordinal))

    def _showForm(self) -> None:
        '''
        Shows the calendar form as an overlay for date selection.
        '''
        _frame = TTkResizableFrame(size=(22,10), border=True, layout=TTkGridLayout())
        _form = TTkDateForm(parent=_frame, date=self._date)
        _form.setFocus()

        @pyTTkSlot(datetime.date)
        def _dateSelected(date:datetime.date) -> None:
            _form.dateChanged.clear()
            _frame.close()
            self.setDate(date)
            self.setFocus()

        _form.dateChanged.connect(_dateSelected)
        TTkHelper.overlay(self, _frame, 0, -3)

    def date(self) -> datetime.date:
        '''
        Returns the current date of the widget.

        :return: The current date.
        :rtype: :py:class:`datetime.date`
        '''
        return self._date

    def setDate(self, date:datetime.date) -> None:
        '''
        Sets the current date of the widget.

        :param date: The new date to set.
        :type date: :py:class:`datetime.date`
        '''
        if date != self._date:
            self._date = date
            self.dateChanged.emit(date)
            self.update()

    def focusOutEvent(self):
        self._state.clear()
        return super().focusOutEvent()

    def mousePressEvent(self, evt:TTkMouseEvent) -> bool:
        self._state.clear()
        self._state.selected = TTkDate._getFieldFromPos(evt.x, evt.y)
        if self._state.selected == _FieldSelected.CAL:
            self._showForm()
        self.update()
        return True

    def keyEvent(self, evt:TTkKeyEvent) -> bool:
        selected = self._state.selected
        if evt.type == TTkK.SpecialKey:
            self._state.digit = 0
            self._state.selected = selected

            # Tab, Right, Left
            # Switch between digits
            if ( evt.key == TTkK.Key_Right or
                 (evt.key == TTkK.Key_Tab and evt.mod != TTkK.ShiftModifier)):
                 ret, self._state.selected = {
                     _FieldSelected.NONE  : (True,  _FieldSelected.YEARS ),
                     _FieldSelected.YEARS : (True,  _FieldSelected.MONTHS),
                     _FieldSelected.MONTHS: (True,  _FieldSelected.DAYS  ),
                     _FieldSelected.DAYS  : (True,  _FieldSelected.CAL   ),
                     _FieldSelected.CAL   : (False, _FieldSelected.NONE  ),
                 }.get(selected)
                 self.update()
                 return ret
            if ( evt.key == TTkK.Key_Left or
                 (evt.key == TTkK.Key_Tab and evt.mod == TTkK.ShiftModifier)):
                 ret, self._state.selected = {
                     _FieldSelected.NONE  : (True,  _FieldSelected.CAL   ),
                     _FieldSelected.CAL   : (True,  _FieldSelected.DAYS  ),
                     _FieldSelected.DAYS  : (True,  _FieldSelected.MONTHS),
                     _FieldSelected.MONTHS: (True,  _FieldSelected.YEARS ),
                     _FieldSelected.YEARS : (False, _FieldSelected.NONE  ),
                 }.get(selected)
                 self.update()
                 return ret

            if ( self._state.selected == _FieldSelected.CAL and
                 evt.key in (TTkK.Key_Up, TTkK.Key_Down, TTkK.Key_Enter)):
                self._showForm()
                self.update()
                return True

            delta = 0
            if selected == _FieldSelected.YEARS:
                delta = 366 if calendar.isleap(self._date.year) else 365
            elif selected == _FieldSelected.MONTHS:
                delta = 30
            elif selected == _FieldSelected.DAYS:
                delta = 1

            if evt.key == TTkK.Key_Up:
                self._addDelta(delta)
                return True
            elif evt.key == TTkK.Key_Down:
                self._addDelta(-delta)
                return True

            if evt.key in (TTkK.Key_Delete, TTkK.Key_Backspace):
                _y = self._date.year
                _m = self._date.month
                _d = self._date.day
                if selected == _FieldSelected.YEARS:
                    _y = 1900
                elif selected == _FieldSelected.MONTHS:
                    _m = 1
                elif selected == _FieldSelected.DAYS:
                    _d = 1
                self.setDate(date=datetime.date(year=_y,month=_m,day=_d))
                self.update()
                return True

            if evt.key == TTkK.Key_Enter:
                self._state.selected = _FieldSelected.NONE
                return True
        else:
            if self._state.selected == _FieldSelected.CAL:
                self._showForm()
                self.update()
                return True
            if '0' <= evt.key <= '9':
                value = int(evt.key)
                digit = self._state.digit
                _y = self._date.year
                _m = self._date.month
                _d = self._date.day
                if selected == _FieldSelected.YEARS:
                    if not digit:
                        _y = 0
                    _mask = {0:10000,1:1000,2:100}.get(digit,10)
                    _y += value*(10**(3-digit)) - (_y%_mask)
                    _y = max(1900,min(2100,_y))
                    self._state.digit = (digit+1)%4
                elif selected == _FieldSelected.MONTHS:
                    _m = value+_m*10 if digit else value
                    _m = max(1,min(12,_m))
                    self._state.digit = (digit+1)%2
                elif selected == _FieldSelected.DAYS:
                    max_days = calendar.monthrange(_y, _m)[1]
                    _d = value+_d*10 if digit else value
                    _d = max(1,min(max_days,_d))
                    self._state.digit = (digit+1)%2
                self.setDate(date=datetime.date(year=_y,month=_m,day=_d))
                self.update()
            return True
        return False

    def mouseMoveEvent(self, evt:TTkMouseEvent) -> bool:
        self._state.hovered = TTkDate._getFieldFromPos(evt.x, evt.y)
        self.update()
        return True

    def leaveEvent(self, evt:TTkMouseEvent) -> bool:
        self._state.hovered = _FieldSelected.NONE
        self.update()
        super().leaveEvent(evt)
        return True


    def wheelEvent(self, evt:TTkMouseEvent) -> bool:
        self._state.digit = 0
        selected = TTkDate._getFieldFromPos(evt.x, evt.y)
        delta = 0
        if selected == _FieldSelected.YEARS:
            delta = 366 if calendar.isleap(self._date.year) else 365
        elif selected == _FieldSelected.MONTHS:
            delta = 30
        elif selected == _FieldSelected.DAYS:
            delta = 1
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

        year   = TTkString(f"{self._date.year:>2}",  color=hoverColor if self._state.hovered == _FieldSelected.YEARS  else selectColor if self._state.selected == _FieldSelected.YEARS  else color)
        month  = TTkString(f"{self._date.month:02}", color=hoverColor if self._state.hovered == _FieldSelected.MONTHS else selectColor if self._state.selected == _FieldSelected.MONTHS else color)
        day    = TTkString(f"{self._date.day:02}",   color=hoverColor if self._state.hovered == _FieldSelected.DAYS   else selectColor if self._state.selected == _FieldSelected.DAYS   else color)
        sep    = TTkString("/", colorSep)
        cal    = TTkString(' 📆') if _FieldSelected.CAL in (self._state.hovered,self._state.selected) else TTkString(' 📅')
        txts = [year,sep,month,sep,day,cal]
        canvas.drawTTkString(pos=(0,0), text=TTkString().join(txts))
        # a = f"{hours:>5}"