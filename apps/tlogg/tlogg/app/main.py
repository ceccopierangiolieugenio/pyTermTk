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

import os
import re
import sys
import argparse

import appdirs

from TermTk import *

from tlogg import TloggHelper, tloggProxy

from .cfg  import *
from .glbl import *
from .about import *
from .loggwidget import LoggWidget
from .options import optionsFormLayout, optionsLoadTheme
from .highlighters import highlightersFormLayout
from .predefinedfilters import PredefinedFiltersFormWindow
from .notepad import NotePad


class TLOGG(TTkGridLayout):
    '''
        ┌──────────────────[Main Splitter]─────────┐
        │┌──────────╥────[File Tab Splitter]──────┐│
        ││ F.Tree   ║       Tab                   ││
        ││ Controls ╟─────────────────────────────┤│
        │├──────────╢┌───────────────────────────┐││
        ││ File     ║│   File Viewer             │││
        ││ Tree     ║│                           │││
        ││          ║╞═══════════════════════════╡││
        ││          ║│   Search Widget           │││
        ││          ║│                           │││
        ││          ║└───────────────────────────┘││
        │└──────────╨─────────────────────────────┘│
        ╞══════════════════════════════════════════╡
        │ Logger,Debug View                        │
        └──────────────────────────────────────────┘
    '''
    __slots__ = ('_kodeTab', '_tloggProxy','_notepad')
    def __init__(self, tloggProxy, *args, **kwargs) -> None:
        self._tloggProxy = tloggProxy
        self._notepad = NotePad()

        super().__init__(*args, **kwargs)

        self._tloggProxy.setOpenFile(self.openFile)

        self.addWidget(appTemplate:=TTkAppTemplate(border=False))

        self._kodeTab = TTkKodeTab(border=False, closable=True)

        appTemplate.setMenuBar(appMenuBar:=TTkMenuBarLayout(), TTkAppTemplate.LEFT)
        fileMenu      = appMenuBar.addMenu("&File")
        buttonOpen    = fileMenu.addMenu("&Open")
        buttonClose   = fileMenu.addMenu("&Close")
        fileMenu.addSpacer()
        buttonColors  = fileMenu.addMenu("C&olors...")
        buttonFilters = fileMenu.addMenu("&Filters...")
        buttonOptions = fileMenu.addMenu("O&ptions...")
        fileMenu.addSpacer()
        buttonExit    = fileMenu.addMenu("E&xit")
        buttonExit.menuButtonClicked.connect(TTkHelper.quit)

        extraMenu = appMenuBar.addMenu("E&xtra")
        extraMenu.addMenu("Scratchpad").menuButtonClicked.connect(self.scratchpad)
        extraMenu.addSpacer()

        helpMenu = appMenuBar.addMenu("&Help", alignment=TTkK.RIGHT_ALIGN)
        helpMenu.addMenu("About ...").menuButtonClicked.connect(self.showAbout)
        helpMenu.addMenu("About tlogg").menuButtonClicked.connect(self.showAboutTlogg)

        def _tabChanged(_,__,widget,data):
            tloggProxy.tloggFocussed.emit(None, data)

        self._kodeTab.currentChanged.connect(_tabChanged)
        self._kodeTab.kodeTabCloseRequested.connect(self._handleTabCloseRequested)

        # fileTree.fileActivated.connect(lambda x: self.openFile(x.path()))

        buttonOpen.menuButtonClicked.connect(self.openFileCallback)
        buttonColors.menuButtonClicked.connect(self.showColors)
        buttonFilters.menuButtonClicked.connect(self.showFilters)
        buttonOptions.menuButtonClicked.connect(self.showOptions )

        for mod in TloggHelper._getPlugins():
            if mod.position:
                appTemplate.setWidget(mod.widget, mod.position, 30)
                if mod.menu:
                    _menu = extraMenu.addMenu(mod.name, checkable=True, checked=mod.visible)
                    mod.widget.setVisible(mod.visible)
                    _menu.toggled.connect(mod.widget.setVisible)


        appTemplate.setWidget(self._kodeTab, TTkAppTemplate.MAIN)
        appTemplate.setWidget(TTkLogViewer(),TTkAppTemplate.BOTTOM,size=1,title="Logs")

    @ttk.pyTTkSlot(TTkTabWidget, int)
    def _handleTabCloseRequested(self, tab:TTkTabWidget, num:int):
        tab.removeTab(num)

    @pyTTkSlot()
    def scratchpad(self):
        win = TTkWindow(
                title="Mr Scratchpad",
                size=(80,30),
                layout=self._notepad,
                flags=TTkK.WindowFlag.WindowMaximizeButtonHint|TTkK.WindowFlag.WindowCloseButtonHint)
        TTkHelper.overlay(None, win, 2, 2, toolWindow=True)

    @pyTTkSlot(TTkMenuButton)
    def openFileCallback(self, btn):
        filePicker = TTkFileDialogPicker(
                        pos = (3,3), size=(90,30),
                        caption="Open a File", path=".",
                        filter="All Files (*);;Text Files (*.txt);;Log Files (*.log)")
        filePicker.filePicked.connect(self.openFile)
        TTkHelper.overlay(btn, filePicker, 10, 2, modal=True)

    @pyTTkSlot(TTkMenuButton)
    def showColors(self, btn):
        win = TTkWindow(title="Highlighters...", size=(70,20), border=True)
        win.setLayout(highlightersFormLayout(win))
        TTkHelper.overlay(btn, win, 10,2, modal=True)

    @pyTTkSlot(TTkMenuButton)
    def showFilters(self, btn):
        win = PredefinedFiltersFormWindow(title="Predefined Filters...", size=(70,20), border=True)
        TTkHelper.overlay(btn, win, 10,2, modal=True)

    @pyTTkSlot(TTkMenuButton)
    def showOptions(self, btn):
        win = TTkWindow(title="Options...", size=(70,20), border=True)
        win.setLayout(optionsFormLayout(win))
        TTkHelper.overlay(btn, win, 10,2, modal=True)

        # tab.addTab(h
        #   @pyTTkSlot()ighlightersForm(), "-Setup-")
    @pyTTkSlot(TTkMenuButton)
    def showAbout(self, btn):
        TTkHelper.overlay(btn, TTkAbout(), 20,5)

    @pyTTkSlot(TTkMenuButton)
    def showAboutTlogg(self, btn):
        TTkHelper.overlay(btn, About(), 20,5)

    def openFile(self, file):
        # openedFiles.append(file)
        loggWidget = LoggWidget(file)
        self._kodeTab.addTab(widget=loggWidget, label=os.path.basename(file), data=file)
        self._kodeTab.setCurrentWidget(loggWidget)
