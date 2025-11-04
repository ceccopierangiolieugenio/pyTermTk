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

__all__ = ['TTkDateForm']

from enum import IntEnum,Enum,auto
from dataclasses import dataclass
import datetime
import calendar

from typing import List,Tuple,Optional

from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.string import TTkString
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.helper import TTkHelper
from TermTk.TTkCore.signal import pyTTkSignal, pyTTkSlot
from TermTk.TTkCore.TTkTerm.inputkey import TTkKeyEvent
from TermTk.TTkCore.TTkTerm.inputmouse import TTkMouseEvent
from TermTk.TTkLayouts import TTkGridLayout, TTkLayout
from TermTk.TTkWidgets.widget import TTkWidget
from TermTk.TTkWidgets.container import TTkContainer
from TermTk.TTkWidgets.spinbox import TTkSpinBox
from TermTk.TTkWidgets.list_ import TTkList
from TermTk.TTkWidgets.resizableframe import TTkResizableFrame


class _FieldSelected(IntEnum):
    NONE = auto()

    MONTH = auto()
    YEAR = auto()
    DAY = auto()

    YEAR_LEFT = auto()
    YEAR_RIGHT = auto()

    MONTH_LEFT = auto()
    MONTH_RIGHT = auto()

    HOVER_DATA = auto()
    HOVER_LEFT = auto()
    HOVER_RIGHT = auto()


class _TTkDateWidgetState():
    __slots__ = (
        '_calendar',
        '_date',
        '_month_calendar',
        '_hovered', '_highlighted', '_selected',
        '_current_month_index',
        # Signals
        'dateChanged',
        'highlightedChanged'
    )

    dateChanged:pyTTkSignal
    _date:datetime.date
    _calendar:calendar.TextCalendar

    _current_month_index:int

    _month_calendar:List[List[datetime.datetime]]

    _first_month_day:int
    _last_month_day:int

    _hovered:Optional[datetime.date]
    _highlighted:datetime.date
    _selected:Optional[datetime.date]

    _selected:_FieldSelected
    _secondDigit:bool

    def __init__(self, date:datetime.date):
        self.dateChanged = pyTTkSignal(datetime.date)
        self.highlightedChanged = pyTTkSignal(datetime.date)
        self._current_month_index = 0
        self._calendar = calendar.TextCalendar(calendar.SUNDAY)
        self._hovered = None
        self._selected = None
        self.setDate(date)

    def _getMonthIndex(self, date: datetime.date) -> int:
        """Returns unique month index: year*12 + month-1"""
        return date.year * 12 + date.month - 1

    def _yearMonthFromMonthIndex(self, month_index: int) -> Tuple[int,int]:
        """Convert month index back to a date (1st of that month)"""
        year = month_index // 12
        month = (month_index % 12) + 1
        return year,month

    def _dateFromMonthIndex(self, month_index: int) -> datetime.date:
        """Convert month index back to a date (1st of that month)"""
        year,month = self._yearMonthFromMonthIndex(month_index)
        return datetime.date(year, month, 1)

    def splitDate(self) -> Tuple[int,int,int]:
        year =  self._date.year
        month = self._date.month
        day =   self._date.day
        return (year,month,day)

    def setDate(self, date:datetime.date) -> None:
        self._date = date
        self._selected = date
        self.setHighlightedDate(date)
        self.dateChanged.emit(date)

    def setHighlightedDate(self, date:datetime.date) -> None:
        self._highlighted = date
        current_month_index = self._getMonthIndex(date)
        if self._current_month_index == current_month_index:
            return
        self._current_month_index = current_month_index

        year =  date.year
        month = date.month
        day =   date.day

        month_day_calendar = self._calendar.monthdayscalendar(year, month)

        # [ 0, 0, 0, 0, 0, 0, 1] <- month_day_calendar, first row
        # [-5,-4,-3,-2,-1, 0, 1] <- normalization
        # [ 1 ,2, 3, 4, 5, 6, 7] <- month_day_calendar, first row
        # [-6,-5,-4,-3,-2,-1, 0] <- normalization ; prepend a line with the previous month days
        # Same logic apply for the last row and the next month
        # Normalize the list of days

        if (first_day:=month_day_calendar[0][0]) == 0:
            ref_day = month_day_calendar[0][-1]
            month_day_calendar[0] = [_d-6+ref_day for _d in range(7)]
        else:
            month_day_calendar.insert(0,[_d+first_day-7 for _d in range(7)])

        if (last_day:=month_day_calendar[-1][-1]) == 0:
            ref_day = month_day_calendar[-1][0]
            month_day_calendar[-1] = [_d+ref_day for _d in range(7)]
        else:
            month_day_calendar.append([_d+last_day+1 for _d in range(7)])

        # Build the list of date
        ordinal = date.toordinal()
        self._month_calendar = [
            [ datetime.date.fromordinal(_day-day+ordinal) for _day in _week ]
            for _week in month_day_calendar
        ]
        self.highlightedChanged.emit(date)

    def clearHover(self):
        self._hovered=None

    def clearSelected(self):
        self._selected=None


