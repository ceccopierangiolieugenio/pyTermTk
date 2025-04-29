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
from typing import List,Tuple,Optional,Any

import TermTk as ttk
from TermTk.TTkWidgets.tabwidget import _TTkNewTabWidgetDragData

from .about import About
from .activitybar import TTKodeActivityBar

class TTKodeFileWidgetItem(ttk.TTkTreeWidgetItem):
    __slots__ = ('_path', '_lineNumber')
    def __init__(self, *args, path:str, lineNumber:int=0, **kwargs) -> None:
        self._path = path
        self._lineNumber = lineNumber
        super().__init__(*args, **kwargs)
    def path(self) -> str:
        return self._path
    def lineNumber(self) -> int:
        return self._lineNumber

class _TextDocument(ttk.TextDocumentHighlight):
    __slots__ = ('_filePath', '_tabText',
                 'fileChangedStatus', '_changedStatus', '_savedSnapshot')
    def __init__(self, filePath:str="", tabText:ttk.TTkString=ttk.TTkString(), **kwargs):
        self.fileChangedStatus:ttk.pyTTkSignal = ttk.pyTTkSignal(bool, _TextDocument)
        self._filePath:str = filePath
        self._tabText = tabText
        self._changedStatus:bool = False
        super().__init__(**kwargs)
        self._savedSnapshot = self.snapshootId()
        self.guessLexerFromFilename(filePath)
        self.contentsChanged.connect(self._handleContentChanged)

    def getTabButtonStyle(self) -> dict:
        if self._changedStatus:
            return {'default':{'closeGlyph':' ● '}}
        else:
            return {'default':{'closeGlyph':' □ '}}

    def _handleContentChanged(self) -> None:
        '''A signal is emitted when the file status change, marking it as modified or not'''
        # ttk.TTkLog.debug(f"{self.isUndoAvailable()=} == {self._changedStatus=}")
        curState = self.changed() or self._savedSnapshot != self.snapshootId()
        if self._changedStatus != curState:
            self._changedStatus = not self._changedStatus
            ttk.TTkLog.debug(f"{self.isUndoAvailable()=} == {self._changedStatus=}")
            self.fileChangedStatus.emit(self._changedStatus, self)

    def save(self):
        self._changedStatus = False
        self._savedSnapshot = self.snapshootId()
        self.fileChangedStatus.emit(self._changedStatus, self)
        pass

