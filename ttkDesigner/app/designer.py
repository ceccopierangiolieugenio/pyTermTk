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

import os
import json

from TermTk import  TTkK, TTkLog, TTkColor, TTkHelper, TTkShortcut
from TermTk import TTkString
from TermTk import pyTTkSlot, pyTTkSignal

from TermTk import TTkWidget, TTkFrame, TTkButton, TTkLabel, TTkMenuButton
from TermTk import TTkTabWidget
from TermTk import TTkFileDialogPicker, TTkMessageBox

from TermTk import  TTkGridLayout, TTkVBoxLayout, TTkHBoxLayout
from TermTk import TTkSplitter
from TermTk import TTkLogViewer
from TermTk import TTkUiLoader, TTkUtil

from .cfg  import *
from .about import *
from .widgetbox import WidgetBoxScrollArea
from .windoweditor import WindowEditor
from .treeinspector import TreeInspector
from .propertyeditor import PropertyEditor
from .signalsloteditor import SignalSlotEditor
from .quickexport import QuickExport
from .notepad import NotePad

from .superobj import SuperWidget, SuperWidgetFrame

import pickle

#
#      Mimic the QT Designer layout
#
#      ┌─────────────────────╥───────────────────────────────╥───────────────────┐
#      │                     ║┌─────────────────────────────┐║                   │
#      │                     ║│       ToolBar               │║  Tree Inspector   │
#      │                     ║├─────────────────────────────┤║                   │
#      │                     ║│                             │║                   │
#      │   Widget            ║│                             │║                   │
#      │   Box               ║│                             │╠═══════════════════╡
#      │                     ║│      Main Window            │║                   │
#      │                     ║│      Editor                 │║   Property        │
#      │                     ║│                             │║   Editor          │
#      │                     ║│                             │║                   │
#      │                     ║│                             │║                   │
#      │                     ║│                             │║                   │
#      │                     ║│                             │║                   │
#      │                     ║│                             │╠═══════════════════╡
#      │                     ║│                             │║                   │
#      │                     ║└─────────────────────────────┘║   Signal/Slot     │
#      │                     ╟───────────────────────────────╢                   │
#      │                     ║     LOG Viewer                ║   Editor          │
#      │                     ║                               ║                   │
#      └─────────────────────╨───────────────────────────────╨───────────────────┘
#