_month_to_str = {
    1: "January", 2: "February", 3: "March",      4: "April",    5: "May",      6: "June",
    7: "July",    8: "August",   9: "September", 10: "October", 11: "November", 12: "December"
}

_month_to_str_slim = {
    1: "Jan", 2: "Feb", 3: "Mar",  4: "Apr",  5: "May",  6: "Jun",
    7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
}

class _TTkBaseMonthYear(TTkWidget):
    classStyle = {
                'default':     {'color':            TTkColor.fgbg("#888888","#222222"),
                                'color2':           TTkColor.fgbg("#888888","#222222"),
                                'colorSeparator':   TTkColor.fgbg("#CCCC00","#222222"),
                                'hoverColor':       TTkColor.fgbg("#ffffff","#00AA66"),
                                'highlightedColor': TTkColor.fgbg("#ffffff","#00AA88"),
                                'selectedColor':    TTkColor.fgbg("#ffffff","#008844")},
                'hover':       {'color':            TTkColor.fgbg("#AAAAAA","#000066")},
                'disabled':    {'color':            TTkColor.fg(  "#444444"),
                                'colorSeparator':   TTkColor.fgbg("#666666","#222222"),
                                'selectedColor':    TTkColor.fgbg("#888888","#444444")},
                'focus':       {'color':            TTkColor.fgbg("#888888","#000066")}
            }

    __slots__ = ('_state', '_hoverState')

    _state:_TTkDateWidgetState
    _hoverstate:_FieldSelected

    def __init__(self, *,
                 state: _TTkDateWidgetState,
                 **kwargs) -> None:
        self._state = state
        self._hoverState = _FieldSelected.NONE
        super().__init__(**kwargs)
        self.setFocusPolicy(TTkK.ClickFocus | TTkK.TabFocus)
        self._state.dateChanged.connect(self.update)
        self._state.highlightedChanged.connect(self.update)

    def _show_chooser(self) -> None:
        raise NotImplementedError()

    def _goto_next(self) -> None:
        raise NotImplementedError()

    def _goto_prev(self) -> None:
        raise NotImplementedError()

    def data(self) -> str:
        raise NotImplementedError()

    def mousePressEvent(self, evt:TTkMouseEvent) -> bool:
        x,y = evt.x,evt.y
        w = self.width()
        if y != 0:
            return
        if 0 <= x <= 1:
            self._goto_prev()
        elif w-2 <= x <= w-1 :
            self._goto_next()
        elif 2 <= x <= w-3:
            self._show_chooser()
        return True

    def leaveEvent(self, evt:TTkMouseEvent) -> bool:
        self._hoverState = _FieldSelected.NONE
        self.update()
        super().leaveEvent(evt)

    def mouseMoveEvent(self, evt:TTkMouseEvent) -> bool:
        x,y = evt.x,evt.y
        w = self.width()
        self._hoverState = _FieldSelected.NONE
        if y != 0:
            return
        if 0 <= x <= 1:
            self._hoverState = _FieldSelected.HOVER_LEFT
        elif w-2 <= x <= w-1 :
            self._hoverState = _FieldSelected.HOVER_RIGHT
        elif 2 <= x <= w-3:
            self._hoverState = _FieldSelected.HOVER_DATA
        self.update()
        return True

    def keyEvent(self, evt:TTkKeyEvent) -> bool:
        if evt.type == TTkK.SpecialKey:
            if evt.key == TTkK.Key_Enter:
                self._show_chooser()
            elif evt.key == TTkK.Key_Up:
                self._goto_next()
            elif evt.key == TTkK.Key_Down:
                self._goto_prev()
            else:
                return False
            return True
        elif( evt.type == TTkK.Character and
              evt.key in (' 1234567890')):
            self._show_chooser()
            return True
        return False


    def paintEvent(self, canvas):
        style = self.currentStyle()

        color       = style['color']
        colorSep    = style['colorSeparator']
        hoverColor  = style['hoverColor']
        selectColor = style['selectedColor']

        data = self.data()

        txts = [
            TTkString("◀┥",      hoverColor if self._hoverState == _FieldSelected.HOVER_LEFT  else color),
            TTkString(f"{data}", hoverColor if self._hoverState == _FieldSelected.HOVER_DATA  else color),
            TTkString("┝▶",      hoverColor if self._hoverState == _FieldSelected.HOVER_RIGHT else color),
            ]
        canvas.drawTTkString(pos=(0,0), text=TTkString().join(txts))


