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

from TermTk import TTkGridLayout, TTkVBoxLayout
from TermTk import TTkSplitter
from TermTk import TTkLogViewer, TTkTomInspector

from .cfg  import *
from .about import *
from .widgetbox import DragDesignItem, WidgetBox, WidgetBoxScrollArea
from .windoweditor import WindowEditor
from .treeinspector import TreeInspector
from .propertyeditor import PropertyEditor

#
#      Mimic the QT Designer layout
#
#      ┌─────────────────────╥───────────────────────────────╥───────────────────┐
#      │                     ║                               ║                   │
#      │                     ║                               ║  Tree Inspector   │
#      │                     ║                               ║                   │
#      │                     ║                               ║                   │
#      │   Widget            ║                               ║                   │
#      │   Box               ║                               ╠═══════════════════╡
#      │                     ║       Main Window             ║                   │
#      │                     ║       Editor                  ║   Property        │
#      │                     ║                               ║   Editor          │
#      │                     ║                               ║                   │
#      │                     ║                               ║                   │
#      │                     ║                               ║                   │
#      │                     ║                               ║                   │
#      │                     ║                               ╠═══════════════════╡
#      │                     ║                               ║                   │
#      │                     ║                               ║   Signal/Slot     │
#      │                     ╟───────────────────────────────╢                   │
#      │                     ║     LOG Viewer                ║   Editor          │
#      │                     ║                               ║                   │
#      └─────────────────────╨───────────────────────────────╨───────────────────┘
#

class TTkDesigner(TTkGridLayout):
    __slots__ = ('_pippo', '_windowEditor')
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

        self._windowEditor = WindowEditor()

        mainSplit.addWidget(centralSplit := TTkSplitter(orientation=TTkK.VERTICAL))
        centralSplit.addWidget(self._windowEditor)
        centralSplit.addWidget(TTkLogViewer())

        mainSplit.addWidget(rightSplit := TTkSplitter(orientation=TTkK.VERTICAL))

        rightSplit.addItem(ti := TreeInspector(self._windowEditor.viewport()))
        rightSplit.addItem(pe := PropertyEditor())
        rightSplit.addWidget(be := TTkButton(text='E', border=True, maxHeight=3))

        ti.widgetSelected.connect(lambda _,s : s.pushSuperControlWidget())
        ti.widgetSelected.connect(pe.setDetail)
        self._windowEditor.viewport().widgetSelected.connect(pe.setDetail)

        self._windowEditor.viewport().weModified.connect(ti.refresh)

        fileMenu = topMenuFrame.menubarTop().addMenu("&File")
        fileMenu.addMenu("Open")
        fileMenu.addMenu("Close")
        fileMenu.addMenu("Exit")

        fileMenu = topMenuFrame.menubarTop().addMenu("F&orm")
        fileMenu.addMenu("Preview...").menuButtonClicked.connect(self.preview)
        be.clicked.connect(self.preview)

        def _showAbout(btn):
            TTkHelper.overlay(None, About(), 30,10)
        def _showAboutTTk(btn):
            TTkHelper.overlay(None, TTkAbout(), 30,10)

        helpMenu = topMenuFrame.menubarTop().addMenu("&Help", alignment=TTkK.RIGHT_ALIGN)
        helpMenu.addMenu("About ...").menuButtonClicked.connect(_showAbout)
        helpMenu.addMenu("About ttk").menuButtonClicked.connect(_showAboutTTk)

        w,_ = self.size()
        mainSplit.setSizes([5,15,10])
        centralSplit.setSizes([8,2])

        # # Internal Debug Stuff
        # mainSplit.addWidget(debugSplit := TTkSplitter(orientation=TTkK.VERTICAL))
        # # debugSplit.addWidget(TTkLabel(text='My Own Debug', maxHeight=1, minHeight=1))
        # debugSplit.addWidget(TTkTomInspector())
        # debugSplit.addWidget(TTkLogViewer())

    def preview(self, btn=None):
        for line in self._windowEditor.getYaml().split('\n'):
            TTkLog.debug(f"{line}")
