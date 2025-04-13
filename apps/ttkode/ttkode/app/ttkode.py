#!/usr/bin/env python3

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

__all__ = ['TTKode']

import os

from TermTk import TTkK, TTkLog, TTkCfg, TTkColor, TTkTheme, TTkTerm, TTkHelper
from TermTk import TTkString
from TermTk import pyTTkSlot, pyTTkSignal

from TermTk import TTkFrame, TTkButton
from TermTk import TTkKodeTab
from TermTk import TTkFileDialogPicker
from TermTk import TTkFileTree, TTkTextEdit, TTkTextCursor

from TermTk import TTkGridLayout
from TermTk import TTkSplitter,TTkAppTemplate
from TermTk import TextDocumentHighlight
from TermTk import TTkLogViewer
from TermTk import TTkMenuBarLayout
from TermTk import TTkAbout
from TermTk import TTkTestWidget, TTkTestWidgetSizes
from TermTk import TTkDnDEvent
from TermTk import TTkTreeWidget, TTkFileTreeWidget, TTkFileTreeWidgetItem
from TermTk.TTkWidgets.tabwidget import _TTkNewTabWidgetDragData

from .about import About
from .activitybar import TTKodeActivityBar

class _TextDocument(TextDocumentHighlight):
    __slots__ = ('_filePath')
    def __init__(self, filePath:str="", **kwargs):
        self._filePath = filePath
        super().__init__(**kwargs)
        self.guessLexerFromFilename(filePath)

class TTKode(TTkGridLayout):
    __slots__ = ('_kodeTab', '_documents', '_activityBar')
    def __init__(self, *, files, **kwargs):
        self._documents = {}

        super().__init__(**kwargs)

        appTemplate = TTkAppTemplate(border=False)
        self.addWidget(appTemplate)

        self._kodeTab = TTkKodeTab(border=False, closable=True)
        self._kodeTab.setDropEventProxy(self._dropEventProxyFile)

        appTemplate.setMenuBar(appMenuBar:=TTkMenuBarLayout(), TTkAppTemplate.MAIN)
        fileMenu = appMenuBar.addMenu("&File")
        fileMenu.addMenu("Open").menuButtonClicked.connect(self._showFileDialog)
        fileMenu.addMenu("Close") # .menuButtonClicked.connect(self._closeFile)
        fileMenu.addMenu("Exit").menuButtonClicked.connect(lambda _:TTkHelper.quit())

        def _showAbout(btn):
            TTkHelper.overlay(None, About(), 30,10)
        def _showAboutTTk(btn):
            TTkHelper.overlay(None, TTkAbout(), 30,10)

        appMenuBar.addMenu("&Quit", alignment=TTkK.RIGHT_ALIGN).menuButtonClicked.connect(TTkHelper.quit)
        helpMenu = appMenuBar.addMenu("&Help", alignment=TTkK.RIGHT_ALIGN)
        helpMenu.addMenu("About ...").menuButtonClicked.connect(_showAbout)
        helpMenu.addMenu("About ttk").menuButtonClicked.connect(_showAboutTTk)

        fileTree = TTkFileTree(path='.', dragDropMode=TTkK.DragDropMode.AllowDrag)
        self._activityBar = TTKodeActivityBar()
        self._activityBar.addActivity(name="Explorer", icon=TTkString("╔██\n╚═╝"), widget=fileTree, select=True)

        appTemplate.setWidget(self._kodeTab, TTkAppTemplate.MAIN)
        appTemplate.setItem(self._activityBar, TTkAppTemplate.LEFT, size=30)
        appTemplate.setWidget(TTkLogViewer(), TTkAppTemplate.BOTTOM, title="Logs", size=3)

        for file in files:
            self._openFile(file)

        fileTree.fileActivated.connect(lambda x: self._openFile(x.path()))

    pyTTkSlot()
    def _showFileDialog(self):
        filePicker = TTkFileDialogPicker(pos = (3,3), size=(75,24), caption="Pick Something", path=".", fileMode=TTkK.FileMode.AnyFile ,filter="All Files (*);;Python Files (*.py);;Bash scripts (*.sh);;Markdown Files (*.md)")
        filePicker.pathPicked.connect(self._openFile)
        TTkHelper.overlay(None, filePicker, 20, 5, True)

    def _openFile(self, filePath, lineNumber=0):
        filePath = os.path.realpath(filePath)
        if filePath in self._documents:
            doc = self._documents[filePath]['doc']
        else:
            with open(filePath, 'r') as f:
                content = f.read()
            doc = _TextDocument(text=content, filePath=filePath)
            self._documents[filePath] = {'doc':doc,'tabs':[]}
        tedit = TTkTextEdit(document=doc, readOnly=False, lineNumber=True)
        label = TTkString(TTkCfg.theme.fileIcon.getIcon(filePath),TTkCfg.theme.fileIconColor) + TTkColor.RST + " " + os.path.basename(filePath)

        self._kodeTab.addTab(tedit, label)
        self._kodeTab.setCurrentWidget(tedit)

        if lineNumber:
            tedit.textCursor().movePosition(operation=TTkTextCursor.MoveOperation.End)
            tedit.ensureCursorVisible()
            tedit.textCursor().setPosition(line=lineNumber,pos=0)
            tedit.ensureCursorVisible()
            newCursor = tedit.textCursor().copy()
            newCursor.clearSelection()
            selection = TTkTextEdit.ExtraSelection(
                                            cursor=newCursor,
                                            color=TTkColor.bg("#444400"),
                                            format=TTkK.SelectionFormat.FullWidthSelection)
            tedit.setExtraSelections([selection])
        tedit.setFocus()

    def _dropEventProxyFile(self, evt:TTkDnDEvent):
        data = evt.data()
        if ( issubclass(type(data), TTkTreeWidget._DropTreeData) and
            data.items and
            issubclass(type(data.items[0]), TTkFileTreeWidgetItem)):
            item:TTkFileTreeWidgetItem = data.items[0]
            filePath = os.path.realpath(item.path())
            if filePath in self._documents:
                doc = self._documents[filePath]['doc']
            else:
                with open(filePath, 'r') as f:
                    content = f.read()
                doc = _TextDocument(text=content, filePath=filePath)
                self._documents[filePath] = {'doc':doc,'tabs':[]}
            tedit = TTkTextEdit(document=doc, readOnly=False, lineNumber=True)
            label = TTkString(TTkCfg.theme.fileIcon.getIcon(filePath),TTkCfg.theme.fileIconColor) + TTkColor.RST + " " + os.path.basename(filePath)

            newData = _TTkNewTabWidgetDragData(
                widget=tedit,
                label=label,
                data=None,
                closable=True
            )
            newEvt = evt.clone()
            newEvt.setData(newData)
            return newEvt
        return evt
        # def _closeFile():
        #     if (index := KodeTab.lastUsed.currentIndex()) >= 0:
        #         KodeTab.lastUsed.removeTab(index)