class TTkDesigner(TTkGridLayout):
    __slots__ = ('_main', '_toolBar', '_fileNameLabel',
                 '_sigslotEditor', '_treeInspector', '_windowEditor', '_notepad',
                 '_fileName', '_currentPath',
                 '_snapshot', '_snapId',
                 # Signals
                 'weModified', 'thingSelected', 'widgetNameChanged'
                 )
    def __init__(self, fileName=None, *args, **kwargs):
        self._snapshot = []
        self._snapId = -1
        self._fileName = "untitled.tui.json"
        self._currentPath = self._currentPath =  os.path.abspath('.')

        self.weModified = pyTTkSignal()
        self.thingSelected = pyTTkSignal(TTkWidget, TTkWidget)
        self.widgetNameChanged = pyTTkSignal(str, str)

        super().__init__(*args, **kwargs)

        self.addWidget(mainSplit := TTkSplitter())
        mainSplit.addItem(widgetBoxLayout := TTkVBoxLayout())
        #mainSplit.addWidget(TTkButton(text='A',border=True))

        # mainSplit.addWidget(sa := TTkScrollArea())
        # sa.viewport().setLayout(TTkGridLayout())
        # sa.viewport().layout().addWidget(WindowEditor())

        self._notepad = NotePad()
        self._main = TTkVBoxLayout()
        self._toolBar = TTkHBoxLayout()
        self._windowEditor = WindowEditor(self)
        self._sigslotEditor = SignalSlotEditor(self)
        self._treeInspector = TreeInspector(self, self._windowEditor.viewport())
        self._fileNameLabel = TTkLabel(text=f"( {self._fileName} )", alignment=TTkK.CENTER_ALIGN)

        widgetBoxLayout.addWidget(topMenuFrame := TTkFrame(minHeight=1,maxHeight=1,border=False))
        widgetBoxLayout.addWidget(WidgetBoxScrollArea(self))

        self._main.addItem(self._toolBar)
        self._main.addWidget(self._windowEditor)

        mainSplit.addWidget(centralSplit := TTkSplitter(orientation=TTkK.VERTICAL))
        centralSplit.addWidget(self._main)
        centralSplit.addWidget(bottonTabWidget := TTkTabWidget(border=False))
        # centralSplit.addWidget(TTkLogViewer())
        bottonTabWidget.addTab(self._sigslotEditor,'Signal/Slot Editor')
        bottonTabWidget.addTab(TTkLogViewer(),'Logs')

        mainSplit.addWidget(rightSplit := TTkSplitter(orientation=TTkK.VERTICAL))

        rightSplit.addItem(self._treeInspector)
        rightSplit.addItem(propertyEditor := PropertyEditor(), title="Property Editor")
        # rightSplit.addItem(self._sigslotEditor)

        self.thingSelected.connect(lambda _,s : s.pushSuperControlWidget() if s.hasControlWidget() else None)
        self.thingSelected.connect(propertyEditor.setDetail)

        self.weModified.connect(self._treeInspector.refresh)
        self.weModified.connect(self._takeSnapshot)

        fileMenu = topMenuFrame.newMenubarTop().addMenu("&File")
        fileMenu.addMenu("&New").menuButtonClicked.connect(self.new)
        fileMenu.addMenu("&Open").menuButtonClicked.connect(self.open)
        fileMenu.addMenu("&Save").menuButtonClicked.connect(self.save)
        fileMenu.addMenu("Save &As...").menuButtonClicked.connect(self.saveAs)
        fileMenu.addSpacer()
        fileMenu.addMenu("&Import 🎁").menuButtonClicked.connect(self.importDictWin)
        fileMenu.addMenu("&Export 📦").menuButtonClicked.connect(self.quickExport)
        fileMenu.addSpacer()
        fileMenu.addMenu("E&xit").menuButtonClicked.connect(TTkHelper.quit)

        extraMenu = topMenuFrame.newMenubarTop().addMenu("E&dit")
        extraMenu.addMenu("&Undo (CTRL+Z)").menuButtonClicked.connect(self.undo)
        extraMenu.addMenu("&Redo (CTRL+Y)").menuButtonClicked.connect(self.redo)
        extraMenu.addSpacer()
        extraMenu.addMenu("&Scratchpad 📝").menuButtonClicked.connect(self.scratchpad)
        extraMenu.addSpacer()
        extraMenu.addMenu("&Preview...").menuButtonClicked.connect(self.preview)

        def _showAbout(btn):
            TTkHelper.overlay(None, About(), 30,10)
        def _showAboutTTk(btn):
            TTkHelper.overlay(None, TTkAbout(), 30,10)

        helpMenu = topMenuFrame.newMenubarTop().addMenu("&Help", alignment=TTkK.RIGHT_ALIGN)
        helpMenu.addMenu("About ...").menuButtonClicked.connect(_showAbout)
        helpMenu.addMenu("About ttk").menuButtonClicked.connect(_showAboutTTk)

        w,_ = self.size()
        mainSplit.setSizes([25,None,42])
        centralSplit.setSizes([None,8])

        self._toolBar.addWidget(btnPreview := TTkButton(maxWidth=12, text='Preview...'))
        self._toolBar.addWidget(btnExport := TTkButton(maxWidth=17, text='Quick Export 📦'))
        self._toolBar.addWidget(btnColors  := TTkButton(maxWidth=11, checkable=True, text=
                            TTkString("▣",TTkColor.fg("#ff0000")) +
                            TTkString("▣",TTkColor.fg("#ffff00")) +
                            TTkString("▣",TTkColor.fg("#00ff00")) +
                            TTkString("▣",TTkColor.fg("#00ffff")) +
                            TTkString("▣",TTkColor.fg("#0000ff")) + "🦄"))

        btnPreview.clicked.connect(self.preview)
        btnExport.clicked.connect(self.quickExport)
        btnColors.toggled.connect(self.toggleColors)

        self._toolBar.addWidget(self._fileNameLabel)

        TTkShortcut(TTkK.CTRL | TTkK.Key_Z).activated.connect(self.undo)
        TTkShortcut(TTkK.CTRL | TTkK.Key_Y).activated.connect(self.redo)
        self._takeSnapshot()

        if fileName:
            self._openFile(fileName)

    # Snapshot Logic:
    #   _snapshots = [ s0 , s1 , s2 , s3 , s4 , s5 , s6 ]
    #   _snapId = 3                   ^
    #
    # Undo:
    #   _snapId-- = 2            ^ = s2
    #   load s2
    #
    # Redo:
    #   _snapId++ = 4                      ^ = s4
    #   load s4
    #
    # Take Snapshot:
    #   Remove the forward Snapshots:
    #   _snapshots = [ s0 , s1 , s2 , s3 ]
    #   Append The new one and update snapId
    #   _snapshots = [ s0 , s1 , s2 , s3 , s4+ ]
    #   _snapId++ = 4

    @pyTTkSlot()
    def _takeSnapshot(self):
        tui = self._windowEditor.dumpDict()
        connections = self._sigslotEditor.dumpDict()
        data = {
            'version':'2.0.0',
            'tui':tui,
            'connections':connections}
        TTkLog.debug(f"{len(pickle.dumps(data))=} {len(self._snapshot)=}")
        if ( self._snapshot and
             0 <= self._snapId < len(self._snapshot) and
             data == self._snapshot[self._snapId]): return
        self._snapshot = self._snapshot[:self._snapId+1]+[data]
        self._snapId = len(self._snapshot)-1

    def _loadSnapshot(self):
        self.weModified.disconnect(self._takeSnapshot)
        data = self._snapshot[self._snapId]
        sw = SuperWidget.loadDict(self, self._windowEditor.viewport(), data['tui'])
        self._windowEditor.importSuperWidget(sw)
        self._sigslotEditor.importConnections(data['connections'])
        self._treeInspector.refresh()
        self.weModified.connect(self._takeSnapshot)

    @pyTTkSlot()
    def undo(self):
        TTkLog.debug(f"Undo: {len(self._snapshot)=}")
        if not self._snapshot: return
        if self._snapId <= 0: return
        self._snapId -= 1
        self._loadSnapshot()

    @pyTTkSlot()
    def redo(self):
        TTkLog.debug(f"Undo: {len(self._snapshot)=}")
        if not self._snapshot: return
        if self._snapId >= len(self._snapshot)-1: return
        self._snapId += 1
        self._loadSnapshot()

    def getWidgets(self):
        widgets = set()
        def _getMenu(menu):
            widgets.add(menu)
            for item in menu._submenu:
                if issubclass(type(item), TTkMenuButton):
                    _getMenu(item)
        def _getItems(layoutItem):
            if layoutItem.layoutItemType() == TTkK.WidgetItem:
                superThing = layoutItem.widget()
                if issubclass(type(superThing), SuperWidget):
                    widgets.add(superThing._wid)
                for c in superThing.layout().children():
                    _getItems(c)
                # Chec and add all the menubuttons
                if issubclass(type(superThing), SuperWidgetFrame):
                    if(_mb := superThing._wid.menuBar(TTkK.TOP)):
                        if(_mbi := _mb._mbItems(TTkK.LEFT_ALIGN)):
                            for _ch in _mbi.children():
                                _getMenu(_ch.widget())
                        if(_mbi := _mb._mbItems(TTkK.CENTER_ALIGN)):
                            for _ch in _mbi.children():
                                _getMenu(_ch.widget())
                        if(_mbi := _mb._mbItems(TTkK.RIGHT_ALIGN)):
                            for _ch in _mbi.children():
                                _getMenu(_ch.widget())
                    if(_mb := superThing._wid.menuBar(TTkK.BOTTOM)):
                        if(_mbi := _mb._mbItems(TTkK.LEFT_ALIGN)):
                            for _ch in _mbi.children():
                                _getMenu(_ch.widget())
                        if(_mbi := _mb._mbItems(TTkK.CENTER_ALIGN)):
                            for _ch in _mbi.children():
                                _getMenu(_ch.widget())
                        if(_mbi := _mb._mbItems(TTkK.RIGHT_ALIGN)):
                            for _ch in _mbi.children():
                                _getMenu(_ch.widget())
        _getItems(self._windowEditor.getTTk().widgetItem())
        return widgets

    @pyTTkSlot(bool)
    def toggleColors(self, state):
        SuperWidget.toggleHighlightLayout.emit(state)

    @pyTTkSlot()
    def quickExport(self):
        tui = self._windowEditor.dumpDict()
        connections = self._sigslotEditor.dumpDict()
        data = {
            'version':'2.0.0',
            'tui':tui,
            'connections':connections}

        win = QuickExport(data)
        TTkHelper.overlay(None, win, 2, 2, modal=True)

    @pyTTkSlot()
    def scratchpad(self):
        win = TTkWindow(
                title="Mr Scratchpad 📝",
                size=(80,30),
                layout=self._notepad,
                flags=TTkK.WindowFlag.WindowMaximizeButtonHint|TTkK.WindowFlag.WindowCloseButtonHint)
        TTkHelper.overlay(None, win, 2, 2, toolWindow=True)

    @pyTTkSlot()
    def preview(self):
        tui = self._windowEditor.dumpDict()
        connections = self._sigslotEditor.dumpDict()
        # for line in jj.split('\n'):
        #     TTkLog.debug(f"{line}")
        newUI = {
            'version':'2.0.0',
            'tui':tui,
            'connections':connections}
        jj =  json.dumps(newUI, indent=1)

        widget = TTkUiLoader.loadJson(jj)
        win = TTkWindow(
                title="Mr Terminal",
                size=(80,30),
                layout=TTkGridLayout(),
                flags=TTkK.WindowFlag.WindowMaximizeButtonHint|TTkK.WindowFlag.WindowCloseButtonHint)
        win.layout().addWidget(widget)
        TTkHelper.overlay(None, win, 2, 2, modal=True)

    @pyTTkSlot()
    def new(self):
        newWindow = TTkUiLoader.loadFile(os.path.join(os.path.dirname(os.path.abspath(__file__)),"../tui/newWindow.tui.json"))
        newWindow.getWidgetByName("BtnWindow"   ).clicked.connect(self._windowEditor.newWindow)
        newWindow.getWidgetByName("BtnContainer").clicked.connect(self._windowEditor.newContainer)
        newWindow.getWidgetByName("BtnFrame"    ).clicked.connect(self._windowEditor.newFrame)
        newWindow.getWidgetByName("BtnResFrame" ).clicked.connect(self._windowEditor.newResFrame)

        newWindow.getWidgetByName("BtnWindow"   ).clicked.connect(self.weModified.emit)
        newWindow.getWidgetByName("BtnContainer").clicked.connect(self.weModified.emit)
        newWindow.getWidgetByName("BtnFrame"    ).clicked.connect(self.weModified.emit)
        newWindow.getWidgetByName("BtnResFrame" ).clicked.connect(self.weModified.emit)
        TTkHelper.overlay(self._windowEditor, newWindow, 10, 4, modal=True)

    @pyTTkSlot()
    def importDictWin(self):
        def _probeCompressedText(_text):
            import re
            ret = ""
            for _t in _text.split('\n'):
                if m := re.match(r'^ *["\']([A-Za-z0-9+/]+[=]{0,2})["\' +]*$',_t):
                    ret += m.group(1)
                elif not re.match(r'^ *$',_t): # exclude empty lines
                    return ""
            return ret
        newWindow = TTkUiLoader.loadFile(os.path.join(os.path.dirname(os.path.abspath(__file__)),"../tui/quickImport.tui.json"))
        te = newWindow.getWidgetByName("TextEdit")
        def _importDict(te=te):
            text = te.toPlainText()
            if compressed := _probeCompressedText(text):
                dd = TTkUtil.base64_deflate_2_obj(compressed)
            else:
                try:
                    dd = eval(text)
                except Exception as e:
                    TTkLog.error(str(e))
                    messageBox = TTkMessageBox(text= str(e),icon=TTkMessageBox.Icon.Warning)
                    TTkHelper.overlay(None, messageBox, 5, 5, True)
                    return

            if type(dd) not in (str,dict):
                messageBox = TTkMessageBox(text= f"Input is {type(dd)}\nImport data must be a dict or \ncompressed String definition",icon=TTkMessageBox.Icon.Warning)
                TTkHelper.overlay(None, messageBox, 5, 5, True)
                return

            dd = TTkUiLoader.normalise(dd)
            sw = SuperWidget.loadDict(self, self._windowEditor.viewport(), dd['tui'])

            self._windowEditor.importSuperWidget(sw)
            self._sigslotEditor.importConnections(dd['connections'])
            self._treeInspector.refresh()
            newWindow.close()

        newWindow.getWidgetByName("BtnDict"   ).clicked.connect(_importDict)
        TTkHelper.overlay(self._windowEditor, newWindow, 10, 4, modal=True)

    def _openFile(self, fileName):
        TTkLog.info(f"Open: {fileName}")
        self._currentPath =  os.path.dirname(os.path.abspath(fileName))
        self._fileName =  os.path.basename(os.path.abspath(fileName))
        self._fileNameLabel.setText(f"( {self._fileName} )")

        with open(fileName) as fp:
            dd = json.load(fp)
            dd = TTkUiLoader.normalise(dd)
            sw = SuperWidget.loadDict(self, self._windowEditor.viewport(), dd['tui'])
            self._windowEditor.importSuperWidget(sw)
            self._sigslotEditor.importConnections(dd['connections'])
            self._treeInspector.refresh()

    @pyTTkSlot()
    def open(self):
        filePicker = TTkFileDialogPicker(pos = (3,3), size=(80,30), caption="Open", path=self._currentPath, fileMode=TTkK.FileMode.ExistingFile ,filter="TTk Tui Files (*.tui.json);;Json Files (*.json);;All Files (*)")
        filePicker.pathPicked.connect(self._openFile)
        TTkHelper.overlay(None, filePicker, 5, 5, True)

    @pyTTkSlot()
    def save(self):
        return self._saveToFile(os.path.join(self._currentPath,self._fileName))

    def _saveToFile(self, fileName):
        TTkLog.info(f"Saving to: {fileName}")

        tui = self._windowEditor.dumpDict()
        connections = self._sigslotEditor.dumpDict()
        newUI = {
            'version':'2.0.0',
            'tui':tui,
            'connections':connections}
        jj =  json.dumps(newUI, indent=1)

        with open(fileName,'w') as fp:
            fp.write(jj)

    @pyTTkSlot()
    def saveAs(self):
        def _approveFile(fileName):
            if os.path.exists(fileName):
                messageBox = TTkMessageBox(
                    text= (
                        TTkString( f'A file named "{os.path.basename(fileName)}" already exists.\nDo you want to replace it?', TTkColor.BOLD) +
                        TTkString( f'\n\nReplacing it will overwrite its contents.') ),
                    icon=TTkMessageBox.Icon.Warning,
                    standardButtons=TTkMessageBox.StandardButton.Discard|TTkMessageBox.StandardButton.Save|TTkMessageBox.StandardButton.Cancel)
                messageBox.buttonSelected.connect(lambda btn : self._saveToFile(fileName) if btn == TTkMessageBox.StandardButton.Save else None)
                TTkHelper.overlay(None, messageBox, 5, 5, True)
            else:
                self._saveToFile(fileName)
        filePicker = TTkFileDialogPicker(pos = (3,3), size=(80,30), acceptMode=TTkK.AcceptMode.AcceptSave, caption="Save As...", path=os.path.join(self._currentPath,self._fileName), fileMode=TTkK.FileMode.AnyFile ,filter="TTk Tui Files (*.tui.json);;Json Files (*.json);;All Files (*)")
        filePicker.pathPicked.connect(_approveFile)
        TTkHelper.overlay(None, filePicker, 5, 5, True)
