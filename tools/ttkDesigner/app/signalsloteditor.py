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
    __slots__ = ('_sender', '_signal', '_receiver', '_slot', '_designer', '_signalData', '_slotData', '_avoidRecursion')
    def __init__(self, designer, *args, **kwargs):
        self._designer = designer
        self._sender   = ttk.TTkComboBox(height=1, list=['<sender>'  ], index=0)
        self._signal   = ttk.TTkComboBox(height=1, list=['<signal>'  ], index=0)
        self._receiver = ttk.TTkComboBox(height=1, list=['<receiver>'], index=0)
        self._slot     = ttk.TTkComboBox(height=1, list=['<slot>'    ], index=0)
        self._signalData = {}
        self._slotData = {}
        self._avoidRecursion = False
        self._sender.currentTextChanged.connect(  self._senderChanged)
        self._signal.currentTextChanged.connect(  self._signalChanged)
        self._receiver.currentTextChanged.connect(self._receiverChanged)
        self._slot.currentTextChanged.connect(    self._slotChanged)
        self._designer.widgetNameChanged.connect( self._widgetNameChanged)
        self._designer.weModified.connect(self.updateWidgets)
        self.updateWidgets()
        super().__init__([self._sender,self._signal,self._receiver,self._slot], *args, **kwargs)

    def isValid(self):
        curSender   = str(self._sender.currentText())
        curReceiver = str(self._receiver.currentText())
        curSignal   = str(self._signal.currentText())
        curSlot     = str(self._slot.currentText())
        if curSender=='<sender>' or curReceiver == '<receiver>':
            return False
        ret = False
        for ccName in self._signalData:
            if curSignal in self._signalData[ccName]:
                ret = True
                break
        for ccName in self._slotData:
            if curSlot in self._slotData[ccName]:
                ret &= True
                break
        return ret

    def importConnection(self, connection):
        self._sender.setCurrentText(connection['sender'])
        self._receiver.setCurrentText(connection['receiver'])
        self._signal.setCurrentText(connection['signal'])
        self._slot.setCurrentText(connection['slot'])

    def dumpDict(self):
        curSender   = str(self._sender.currentText())
        curReceiver = str(self._receiver.currentText())
        curSignal   = str(self._signal.currentText())
        curSlot     = str(self._slot.currentText())
        return {
            'sender':   curSender,
            'receiver': curReceiver,
            'signal':   curSignal,
            'slot':     curSlot }

    @ttk.pyTTkSlot()
    def updateWidgets(self):
        self._widgetNameChanged()

    @staticmethod
    def typeToString(t):
        if type(t) in (list,tuple):
            return ",".join([_SignalSlotItem.typeToString(x) for x in t])
        return {bool    : 'bool',
                int     : 'int',
                float   : 'float',
                complex : 'complex',
                str     : 'str',
                None    : ''}.get(t,f"UNDEFINED {t}")

    @ttk.pyTTkSlot(str, str)
    def _widgetNameChanged(self, oldName='', newName=''):
        names = [w.name() for w in self._designer.getWidgets()]

        def _setCB(cb:ttk.TTkComboBox, base):
            text = cb.currentText()
            text = text if text!=oldName else newName
            cb.clear()
            cb.addItems([base]+names)
            cb.setCurrentText(text)

        _setCB(self._sender,   '<sender>')
        _setCB(self._receiver, '<receiver>')

    @ttk.pyTTkSlot(str)
    def _senderChanged(self, text):
        self._signalData, _ = self.getSignalSlot(text)
        self._refreshSignals()

    def _refreshSignals(self):
        curSignal = str(self._signal.currentText())
        curSlot = str(self._slot.currentText())
        filter = None
        for c in self._slotData:
            if not str(curSlot) in self._slotData[c]: continue
            filter = self._slotData[c][curSlot]['type']
            break

        signals = ['<signal>']
        for ccName in self._signalData:
            signals.append(ttk.TTkString(f"{ccName}:",ttk.TTkColor.fg("#FFFF88")+ttk.TTkColor.UNDERLINE))
            for s in self._signalData[ccName]:
                if filter in (None,self._signalData[ccName][s]['type']):
                    signals.append(s)
        self._signal.clear()
        self._signal.addItems(signals)
        self._signal.setCurrentText(curSignal)

    @ttk.pyTTkSlot(str)
    def _signalChanged(self, text):
        if self._avoidRecursion: return
        self._avoidRecursion = True
        self._refreshSlots()
        self._avoidRecursion = False


    @ttk.pyTTkSlot(str)
    def _receiverChanged(self, text):
        _, self._slotData = self.getSignalSlot(text)
        self._refreshSlots()

    def _refreshSlots(self):
        curSignal = self._signal.currentText()
        curSlot = self._slot.currentText()
        filter = 'ALL'
        for c in self._signalData:
            if not str(curSignal) in self._signalData[c]: continue
            filter = self._signalData[c][curSignal]['type']
            break

        slots = ['<slot>']
        for ccName in self._slotData:
            slots.append(ttk.TTkString(f"{ccName}:",ttk.TTkColor.fg("#FFFF88")+ttk.TTkColor.UNDERLINE))
            for s in self._slotData[ccName]:
                if filter in ('ALL',self._slotData[ccName][s]['type']) or not self._slotData[ccName][s]['type']:
                    slots.append(s)

        self._slot.clear()
        self._slot.addItems(slots)
        self._slot.setCurrentText(curSlot)

    @ttk.pyTTkSlot(str)
    def _slotChanged(self, text):
        if self._avoidRecursion: return
        self._avoidRecursion = True
        self._refreshSignals()
        self._avoidRecursion = False

    def getSignalSlot(self, name):
        if not (widget := {w.name():w for w in self._designer.getWidgets()}.get(name,None)):
            return {},{}
        ttk.TTkLog.debug(f"Selected {widget=}")
        slots = {}
        signals = {}
        for cc in reversed(type(widget).__mro__):
            if issubclass(cc, ttk.TTkWidget) or issubclass(cc, ttk.TTkLayout):
                ccName = cc.__name__
                if ccName in ttk.TTkUiProperties:
                    if ttk.TTkUiProperties[ccName]['slots']:
                        slots[ccName] = ttk.TTkUiProperties[ccName]['slots']
                    if ttk.TTkUiProperties[ccName]['signals']:
                        signals[ccName] = ttk.TTkUiProperties[ccName]['signals']
        return signals,slots