class _TTkDateYear(_TTkBaseMonthYear):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs|{'size':(8,1)})

    def data(self) -> str:
        return str(self._state._highlighted.year)

    def _show_chooser(self) -> None:
        year=self._state._date.year
        _frame = TTkResizableFrame(size=(7,12), border=True, layout=TTkGridLayout())
        _list = TTkList(parent=_frame, showSearch=False, size=(5,10))
        _list.addItems([str(_i) for _i in range(1900,2100)])
        _list.setCurrentRow(year-1900)
        _list.viewport().viewMoveTo(0,year-1900)

        @pyTTkSlot(str)
        def _yearSelected(yearTxt:str) -> None:
            year = int(yearTxt)
            _list.textClicked.clear()
            _frame.close()
            try:
                newDate = self._state._date.replace(year=year)
            except ValueError:
                # Handle Feb 29 on non-leap years - move to Feb 28
                newDate = self._state._date.replace(year=year, day=28)
            self._state.setDate(newDate)
            self.setFocus()

        _list.textClicked.connect(_yearSelected)
        TTkHelper.overlay(self, _frame, 1, -1)

    def _goto_next(self) -> None:
        ordinal = self._state._date.toordinal()
        days_in_month = 365 # 366 if calendar.isleap(month) else 365
        self._state.setDate(datetime.date.fromordinal(max(1,ordinal+days_in_month)))

    def _goto_prev(self) -> None:
        ordinal = self._state._date.toordinal()
        days_in_month = 365 # 366 if calendar.isleap(month) else 365
        self._state.setDate(datetime.date.fromordinal(max(1,ordinal-days_in_month)))


class _TTkDateMonth(_TTkBaseMonthYear):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs|{'size':(7,1)})

    def data(self) -> str:
        return _month_to_str_slim.get(self._state._highlighted.month, 'XXX')

    def _show_chooser(self) -> None:
        month=self._state._date.month
        _frame = TTkResizableFrame(size=(7,12), border=True, layout=TTkGridLayout())
        _list = TTkList(parent=_frame, showSearch=False, size=(5,10))
        _list.addItems([_m for _m in _month_to_str_slim.values()])
        _list.setCurrentRow(month-1)
        _list.viewport().viewMoveTo(0,month-1)

        @pyTTkSlot(str)
        def _monthSelected(monthTxt:str) -> None:
            month = {_v:_k for _k,_v in _month_to_str_slim.items()}.get(str(monthTxt),1)
            _list.textClicked.clear()
            _frame.close()
            try:
                newDate = self._state._date.replace(month=month)
            except ValueError:
                # Handle Feb 29 on non-leap months - move to Feb 28
                newDate = self._state._date.replace(month=month, day=28)
            self._state.setDate(newDate)
            self.setFocus()

        _list.textClicked.connect(_monthSelected)
        TTkHelper.overlay(self, _frame, 1, -1)

    def _goto_next(self) -> None:
        year = self._state._date.year
        month = self._state._date.month
        days_in_month = calendar.monthrange(year, month)[1]
        ordinal = self._state._date.toordinal()
        self._state.setDate(datetime.date.fromordinal(max(1,ordinal+days_in_month)))

    def _goto_prev(self) -> None:
        year = self._state._date.year
        month = max(1,min(12,self._state._date.month-1))
        days_in_month = calendar.monthrange(year, month)[1]
        ordinal = self._state._date.toordinal()
        self._state.setDate(datetime.date.fromordinal(max(1,ordinal-days_in_month)))


