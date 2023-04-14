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

from TermTk import TTk, TTkK, TTkLog, TTkCfg, TTkColor, TTkTheme, TTkTerm, TTkHelper
from TermTk import TTkString
from TermTk import TTkColorGradient
from TermTk import pyTTkSlot, pyTTkSignal

from TermTk import TTkWidget, TTkFrame, TTkButton, TTkLabel
from TermTk import TTkTabWidget
from TermTk import TTkAbstractScrollArea, TTkAbstractScrollView, TTkScrollArea
from TermTk import TTkFileDialogPicker, TTkMessageBox
from TermTk import TTkFileTree, TTkTextEdit

from TermTk import TTkLayout, TTkGridLayout, TTkVBoxLayout, TTkHBoxLayout
from TermTk import TTkSplitter
from TermTk import TTkLogViewer, TTkTomInspector

from TermTk import TTkUiLoader, TTkUtil

from .cfg  import *
from .about import *
from .widgetbox import DragDesignItem, WidgetBox, WidgetBoxScrollArea
from .windoweditor import WindowEditor, SuperWidget
from .treeinspector import TreeInspector
from .propertyeditor import PropertyEditor
from .signalsloteditor import SignalSlotEditor
from .quickexport import QuickExport

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
    __slots__ = ('_pippo', '_main', '_windowEditor', '_toolBar', '_sigslotEditor', '_treeInspector',
                 # Signals
                 'weModified', 'thingSelected', 'widgetNameChanged'
                 )
    def __init__(self, *args, **kwargs):
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

        self._main = TTkVBoxLayout()
        self._toolBar = TTkHBoxLayout()
        self._windowEditor = WindowEditor(self)
        self._sigslotEditor = SignalSlotEditor(self)
        self._treeInspector = TreeInspector(self, self._windowEditor.viewport())

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
        rightSplit.addItem(propertyEditor := PropertyEditor())
        # rightSplit.addItem(self._sigslotEditor)

        self.thingSelected.connect(lambda _,s : s.pushSuperControlWidget())
        self.thingSelected.connect(propertyEditor.setDetail)

        self.weModified.connect(self._treeInspector.refresh)

        fileMenu = topMenuFrame.menubarTop().addMenu("&File")
        fileMenu.addMenu("New").menuButtonClicked.connect(self.new)
        fileMenu.addMenu("Open").menuButtonClicked.connect(self.open)
        fileMenu.addMenu("Save").menuButtonClicked.connect(self.save)
        fileMenu.addMenu("Save As...").menuButtonClicked.connect(self.saveAs)
        fileMenu.addMenu("Exit").menuButtonClicked.connect(TTkHelper.quit)

        fileMenu = topMenuFrame.menubarTop().addMenu("F&orm")
        fileMenu.addMenu("Preview...").menuButtonClicked.connect(self.preview)

        def _showAbout(btn):
            TTkHelper.overlay(None, About(), 30,10)
        def _showAboutTTk(btn):
            TTkHelper.overlay(None, TTkAbout(), 30,10)

        helpMenu = topMenuFrame.menubarTop().addMenu("&Help", alignment=TTkK.RIGHT_ALIGN)
        helpMenu.addMenu("About ...").menuButtonClicked.connect(_showAbout)
        helpMenu.addMenu("About ttk").menuButtonClicked.connect(_showAboutTTk)

        w,_ = self.size()
        mainSplit.setSizes([25,None,40])
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

        self._toolBar.addItem(TTkLayout())

    def getWidgets(self):
        widgets = []
        def _getItems(layoutItem):
            if layoutItem.layoutItemType == TTkK.WidgetItem:
                superThing = layoutItem.widget()
                if issubclass(type(superThing), SuperWidget):
                    widgets.append(superThing._wid)
                for c in superThing.layout().children():
                    _getItems(c)
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
            'version':'1.0.0',
            'tui':tui,
            'connections':connections}

        win = QuickExport(
                data=data,
                title="Mr Export", size=(80,30),
                flags=TTkK.WindowFlag.WindowMaximizeButtonHint|TTkK.WindowFlag.WindowCloseButtonHint)
        TTkHelper.overlay(None, win, 2, 2, modal=True)

    @pyTTkSlot()
    def preview(self):
        tui = self._windowEditor.dumpDict()
        connections = self._sigslotEditor.dumpDict()
        # for line in jj.split('\n'):
        #     TTkLog.debug(f"{line}")
        newUI = {
            'version':'1.0.0',
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
        newWindow = TTkUiLoader.loadDict(TTkUtil.base64_deflate_2_obj(
            "eJytlm1L21AUxxOTmtau0zmmm75YGIP1xSzVzU3pq1WnskwRVnQgfRGbS28wTSQPs24IslctXMaEWzYGQ9hH6yfYR9i5eahpS2tx5oHc03Pvye9/z7m5PRdbX1Ocf5zR" +
            "LJE+IdvRLZOSxGIun8tTIrieTpkrUTFUx6EkVSod7eumZp1QMn6s2mrN8f3ijlpD4N5BJ5E7uWs5usvClWlWEZUxRMQP+mfkm+vKNCKpbd2U93XNxVQZIxPM2kJ6FbtU" +
            "EcGp1kPnNjcFXjBDL7OlXVXTdLPqRxMUnp2IjL9XTy3PpSQDnJu2rkW2tKc7+qGBaINIb00VWhprlizLKOnHlIjzB/kaSCpatoZscCVKugvdSZY52A3K5A3LrskLMsSW" +
            "15GjV01ky38vf34LBt8JlMsbhlp1APLcI+NG8H6YIpzAM1g6g3nZRFYNufYpgHNwFpW7LnVIsoJ1Q7ORP11+f3+yi57rwhSykVmcIqmia4aacJpJnwHZOBO0RIQnlSSe" +
            "UgR87x3H8RyeDh73y+G74ET4gR84ijLbwA+b+BGeI2IJ1WGqpiPFQQ9fG55vkNQaRpUjNnW0SSTfgElsevhxoG6BMeInwYsABkThp2XqEcGGcoAECxXLYE8JbOdYNanC" +
            "Ewl+C9teEOZZXGpYS4HU5zGpGSZ1EqRKw6UCFRPYYAJx7uMcz3GRvHaLtlvfr7t+TLRbF3KY2XBo4cVKYamwtLzs3/nCS2bm4QSzdtDXabWvT32UQOUr0AuAuGzT82uu" +
            "1h8f9uoIRv4aQebvKM0438SLA5OaiZKKXylj+DUU2ooi4tVBydOqKKpTrjd5I9Rpd/KuCjMIfDNifhBxBohjX4xodSU61AKjzoxM3QypZyNqFlzuXlPD0YUYugDoY4DO" +
            "D0LfK1r1HvTkraGz4DdGF69D3+pHT98a+tb/oCf60UnS/3YeIqPzTU77Zk+1cx0FPFMwAQr4jgJoDi/1mfiuEyt3klizDMvu7FepNwbsQjVksi1zkCI+pogPl0A8GXa3" +
            "kJ5UDBUyyrLt0hLPxGmoAn8Znb23kOzeJHTtF7fLHgS/ObvQYUeeR9IVyzRRhf1BcmDL93L/AD7YB1I="))

        newWindow.getWidgetByName("BtnWindow").clicked.connect(newWindow.close)
        newWindow.getWidgetByName("BtnWidget").clicked.connect(newWindow.close)
        newWindow.getWidgetByName("BtnWindow").clicked.connect(self._windowEditor.newWindow)
        newWindow.getWidgetByName("BtnWidget").clicked.connect(self._windowEditor.newWidget)
        newWindow.getWidgetByName("BtnWindow").clicked.connect(self.weModified.emit)
        newWindow.getWidgetByName("BtnWidget").clicked.connect(self.weModified.emit)

        TTkHelper.overlay(self._windowEditor, newWindow, 10, 4, modal=True)

    def _openFile(self, fileName):
        TTkLog.info(f"Open: {fileName}")
        with open(fileName) as fp:
            dd = json.load(fp)
            sw = SuperWidget.loadDict(self, self._windowEditor.viewport(), dd['tui'])
            self._windowEditor.importSuperWidget(sw)
            self._sigslotEditor.importConnections(dd['connections'])
            self._treeInspector.refresh()

    @pyTTkSlot()
    def open(self):
        # self._openFile('tmp/pippo.008.json')
        # return
        filePicker = TTkFileDialogPicker(pos = (3,3), size=(75,24), caption="Open", path="experiments", fileMode=TTkK.FileMode.AnyFile ,filter="Json Files (*.json);;All Files (*)")
        filePicker.pathPicked.connect(self._openFile)
        TTkHelper.overlay(None, filePicker, 5, 5, True)

    @pyTTkSlot()
    def save(self):
        return self.saveAs()

    def _saveToFile(self, fileName):
        TTkLog.info(f"Saving to: {fileName}")

        tui = self._windowEditor.dumpDict()
        connections = self._sigslotEditor.dumpDict()
        newUI = {
            'version':'1.0.0',
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
                    title='Title',
                    text= (
                        TTkString( f'A file named "{os.path.basename(fileName)}" already exists.\nDo you want to replace it?', TTkColor.BOLD) +
                        TTkString( f'\n\nReplacing it will overwrite its contents.') ),
                    icon=TTkMessageBox.Icon.Warning,
                    standardButtons=TTkMessageBox.StandardButton.Discard|TTkMessageBox.StandardButton.Save|TTkMessageBox.StandardButton.Cancel)
                messageBox.buttonSelected.connect(lambda btn : self._saveToFile(fileName) if btn == TTkMessageBox.StandardButton.Save else None)
                TTkHelper.overlay(None, messageBox, 5, 5, True)
            else:
                self._saveToFile(fileName)
        filePicker = TTkFileDialogPicker(pos = (3,3), size=(75,24), caption="Save As...", path="experiments", fileMode=TTkK.FileMode.AnyFile ,filter="All Files (*);;Python Files (*.json)")
        filePicker.pathPicked.connect(_approveFile)
        TTkHelper.overlay(None, filePicker, 5, 5, True)
