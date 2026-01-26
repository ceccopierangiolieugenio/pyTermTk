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

__all__ = [
    'PTP_Tree',
    'PTP_Action',
    'PTP_TreeItem', 'PTP_TreeItemPath', 'PTP_TreeItemMethod']

from enum import IntEnum
from dataclasses import dataclass
from typing import Optional

import TermTk as ttk

from _030.pytest_data import PTP_Node
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

class PTP_TreeItem(ttk.TTkTreeWidgetItem):
    __slots__ = ('_testStatus', '_ptp_node', '_test_id')
    def __init__(self, name:str, test_id:str, node:PTP_Node, testStatus:_testStatus=_testStatus.Undefined, **kwargs):
        self._testStatus = testStatus
        self._ptp_node = node
        self._test_id = test_id
        super().__init__([ttk.TTkString(name)], **kwargs)

    def test_id(self) -> str:
        return self._test_id

    def node(self) -> PTP_Node:
        return self._ptp_node

    def data(self, col, role = None) -> ttk.TTkString:
        return _toMark(self._testStatus) + super().data(col, role)

    def testStatus(self) -> _testStatus:
        return self._testStatus

    def setTestStatus(self, status:_testStatus) -> None:
        if status == self._testStatus:
            return
        self._testStatus = status
        self.dataChanged.emit()

class PTP_TreeItemPath(PTP_TreeItem):
    pass

class PTP_TreeItemMethod(PTP_TreeItem):
    pass


@dataclass
class _PTP_Highlight():
    pos:int
    run:bool
    item:PTP_TreeItem

@dataclass
class PTP_Action():
    item:PTP_TreeItem

class PTP_TreeWidget(ttk.TTkTreeWidget):
    __slots__ = ('_PTP_highight', 'actionPressed')

    _PTP_highight:Optional[_PTP_Highlight]

    def __init__(self, **kwargs):
        self._PTP_highight = None
        self.actionPressed = ttk.pyTTkSignal(PTP_Action)
        super().__init__(**kwargs)
        self.mergeStyle({'default':{'hoveredColor':ttk.TTkColor.bg('#666666')}})

    def mousePressEvent(self, evt:ttk.TTkMouseEvent) -> bool:
        y,x = evt.y, evt.x
        w = self.width()
        if (_item:=self.itemAt(y)) and x>=w-3:
            self.actionPressed.emit(PTP_Action(item=_item))
            self.update()
            return True
        return super().mousePressEvent(evt)

    def mouseMoveEvent(self, evt:ttk.TTkMouseEvent) -> bool:
        y,x = evt.y, evt.x
        w = self.width()
        if _item:=self.itemAt(y):
            self._PTP_highight = _PTP_Highlight(
                pos=evt.y,
                run=x>=w-3,
                item=_item
            )
            self.update()
        elif self._PTP_highight is not None:
            self._PTP_highight = None
            self.update()
        return super().mouseMoveEvent(evt)

    def leaveEvent(self, evt:ttk.TTkMouseEvent) -> bool:
        if self._PTP_highight is not None:
            self._PTP_highight = None
            self.update()
        super().leaveEvent(evt)

    def paintEvent(self, canvas:ttk.TTkCanvas) -> None:
        super().paintEvent(canvas)
        style = self.currentStyle()
        hoveredColor=style['hoveredColor']
        if _ph:=self._PTP_highight:
            w = self.width()
            if _ph.run:
                canvas.drawText(text='...[ ]', pos=(w-6,_ph.pos), color=hoveredColor+ttk.TTkColor.YELLOW+ttk.TTkColor.BOLD)
                canvas.drawText(text=    '▶' , pos=(w-2,_ph.pos), color=hoveredColor+ttk.TTkColor.RED)
            else:
                canvas.drawText(text='...[ ]', pos=(w-6,_ph.pos), color=hoveredColor+ttk.TTkColor.YELLOW+ttk.TTkColor.BOLD)
                canvas.drawText(text=    '▶' , pos=(w-2,_ph.pos), color=hoveredColor+ttk.TTkColor.GREEN)
                # canvas.drawText(text=  '▷'  , pos=(w-3,_ph.pos), color=hoveredColor+ttk.TTkColor.GREEN)


class PTP_Tree(ttk.TTkTree):
    __slots__ = ('actionPressed')
    def __init__(self, **kwargs):
        tw = PTP_TreeWidget(**kwargs)
        super().__init__(treeWidget=tw, **kwargs)
        self.actionPressed = tw.actionPressed
