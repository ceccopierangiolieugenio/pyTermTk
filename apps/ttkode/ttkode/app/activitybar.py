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

__all__ = ['TTKodeActivityBar']

import TermTk as ttk
from typing import List

from dataclasses import dataclass

class _ActivityWidget(ttk.TTkRadioButton):
    classStyle = {
        'default':  {'color': ttk.TTkColor.RST},
        'disabled': {'color': ttk.TTkColor.fg('#888888')},
        'hover':    {'color': ttk.TTkColor.bg('#888800')}}
    __slots__ = ('_actionName', '_icon', '_widget')
    _actionName: ttk.TTkString
    _icon: List[ttk.TTkString]
    _widget: ttk.TTkWidget
    def __init__(self, actionName: ttk.TTkString, icon: ttk.TTkString, widget: ttk.TTkWidget, **kwargs):
        self._actionName = actionName
        self._icon = icon.split('\n')
        self._widget = widget
        width = max(i.termWidth() for i in self._icon)
        params = {
            'toolTip':actionName,
            'maxSize':(width,2),
            'minSize':(width,2),
            'size':(width,2),
            'radiogroup':'ttkodeActionBar'}
        super().__init__(**kwargs|params)

    def actionName(self) -> ttk.TTkString:
        return self._actionName
    def icon(self) -> List[ttk.TTkString]:
        return self._icon
    def widget(self) -> ttk.TTkWidget:
        return self._widget

    def paintEvent(self, canvas):
        style = self.currentStyle()
        iconLine1 = self._icon[0].setColor(style['color'])
        iconLine2 = self._icon[1].setColor(style['color'])
        canvas.drawTTkString(pos=(0,0),text=iconLine1)
        if self.isChecked():
            canvas.drawTTkString(pos=(0,1),text=iconLine2.setColor(ttk.ttk.TTkColor.UNDERLINE))
        else:
            canvas.drawTTkString(pos=(0,1),text=iconLine2)


class _SideBar(ttk.TTkLayout):
    __slots__ = ('_sideWidgets', '_position')
    _sideWidgets:List[_ActivityWidget]
    _position:int
    def __init__(self, position:int=ttk.TTkK.TOP, **kwargs) -> None:
        self._sideWidgets = []
        self._position = position
        params = {
            'maxHeight':2,
            'minHeught':2}
        super().__init__(**kwargs|params)

    def _refreshItems(self) -> None:
        x = 1
        for wid in self._sideWidgets:
            wid.move(x,0)
            x+=wid.width()+1

    def activities(self) -> List[_ActivityWidget]:
        return self._sideWidgets

    def addActivity(self, widget: _ActivityWidget):
        self._sideWidgets.append(widget)
        self.addWidget(widget)
        self._refreshItems()
        self.update()

    def removeActivity(self, widget: _ActivityWidget):
        self._sideWidgets.remove(widget)
        self.removeWidget(widget)
        self._refreshItems()
        self.update()

    def clearActivities(self) -> None:
        self.removeWidgets(self._sideWidgets)
        self._sideWidgets.clear()
        self.update()


class TTKodeActivityBar(ttk.TTkVBoxLayout):
    __slots__ = ('_sideBar')
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._sideBar = _SideBar()
        self.addItem(self._sideBar)

    @ttk.pyTTkSlot()
    def _activityChanged(self) -> None:
        for act in self._sideBar.activities():
            if act.isChecked():
                act.widget().setVisible(True)
            else:
                act.widget().setVisible(False)

    def addActivity(
            self,
            name: ttk.TTkString,
            icon: ttk.TTkString,
            widget: ttk.TTkWidget,
            select:bool=False) -> None:
        activityWidget = _ActivityWidget(name, icon, widget)
        self.addWidget(widget)
        widget.setVisible(False)
        activityWidget.toggled.connect(self._activityChanged)
        self._sideBar.addActivity(activityWidget)
        if select:
            activityWidget.setChecked(True)
            widget.setVisible(True)