class _TTkDateCal(TTkWidget):
    classStyle = {
                'default':     {'color':            TTkColor.fgbg("#888888","#222222")+TTkColor.UNDERLINE,
                                'color2':           TTkColor.fgbg("#888888","#222222"),
                                'colorSeparator':   TTkColor.fgbg("#CCCC00","#222222")+TTkColor.UNDERLINE,
                                'hoverColor':       TTkColor.fgbg("#ffffff","#00AA66")+TTkColor.UNDERLINE,
                                'highlightedColor': TTkColor.fgbg("#ffffff","#00AA88")+TTkColor.UNDERLINE,
                                'selectedColor':    TTkColor.fgbg("#ffffff","#008844")+TTkColor.UNDERLINE},
                'hover':       {'color':            TTkColor.fgbg("#AAAAAA","#000066")+TTkColor.UNDERLINE},
                'disabled':    {'color':            TTkColor.fg(  "#444444")+TTkColor.UNDERLINE,
                                'colorSeparator':   TTkColor.fgbg("#666666","#222222")+TTkColor.UNDERLINE,
                                'selectedColor':    TTkColor.fgbg("#888888","#444444")+TTkColor.UNDERLINE},
                'focus':       {'color':            TTkColor.fgbg("#888888","#000066")+TTkColor.UNDERLINE}
            }

    __slots__ = ('_state')

    _state:_TTkDateWidgetState

    def __init__(self, *,
                 state: _TTkDateWidgetState,
                 **kwargs) -> None:
        self._state = state
        super().__init__(**kwargs|{'size':(20,6)})
        self.setFocusPolicy(TTkK.ClickFocus | TTkK.TabFocus)
        self._state.dateChanged.connect(self.update)
        self._state.highlightedChanged.connect(self.update)

    def focusOutEvent(self):
        self._state.clearHover()
        return super().focusOutEvent()

    def keyEvent(self, evt:TTkKeyEvent) -> bool:
        if ( evt.type == TTkK.SpecialKey and
             evt.key in (
                 TTkK.Key_Enter,
                 TTkK.Key_Right, TTkK.Key_Left,
                 TTkK.Key_Down,  TTkK.Key_Up)):
            if evt.key == TTkK.Key_Enter:
                self._state.setDate(self._state._highlighted)
                self.update()
                return True
            ordinal = self._state._highlighted.toordinal()
            if evt.key == TTkK.Key_Right:
                ordinal += 1
            if evt.key == TTkK.Key_Left:
                ordinal -= 1
            elif evt.key == TTkK.Key_Up:
                ordinal -= 7
            elif evt.key == TTkK.Key_Down:
                ordinal += 7
            self._state.setHighlightedDate(datetime.date.fromordinal(ordinal))
            self.update()
            return True
        elif evt.key == ' ':
            self._state.setDate(self._state._highlighted)
            self.update()
            return True
        return False

    def _getDayFromPos(self, x:int, y:int) -> Optional[datetime.date]:
        month_calendar = self._state._month_calendar
        col = x//3
        row = y
        if row < len(month_calendar) and 0<=col<7:
            return month_calendar[row][col]
        return None

    def mousePressEvent(self, evt:TTkMouseEvent) -> bool:
        x,y = evt.x,evt.y
        self._state.clearSelected()
        if 0 <= y <= 5 and 0 <= x < 20:
            if _d := self._getDayFromPos(x,y):
                self._state.setDate(_d)
            self.update()
        return True

    def mouseMoveEvent(self, evt:TTkMouseEvent) -> bool:
        x,y = evt.x,evt.y
        self._state.clearHover()
        if 0 <= y <= 5 and 0 <= x < 20:
            self._state._hovered = self._getDayFromPos(x,y)
            self.update()
        return True

    def leaveEvent(self, evt:TTkMouseEvent) -> bool:
        self._state.clearHover()
        super().leaveEvent(evt)

    # def wheelEvent(self, evt:TTkMouseEvent) -> bool:
    #     return True

    def paintEvent(self, canvas):
        #     October 2025
        # Su Mo Tu We Th Fr Sa
        #         1  2  3  4
        # 5  6  7  8  9 10 11
        # 12 13 14 15 16 17 18
        # 19 20 21 22 23 24 25
        # 26 27 28 29 30 31
        style = self.currentStyle()

        color            = style['color']
        color2           = style['color2']
        colorSep         = style['colorSeparator']
        hoverColor       = style['hoverColor']
        highlightedColor = style['highlightedColor']
        selectColor      = style['selectedColor']

        month_calendar = self._state._month_calendar

        hovered = self._state._hovered
        selected = self._state._selected
        highlighted = self._state._highlighted
        for i, week in enumerate(month_calendar):
            week_strs = []
            for _day in week:
                if _day==hovered:
                    week_strs.append(TTkString(f"{_day.day:2d}",hoverColor) + TTkString(" "))
                elif _day==highlighted:
                    week_strs.append(TTkString(f"{_day.day:2d}",highlightedColor) + TTkString(" "))
                elif _day==selected:
                    week_strs.append(TTkString(f"{_day.day:2d}",selectColor) + TTkString(" "))
                elif _day.month == highlighted.month:
                    week_strs.append(TTkString(f"{_day.day:2d}",color) + TTkString(" "))
                else:
                    week_strs.append(TTkString(f"{_day.day:2d}",color2) + TTkString(" "))
            canvas.drawTTkString(pos=(0,i), text=TTkString('').join(week_strs))


