# MIT License
#
# Copyright (c) 2023 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

import TermTk as ttk

from .superobj.superwidget import SuperWidget
from .superobj.superlayout import SuperLayout

class _SignalSlotItem(ttk.TTkTreeWidgetItem):
    __slots__ = ('_sender', '_signal', '_receiver', '_slot')
    def __init__(self, *args, **kwargs):
        self._sender   = ttk.TTkComboBox(height=1, list=['<sender>'  ], index=0)
        self._signal   = ttk.TTkComboBox(height=1, list=['<signal>'  ], index=0)
        self._receiver = ttk.TTkComboBox(height=1, list=['<receiver>'], index=0)
        self._slot     = ttk.TTkComboBox(height=1, list=['<slot>'    ], index=0)
        super().__init__([self._sender,self._signal,self._receiver,self._slot], *args, **kwargs)

    def updateWidgets(self, widgets):
        names = [w.name() for w in widgets]
        self._sender.addItems(names)
        self._receiver.addItems(names)

class SignalSlotEditor(ttk.TTkWidget):
    __slots__ = ('_items', '_windowEditor')
    def __init__(self, windowEditor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setLayout(ttk.TTkGridLayout())
        self._items = []
        self._windowEditor = windowEditor

        self._detail = ttk.TTkTree()
        self._detail.setHeaderLabels(["Sender","Signal","Receiver","Slot"])
        self.layout().addWidget(addb := ttk.TTkButton(border=False, text="ADD"),1,1)
        self.layout().addWidget(delb := ttk.TTkButton(border=False, text="DEL"),1,2)
        self.layout().addWidget(ttk.TTkLabel(text=" Signal/Slot Editor "),1,3)
        self.layout().addWidget(self._detail,2,1,1,3)

        addb.clicked.connect(self._addStuff)

    def _addStuff(self):
        item = _SignalSlotItem()
        item.updateWidgets(self._getWidgets())
        self._items.append(item)
        self._detail.addTopLevelItem(item)

    def _getWidgets(self):
        widgets = []
        def _getItems(layoutItem):
            if layoutItem.layoutItemType == ttk.TTkK.WidgetItem:
                superThing = layoutItem.widget()
                if issubclass(type(superThing), SuperWidget):
                    widgets.append(superThing._wid)

                for c in superThing.layout().children():
                    _getItems(c)
        _getItems(self._windowEditor.getTTk().widgetItem())
        return widgets

