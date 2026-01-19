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

from __future__ import annotations

__all__ = ['PTP_TreeItem', 'PTP_TreeItemPath', 'PTP_TreeItemMethod']

from enum import IntEnum

import TermTk as ttk

from ttkode.app.ttkode import TTKodeFileWidgetItem

class _testStatus(IntEnum):
    Pass = 0x01
    Fail = 0x02
    Undefined = 0x03

_statusMarks = {
    _testStatus.Pass:      ttk.TTkString('✔ ', ttk.TTkColor.GREEN),
    _testStatus.Fail:      ttk.TTkString('x ', ttk.TTkColor.RED),
    _testStatus.Undefined: ttk.TTkString('○ ', ttk.TTkColor.fg('#888888')),
}

def _toMark(status:_testStatus) -> ttk.TTkString:
    return _statusMarks.get(status, ttk.TTkString('- '))

class PTP_TreeItem(TTKodeFileWidgetItem):
    __slots__ = ('_testStatus')
    def __init__(self, *args, testStatus:_testStatus=_testStatus.Undefined, **kwargs):
        self._testStatus = testStatus
        super().__init__(*args, **kwargs)

    def data(self, col, role = None) -> ttk.TTkString:
        return _toMark(self._testStatus) + super().data(col, role)

    def setTestStatus(self, status:_testStatus) -> None:
        if status == self._testStatus:
            return
        self._testStatus = status
        self.dataChanged.emit()

class PTP_TreeItemPath(PTP_TreeItem):
    pass

class PTP_TreeItemMethod(PTP_TreeItem):
    __slots__ = ('_test_call')
    def __init__(self, *args, **kwargs):
        path_method = kwargs.pop('path','')
        path = path_method.split('::')[0]
        mathods = path_method.split('::')[1:]
        super().__init__(*args, **kwargs|{'path':path})

    def test_call(self) -> str:
        return self._test_call