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

from TermTk import TTk, TTkK, TTkLog, TTkCfg, TTkColor, TTkTheme, TTkTerm, TTkHelper
from TermTk import TTkString
from TermTk import TTkColorGradient
from TermTk import pyTTkSlot, pyTTkSignal

from TermTk import TTkFrame, TTkButton, TTkLabel
from TermTk import TTkTabWidget
from TermTk import TTkAbstractScrollArea, TTkAbstractScrollView, TTkScrollArea
from TermTk import TTkFileDialogPicker
from TermTk import TTkFileTree, TTkTextEdit

from TermTk import TTkLayout, TTkGridLayout, TTkVBoxLayout, TTkHBoxLayout
from TermTk import TTkSplitter
from TermTk import TTkLogViewer, TTkTomInspector

from TermTk import TTkUiLoader

from .cfg  import *
from .about import *
from .widgetbox import DragDesignItem, WidgetBox, WidgetBoxScrollArea
from .windoweditor import WindowEditor, SuperWidget
from .treeinspector import TreeInspector
from .propertyeditor import PropertyEditor

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
    __slots__ = ('_pippo', '_main', '_windowEditor', '_toolBar')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.addWidget(mainSplit := TTkSplitter())
        mainSplit.addItem(widgetBoxLayout := TTkVBoxLayout())
        #mainSplit.addWidget(TTkButton(text='A',border=True))

        widgetBoxLayout.addWidget(topMenuFrame := TTkFrame(minHeight=1,maxHeight=1,border=False))
        widgetBoxLayout.addWidget(WidgetBoxScrollArea())

        # mainSplit.addWidget(sa := TTkScrollArea())
        # sa.viewport().setLayout(TTkGridLayout())
        # sa.viewport().layout().addWidget(WindowEditor())

        self._main = TTkVBoxLayout()

        self._toolBar = TTkHBoxLayout()

        self._windowEditor = WindowEditor()

        self._main.addItem(self._toolBar)
        self._main.addWidget(self._windowEditor)

        mainSplit.addWidget(centralSplit := TTkSplitter(orientation=TTkK.VERTICAL))
        centralSplit.addWidget(self._main)
        centralSplit.addWidget(TTkLogViewer())

        mainSplit.addWidget(rightSplit := TTkSplitter(orientation=TTkK.VERTICAL))

        rightSplit.addItem(treeInspector := TreeInspector(self._windowEditor.viewport()))
        rightSplit.addItem(propertyEditor := PropertyEditor())
        rightSplit.addWidget(TTkButton(text='E', border=True, maxHeight=3))

        treeInspector.thingSelected.connect(lambda _,s : s.pushSuperControlWidget())
        treeInspector.thingSelected.connect(propertyEditor.setDetail)
        self._windowEditor.viewport().thingSelected.connect(propertyEditor.setDetail)

        self._windowEditor.viewport().weModified.connect(treeInspector.refresh)

        fileMenu = topMenuFrame.menubarTop().addMenu("&File")
        fileMenu.addMenu("Open")
        fileMenu.addMenu("Close")
        fileMenu.addMenu("Exit")

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
        mainSplit.setSizes([5,15,10])
        centralSplit.setSizes([6,4])

        self._toolBar.addWidget(btnPreview := TTkButton(maxWidth=12, text='Preview...'))
        self._toolBar.addWidget(btnColors  := TTkButton(maxWidth=11, checkable=True, text=
                            TTkString("▣",TTkColor.fg("#ff0000")) +
                            TTkString("▣",TTkColor.fg("#ffff00")) +
                            TTkString("▣",TTkColor.fg("#00ff00")) +
                            TTkString("▣",TTkColor.fg("#00ffff")) +
                            TTkString("▣",TTkColor.fg("#0000ff")) + "🦄"))

        btnPreview.clicked.connect(self.preview)
        btnColors.toggled.connect(self.toggleColors)

        self._toolBar.addItem(TTkLayout())

        # # Internal Debug Stuff
        # mainSplit.addWidget(debugSplit := TTkSplitter(orientation=TTkK.VERTICAL))
        # # debugSplit.addWidget(TTkLabel(text='My Own Debug', maxHeight=1, minHeight=1))
        # debugSplit.addWidget(TTkTomInspector())
        # debugSplit.addWidget(TTkLogViewer())

    pyTTkSlot(bool)
    def toggleColors(self, state):
        SuperWidget.toggleHighlightLayout.emit(state)

    def preview(self, btn=None):
        jj = self._windowEditor.getJson()
        for line in jj.split('\n'):
            TTkLog.debug(f"{line}")
        widget = TTkUiLoader.loadJson(jj)
        win = TTkWindow(
                title="Mr Terminal",
                size=(80,30),
                layout=TTkGridLayout(),
                flags=TTkK.WindowFlag.WindowMaximizeButtonHint|TTkK.WindowFlag.WindowCloseButtonHint)
        win.layout().addWidget(widget)
        TTkHelper.overlay(None, win, 2, 2, modal=True)

