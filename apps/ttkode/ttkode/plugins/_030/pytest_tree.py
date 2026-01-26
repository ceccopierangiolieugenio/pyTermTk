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

''' PyTest Tree Widget Components

This module provides specialized tree widget components for displaying pytest
test hierarchies with visual status indicators and interactive controls for
running individual tests or test groups.
'''

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
    ''' Test status enumeration for visual indicators

    Represents the current state of a test item in the tree.
    '''
    Pass = 0x01
    Fail = 0x02
    Undefined = 0x03

_statusMarks = {
    _testStatus.Pass:      ttk.TTkString('✔ ', ttk.TTkColor.GREEN),
    _testStatus.Fail:      ttk.TTkString('x ', ttk.TTkColor.RED),
    _testStatus.Undefined: ttk.TTkString('○ ', ttk.TTkColor.fg('#888888')),
}

def _toMark(status:_testStatus) -> ttk.TTkString:
    ''' Convert test status to colored visual mark

    :param status: the test status
    :type status: _testStatus

    :return: colored status mark (✔, x, or ○)
    :rtype: :py:class:`TTkString`
    '''
    return _statusMarks.get(status, ttk.TTkString('- '))

class PTP_TreeItem(ttk.TTkTreeWidgetItem):
    ''' Base tree item for pytest test nodes

    Extends :py:class:`TTkTreeWidgetItem` to add test-specific functionality including
    status tracking and visual indicators.

    :param name: display name for the tree item
    :type name: str
    :param test_id: unique pytest node ID
    :type test_id: str
    :param node: associated pytest node data
    :type node: PTP_Node
    :param testStatus: initial test status
    :type testStatus: _testStatus
    '''
    __slots__ = ('_testStatus', '_ptp_node', '_test_id')
    def __init__(self, name:str, test_id:str, node:PTP_Node, testStatus:_testStatus=_testStatus.Undefined, **kwargs):
        self._testStatus = testStatus
        self._ptp_node = node
        self._test_id = test_id
        super().__init__([ttk.TTkString(name)], **kwargs)

    def test_id(self) -> str:
        ''' Get the pytest node ID for this item

        :return: the test ID path
        :rtype: str
        '''
        return self._test_id

    def node(self) -> PTP_Node:
        ''' Get the pytest node data

        :return: the associated node data
        :rtype: PTP_Node
        '''
        return self._ptp_node

    def data(self, col, role = None) -> ttk.TTkString:
        ''' Get display data with status mark prefix

        :param col: column index
        :type col: int
        :param role: data role (unused)
        :type role: Optional[Any]

        :return: formatted string with status mark
        :rtype: :py:class:`TTkString`
        '''
        return _toMark(self._testStatus) + super().data(col, role)

    def testStatus(self) -> _testStatus:
        ''' Get the current test status

        :return: the test status
        :rtype: _testStatus
        '''
        return self._testStatus

    def clearTestStatus(self, clearParent:bool=False, clearChildren:bool=False) -> None:
        ''' Clear test status to undefined

        :param clearParent: whether to recursively clear parent status
        :type clearParent: bool
        :param clearChildren: whether to recursively clear children status
        :type clearChildren: bool
        '''
        if self._testStatus is _testStatus.Undefined:
            return
        self._testStatus = _testStatus.Undefined
        if clearParent:
            if isinstance(self._parent, PTP_TreeItem):
                self._parent.clearTestStatus(clearParent=True)
        self.dataChanged.emit()

    def setTestStatus(self, status:_testStatus) -> None:
        ''' Set the test status and update parent if needed

        :param status: the new test status
        :type status: _testStatus
        '''
        if status == self._testStatus:
            return
        self._testStatus = status
        if isinstance(self._parent, PTP_TreeItemPath):
            self._parent._updateTestStatus(status=status)
        self.dataChanged.emit()

class PTP_TreeItemPath(PTP_TreeItem):
    ''' Tree item representing a test path or directory

    Aggregates status from child test items - shows failure if any child fails.
    '''
    def _updateTestStatus(self, status:_testStatus):
        ''' Update status based on child test statuses

        :param status: the new status to propagate
        :type status: _testStatus
        '''
        fail = any(_c.testStatus() == _testStatus.Fail for _c in self.children() if isinstance(_c, PTP_TreeItem))
        self._testStatus = _testStatus.Fail if fail else status
        if isinstance(self._parent, PTP_TreeItemPath):
            self._parent._updateTestStatus(status=status)
        self.dataChanged.emit()

    def clearTestStatus(self, clearParent:bool=False, clearChildren:bool=False) -> None:
        if clearChildren:
            for _c in self.children():
                if isinstance(_c, PTP_TreeItem):
                    _c.clearTestStatus(clearChildren=True)
        super().clearTestStatus(clearParent=clearParent)