class _TextEdit(ttk.TTkTextEdit):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cursorPositionChanged.connect(self._positionChanged)


    @ttk.pyTTkSlot(ttk.TTkTextCursor)
    def _positionChanged(self, cursor:ttk.TTkTextCursor):
        extra_selections = []
        # Highlight Red only the  lines under the cursor positions
        cursor = self.textCursor().copy()
        cursor.clearSelection()
        selection = ttk.TTkTextEdit.ExtraSelection(
                                        cursor=cursor,
                                        color=ttk.TTkColor.bg("#333300"),
                                        format=ttk.TTkK.SelectionFormat.FullWidthSelection)
        extra_selections.append(selection)
        self.setExtraSelections(extra_selections)

    def goToLine(self, linenum: int) ->  None:
        w,h = self.size()
        h = min(h, self.document().lineCount())
        tedit:ttk.TTkTextEditView = self
        tedit.textCursor().movePosition(operation=ttk.TTkTextCursor.MoveOperation.End)
        tedit.ensureCursorVisible()
        tedit.textCursor().setPosition(line=linenum-h//3,pos=0)
        tedit.ensureCursorVisible()
        tedit.textCursor().setPosition(line=linenum,pos=0)

class TTKode(ttk.TTkGridLayout):
    __slots__ = ('_kodeTab', '_activityBar')
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        appTemplate = ttk.TTkAppTemplate(border=False)
        self.addWidget(appTemplate)

        self._kodeTab = ttk.TTkKodeTab(border=False, barType=ttk.TTkBarType.NERD_1 ,closable=True)
        self._kodeTab.setDropEventProxy(self._dropEventProxyFile)

        appTemplate.setMenuBar(appMenuBar:=ttk.TTkMenuBarLayout(), ttk.TTkAppTemplate.MAIN)
        fileMenu = appMenuBar.addMenu("&File")
        fileMenu.addMenu("Open").menuButtonClicked.connect(self._showFileDialog)
        fileMenu.addMenu("Close") # .menuButtonClicked.connect(self._closeFile)
        fileMenu.addMenu("Exit").menuButtonClicked.connect(lambda _:ttk.TTkHelper.quit())

        def _showAbout(btn):
            ttk.TTkHelper.overlay(None, About(), 30,10)
        def _showAboutTTk(btn):
            ttk.TTkHelper.overlay(None, ttk.TTkAbout(), 30,10)

        appMenuBar.addMenu("&Quit", alignment=ttk.TTkK.RIGHT_ALIGN).menuButtonClicked.connect(ttk.TTkHelper.quit)
        helpMenu = appMenuBar.addMenu("&Help", alignment=ttk.TTkK.RIGHT_ALIGN)
        helpMenu.addMenu("About ...").menuButtonClicked.connect(_showAbout)
        helpMenu.addMenu("About ttk").menuButtonClicked.connect(_showAboutTTk)

        fileTree = ttk.TTkFileTree(path='.', dragDropMode=ttk.TTkK.DragDropMode.AllowDrag)
        self._activityBar = TTKodeActivityBar()
        self._activityBar.addActivity(name="Explorer", icon=ttk.TTkString("╔██\n╚═╝"), widget=fileTree, select=True)

        appTemplate.setWidget(self._kodeTab, ttk.TTkAppTemplate.MAIN)
        appTemplate.setItem(self._activityBar, ttk.TTkAppTemplate.LEFT, size=30)

        # Define the bottom panel, using the menu feature to add logs and terminal
        bottomLayout = ttk.TTkGridLayout()
        appTemplate.setItem(bottomLayout, ttk.TTkAppTemplate.BOTTOM, size=3)
        appTemplate.setMenuBar(bottomMenuBar:=ttk.TTkMenuBarLayout(), ttk.TTkAppTemplate.BOTTOM)

        bottomLayout.addWidget(_logViewer:=ttk.TTkLogViewer())
        bottomLayout.addWidget(_terminal:=ttk.TTkTerminal(visible=False))
        _th = ttk.TTkTerminalHelper(term=_terminal)
        _th.runShell()
        @ttk.pyTTkSlot(ttk.TTkWidget)
        def _showBottomTab(wid:ttk.TTkWidget):
            _logViewer.hide()
            _terminal.hide()
            wid.show()

        bottomMenuBar.addMenu("Logs", alignment=ttk.TTkK.LEFT_ALIGN).menuButtonClicked.connect(lambda : _showBottomTab(_logViewer))
        bottomMenuBar.addMenu(" Terminal", alignment=ttk.TTkK.LEFT_ALIGN).menuButtonClicked.connect(lambda : _showBottomTab(_terminal))

        fileTree.fileActivated.connect(lambda x: self._openFile(x.path()))
        self._kodeTab.tabAdded.connect(self._tabAdded)

    def _getTabButtonFromWidget(self, widget:ttk.TTkWidget) -> ttk.TTkTabButton:
        for item, tab in self._kodeTab.iterWidgets():
            if item == widget:
                return tab
        return None

    ttk.pyTTkSlot(ttk.TTkTabWidget, int)
    def _tabAdded(self, tw:ttk.TTkTabWidget, index:int):
        tb = tw.tabButton(index)
        wid = tw.widget(index)
        if isinstance(wid,_TextEdit):
            tb.mergeStyle(wid.document().getTabButtonStyle())

    ttk.pyTTkSlot()
    def _showFileDialog(self):
        filePicker = ttk.TTkFileDialogPicker(pos = (3,3), size=(75,24), caption="Pick Something", path=".", fileMode=ttk.TTkK.FileMode.AnyFile ,filter="All Files (*);;Python Files (*.py);;Bash scripts (*.sh);;Markdown Files (*.md)")
        filePicker.pathPicked.connect(self._openFile)
        ttk.TTkHelper.overlay(None, filePicker, 20, 5, True)

    def _getDocument(self, filePath) -> Tuple[_TextDocument, Optional[_TextEdit]]:
        for item, _ in self._kodeTab.iterWidgets():
            if issubclass(type(item), _TextEdit):
                doc = item.document()
                if issubclass(type(doc), _TextDocument):
                    if filePath == doc._filePath:
                        return doc, item
        with open(filePath, 'r') as f:
            content = f.read()
        tabText = ttk.TTkString(ttk.TTkCfg.theme.fileIcon.getIcon(filePath),ttk.TTkCfg.theme.fileIconColor) + ttk.TTkColor.RST + " " + os.path.basename(filePath)
        td = _TextDocument(text=content, filePath=filePath, tabText=tabText)
        td.fileChangedStatus.connect(self._handleFileChangedStatus)
        return td, None

    ttk.pyTTkSlot(bool, _TextDocument)
    def _handleFileChangedStatus(self, status:bool, doc:_TextDocument) -> None:
        # ttk.TTkLog.debug(f"Status ({status}) -> {doc._filePath}")
        for item, tab in self._kodeTab.iterWidgets():
            if issubclass(type(item), _TextEdit):
                if doc == item.document():
                    tab.mergeStyle(doc.getTabButtonStyle())

    def _openFile(self, filePath, line:int=0, pos:int=0):
        filePath = os.path.realpath(filePath)
        doc, tedit = self._getDocument(filePath=filePath)
        if tedit:
            self._kodeTab.setCurrentWidget(tedit)
        else:
            tedit = _TextEdit(document=doc, readOnly=False, lineNumber=True)
            self._kodeTab.addTab(tedit, doc._tabText)
            self._kodeTab.setCurrentWidget(tedit)
        tedit.goToLine(line)
        tedit.setFocus()

    def _dropEventProxyFile(self, evt:ttk.TTkDnDEvent):
        data = evt.data()
        filePath = None

        if ( issubclass(type(data), ttk.TTkTreeWidget._DropTreeData) and data.items ):
            if issubclass(type(data.items[0]), ttk.TTkFileTreeWidgetItem):
                linenum:int = 0
                ftwi:ttk.TTkFileTreeWidgetItem = data.items[0]
                filePath = os.path.realpath(ftwi.path())
            elif issubclass(type(data.items[0]), TTKodeFileWidgetItem):
                kfwi:TTKodeFileWidgetItem = data.items[0]
                linenum:int = kfwi.lineNumber()
                filePath = os.path.realpath(kfwi.path())

        if filePath:
            doc, _ = self._getDocument(filePath=filePath)
            tedit = _TextEdit(document=doc, readOnly=False, lineNumber=True)
            tedit.goToLine(linenum)
            newData = _TTkNewTabWidgetDragData(
                widget=tedit,
                label=doc._tabText,
                data=None,
                closable=True
            )
            newEvt = evt.clone()
            newEvt.setData(newData)
            return newEvt
        return evt