class TTkDateForm(TTkContainer):

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

    __slots__ = (
        '_state',
        '_calWidget', '_yearWidget', '_monthWidget',
        'dateChanged')

    dateChanged:pyTTkSignal
    _calWidget:_TTkDateCal
    _yearWidget:_TTkDateYear
    _monthWidget:_TTkDateMonth
    _state:_TTkDateWidgetState

    def __init__(self, *,
                 date:Optional[datetime.date]=None,
                 **kwargs) -> None:
        if not date:
            date = datetime.date.today()
        self._state = _TTkDateWidgetState(date=date)
        self._state.highlightedChanged.connect(self.update)
        self.dateChanged = self._state.dateChanged
        _layout=TTkLayout()
        size = (20,8)
        super().__init__(**kwargs|{'layout':_layout, 'size':size, 'minSize':size})
        self._calWidget = _TTkDateCal(parent=self, pos=(0,2), state=self._state)
        self._yearWidget = _TTkDateYear(parent=self, pos=(2,0), state=self._state)
        self._monthWidget = _TTkDateMonth(parent=self, pos=(12,0), state=self._state)

    def date(self) -> datetime.date:
        return self._state._date

    @pyTTkSlot(datetime.date)
    def setDate(self, date:datetime.date) -> None:
        if date != self._state._date:
            self._state.setDate(date=date)

    def paintEvent(self, canvas):
        style = self.currentStyle()

        color       = style['color']
        colorSep    = style['colorSeparator']
        hoverColor  = style['hoverColor']
        selectColor = style['selectedColor']

        header_days = TTkString('Su Mo Tu We Th Fr Sa')
        canvas.drawTTkString(pos=( 0,1), text=header_days)