class PTP_TreeItemMethod(PTP_TreeItem):
    ''' Tree item representing an individual test method

    Leaf node in the test tree hierarchy.
    '''
    pass


@dataclass
class _PTP_Highlight():
    ''' Internal state for mouse hover highlighting

    :param pos: vertical position of the highlight
    :type pos: int
    :param run: whether mouse is over the run button area
    :type run: bool
    :param item: the highlighted tree item
    :type item: PTP_TreeItem
    '''
    pos:int
    run:bool
    item:PTP_TreeItem

@dataclass
class PTP_Action():
    ''' Action data emitted when a test run button is clicked

    :param item: the test item to run
    :type item: PTP_TreeItem
    '''
    item:PTP_TreeItem

class PTP_TreeWidget(ttk.TTkTreeWidget):
    ''' Custom tree widget with interactive run buttons

    Extends :py:class:`TTkTreeWidget` to add per-item run buttons that appear
    on mouse hover, allowing individual test or test group execution.

    ::

        ✔ test_module.py        ...[ ]▶
          ○ test_pending
          x test_failed

    '''
    __slots__ = ('_PTP_highight', 'actionPressed')

    _PTP_highight:Optional[_PTP_Highlight]
    actionPressed: ttk.pyTTkSignal
    '''
    This signal is emitted when a run button is clicked.

    :param action: the action containing the item to run
    :type action: PTP_Action
    '''

    def __init__(self, **kwargs):
        self._PTP_highight = None
        self.actionPressed = ttk.pyTTkSignal(PTP_Action)
        super().__init__(**kwargs)
        self.mergeStyle({'default':{'hoveredColor':ttk.TTkColor.bg('#666666')}})

    def mousePressEvent(self, evt:ttk.TTkMouseEvent) -> bool:
        ''' Handle mouse press events for run button activation

        :param evt: the mouse event
        :type evt: :py:class:`TTkMouseEvent`

        :return: True if event was handled
        :rtype: bool
        '''
        y,x = evt.y, evt.x
        w = self.width()
        if (_item:=self.itemAt(y)) and x>=w-3:
            self.actionPressed.emit(PTP_Action(item=_item))
            self.update()
            return True
        return super().mousePressEvent(evt)

    def mouseMoveEvent(self, evt:ttk.TTkMouseEvent) -> bool:
        ''' Handle mouse movement to update hover highlighting

        :param evt: the mouse event
        :type evt: :py:class:`TTkMouseEvent`

        :return: True if event was handled
        :rtype: bool
        '''
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
        ''' Clear highlighting when mouse leaves widget

        :param evt: the mouse event
        :type evt: :py:class:`TTkMouseEvent`

        :return: True if event was handled
        :rtype: bool
        '''
        if self._PTP_highight is not None:
            self._PTP_highight = None
            self.update()
        super().leaveEvent(evt)

    def paintEvent(self, canvas:ttk.TTkCanvas) -> None:
        ''' Paint the tree with interactive run buttons on hover

        :param canvas: the canvas to paint on
        :type canvas: :py:class:`TTkCanvas`
        '''
        super().paintEvent(canvas)
        style = self.currentStyle()
        hoveredColor=style['hoveredColor']
        if _ph:=self._PTP_highight:
            w = self.width()
            if _ph.run:
                canvas.drawText(text='[ ]', pos=(w-3,_ph.pos), color=hoveredColor+ttk.TTkColor.YELLOW+ttk.TTkColor.BOLD)
                canvas.drawText(text= '▶' , pos=(w-2,_ph.pos), color=hoveredColor+ttk.TTkColor.RED)
            else:
                canvas.drawText(text='[ ]', pos=(w-3,_ph.pos), color=hoveredColor+ttk.TTkColor.YELLOW+ttk.TTkColor.BOLD)
                canvas.drawText(text= '▶' , pos=(w-2,_ph.pos), color=hoveredColor+ttk.TTkColor.GREEN)
                # canvas.drawText(text=  '▷'  , pos=(w-3,_ph.pos), color=hoveredColor+ttk.TTkColor.GREEN)


class PTP_Tree(ttk.TTkTree):
    ''' Pytest tree container with scrollable view

    Wraps :py:class:`PTP_TreeWidget` in a scrollable :py:class:`TTkTree` container,
    exposing the actionPressed signal for test execution.
    '''
    __slots__ = ('actionPressed')
    actionPressed: ttk.pyTTkSignal
    '''
    This signal is emitted when a run button is clicked.

    :param action: the action containing the item to run
    :type action: PTP_Action
    '''

    def __init__(self, **kwargs):
        tw = PTP_TreeWidget(**kwargs)
        super().__init__(treeWidget=tw, **kwargs)
        self.actionPressed = tw.actionPressed