class SignalSlotEditor(ttk.TTkContainer):
    __slots__ = ('_items', '_designer')
    def __init__(self, designer, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setLayout(ttk.TTkGridLayout())
        self._items = []
        self._designer = designer

        self._detail = ttk.TTkTree()
        self._detail.setHeaderLabels(["Sender","Signal","Receiver","Slot"])
        self.layout().addWidget(addb := ttk.TTkButton(border=False, text="ADD"),1,1)
        self.layout().addWidget(delb := ttk.TTkButton(border=False, text="DEL"),1,2)
        self.layout().addWidget(ttk.TTkLabel(text=" Signal/Slot Editor "),1,3)
        self.layout().addWidget(self._detail,2,1,1,3)

        addb.clicked.connect(self._addStuff)
        delb.clicked.connect(self._delStuff)

    def _addStuff(self):
        item = _SignalSlotItem(self._designer)
        self._items.append(item)
        self._detail.addTopLevelItem(item)

    def _delStuff(self):
        if not (items := self._detail.selectedItems()):
            return
        for item in items:
            if (index := self._detail.indexOfTopLevelItem(item)) is not None:
                self._detail.takeTopLevelItem(index)

    def importConnections(self, connections):
        self._items = []
        self._detail.clear()
        for c in connections:
            item = _SignalSlotItem(self._designer)
            item.importConnection(c)
            self._items.append(item)
            self._detail.addTopLevelItem(item)

    def dumpDict(self):
        ret = []
        for i in self._items:
            if i.isValid():
                ret.append(i.dumpDict())
        return ret
