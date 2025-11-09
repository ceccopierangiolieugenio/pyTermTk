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

__all__ = ['TTkDateTime']

import datetime as dt

from typing import Optional

from TermTk.TTkCore.signal import pyTTkSignal, pyTTkSlot
from TermTk.TTkWidgets.container import TTkContainer
from TermTk.TTkWidgets.datetime_date import TTkDate
from TermTk.TTkWidgets.datetime_time import TTkTime

class TTkDateTime(TTkContainer):
    ''' TTkDateTime:

    A composite widget for displaying and editing date and time values.

    Combines :class:`~TermTk.TTkWidgets.datetime_date.TTkDate` and :class:`~TermTk.TTkWidgets.datetime_time.TTkTime` widgets
    into a single datetime editor. (`demo <https://ceccopierangiolieugenio.github.io/pyTermTk-Docs/sandbox/sandbox.html?filePath=demo/showcase/date_time.py>`__)

    ::

        2025/11/04 📅 12:30:45

    .. code:: python

        import TermTk as ttk

        root = ttk.TTk()

        ttk.TTkDateTime(parent=root) # Defaults to the current datetime

        root.mainloop()

    :param datetime: The initial datetime to display, defaults to the current datetime.
    :type datetime: :py:class:`datetime.datetime`, optional
    '''

    __slots__ = (
        '_datetime',
        '_dateWidget', '_timeWidget',
        # Signals
        'datetimeChanged')

    datetimeChanged:pyTTkSignal
    '''
    This signal is emitted whenever the datetime changes.

    :param datetime: The new datetime value
    :type datetime: :py:class:`datetime.datetime`
    '''

    _datetime:dt.datetime
    _dateWidget:TTkDate
    _timeWidget:TTkTime

    def __init__(self, *,
                 datetime:Optional[dt.datetime]=None,
                 **kwargs) -> None:
        '''
        Initializes the TTkDateTime widget.

        :param datetime: The initial datetime to display. If None, the current datetime is used.
        :type datetime: :py:class:`datetime.datetime`, optional
        '''
        self.datetimeChanged = pyTTkSignal(dt.datetime)
        if not datetime:
            datetime = dt.datetime.now().replace(microsecond=0)
        self._datetime = datetime
        size = (13+1+8,1)
        super().__init__(**kwargs|{'size':size, 'minSize':size})
        self._dateWidget = TTkDate(parent=self, pos=( 0,0), date=datetime.date())
        self._timeWidget = TTkTime(parent=self, pos=(14,0), time=datetime.time())
        self._dateWidget.dateChanged.connect(self._somethingChanged)
        self._timeWidget.timeChanged.connect(self._somethingChanged)

    @pyTTkSlot()
    def _somethingChanged(self) -> None:
        '''
        Internal slot that synchronizes the datetime value when either date or time changes.
        '''
        self.setDatetime(
            self._datetime.combine(
                date=self._dateWidget.date(),
                time=self._timeWidget.time()))

    def datetime(self) -> dt.datetime:
        '''
        Returns the current datetime of the widget.

        :return: The current datetime
        :rtype: :py:class:`datetime.datetime`
        '''
        return self._datetime

    @pyTTkSlot(dt.datetime)
    def setDatetime(self, datetime:dt.datetime) -> None:
        '''
        Sets the current datetime of the widget.

        This updates both the internal date and time widgets and emits the
        :py:attr:`datetimeChanged` signal if the value changes.

        :param datetime: The new datetime to set
        :type datetime: :py:class:`datetime.datetime`
        '''
        if datetime != self._datetime:
            self._datetime = datetime
            self._dateWidget.setDate(datetime.date())
            self._timeWidget.setTime(datetime.time())
            self.datetimeChanged.emit(datetime)