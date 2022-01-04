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

import os
import datetime

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.cfg import TTkCfg
from TermTk.TTkCore.string import TTkString
from TermTk.TTkWidgets.window import TTkWindow
from TermTk.TTkWidgets.tree import TTkTree
from TermTk.TTkWidgets.treewidgetitem import TTkTreeWidgetItem
from TermTk.TTkWidgets.splitter import TTkSplitter
from TermTk.TTkWidgets.frame import TTkFrame
from TermTk.TTkWidgets.combobox import TTkComboBox
from TermTk.TTkWidgets.button import TTkButton
from TermTk.TTkWidgets.label import TTkLabel
from TermTk.TTkWidgets.list_ import TTkList
from TermTk.TTkLayouts.gridlayout import TTkGridLayout
from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal


'''
::

    +----------------------------------------+
    |  Look in: [--FULL-PATH-|v] [<] [>] [^] |
    | +-----------+------------------------+ |
    | | Bookmarks ║     File Tree          | |
    | |           ║                        | |
    | +-----------+------------------------+ |
    | File name:     [-----------]  [Open  ] |
    | Files of Type  [-----------]  [Cancel] |
    +--------------+-------------------------+
'''

class _FileTreeWidgetItem(TTkTreeWidgetItem):
    FILE = 0x00
    DIR  = 0x01

    __slots__ = ('_path', '_type')
    def __init__(self, *args, **kwargs):
        TTkTreeWidgetItem.__init__(self, *args, **kwargs)
        self._path = kwargs.get('path', '.')
        self._type = kwargs.get('type', _FileTreeWidgetItem.FILE)
        self.setTextAlignment(1, TTkK.RIGHT_ALIGN)

    def getPath(self):
        return self._path

    def getType(self):
        return self._type

class TTkFileDialogPicker(TTkWindow):
    __slots__ = ('_path', '_filter', '_caption',
                 #Signals
                 'filePicked')

    def __init__(self, *args, **kwargs):
        # Signals
        self.filePicked = pyTTkSignal(str)

        TTkWindow.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'TTkFileDialogPicker' )

        self._path    = kwargs.get('path','.')
        self._filter  = kwargs.get('filter','All Files (*)')
        self._caption = kwargs.get('caption','File Dialog')

        self.setTitle(self._caption)
        self.setLayout(TTkGridLayout())

        # Top (absPath)
        topLayout = TTkGridLayout()
        self.layout().addItem(topLayout,0,0)

        topLayout.addWidget(TTkLabel(text="Look in:",maxWidth=14),      0,0)
        topLayout.addWidget(lookPath := TTkComboBox(list=TTkFileDialogPicker._getListLook(self._path)),       0,1)
        topLayout.addWidget(btnPrev  := TTkButton(text="<",maxWidth=3), 0,2)
        topLayout.addWidget(btnNext  := TTkButton(text=">",maxWidth=3), 0,3)
        topLayout.addWidget(btnUp    := TTkButton(text="^",maxWidth=3), 0,4)

        # Bottom (File Name, Controls)
        bottomLayout = TTkGridLayout()
        self.layout().addItem(bottomLayout,2,0)
        bottomLayout.addWidget(TTkLabel(text="File name:"     ,maxWidth=14),      0,0)
        bottomLayout.addWidget(TTkLabel(text="Files of type:" ,maxWidth=14),      1,0)
        bottomLayout.addWidget(lookPath := TTkComboBox(),       0,1)
        bottomLayout.addWidget(lookPath := TTkComboBox(),       1,1)
        bottomLayout.addWidget(btnOpen   := TTkButton(text="Open",  maxWidth=8), 0,2)
        bottomLayout.addWidget(btnCancel := TTkButton(text="Cancel",maxWidth=8), 1,2)

        # Center (FileTree, Bookmarks)
        splitter = TTkSplitter(border=True)
        self.layout().addWidget(splitter,1,0)

        bookmarks = TTkList(parent=splitter)

        fileTree = TTkTree(parent=splitter)
        fileTree.setHeaderLabels(["Name", "Size", "Type", "Date Modified"])
        fileTree.itemExpanded.connect(TTkFileDialogPicker._updateChildren)
        fileTree.itemExpanded.connect(TTkFileDialogPicker._folderExpanded)
        fileTree.itemCollapsed.connect(TTkFileDialogPicker._folderCollapsed)

        for i in TTkFileDialogPicker._getFileItems(self._path):
            fileTree.addTopLevelItem(i)

    @staticmethod
    def _getListLook(path):
        path = os.path.abspath(path)
        ret = [path]
        while True:
            path, e = os.path.split(path)
            if e:
                ret.append(path)
            if not path or path=='/':
                break
        return ret

    @staticmethod
    def _getFileItems(path):
        path = os.path.abspath(path)
        dir_list = os.listdir(path)
        ret = []
        for n in dir_list:
            nodePath = os.path.join(path,n)
            info = os.stat(nodePath)
            time = datetime.datetime.fromtimestamp(info.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
            if info.st_size > (1024*1024*1024):
                size = f"{info.st_size/(1024*1024*1024):.2f} GB"
            if info.st_size > (1024*1024):
                size = f"{info.st_size/(1024*1024):.2f} MB"
            elif info.st_size > 1024:
                size = f"{info.st_size/1024:.2f} KB"
            else:
                size = f"{info.st_size} bytes"

            description = [ n, info.st_size, ]
            if os.path.isdir(nodePath):
                ret.append(_FileTreeWidgetItem(
                                [ TTkString()+TTkCfg.theme.folderNameColor+n+'/', "",   "Folder",  time],
                                path=nodePath,
                                type=_FileTreeWidgetItem.DIR,
                                icon=TTkCfg.theme.folderIconClose,
                                childIndicatorPolicy=TTkK.ShowIndicator))
            elif os.path.isfile(nodePath):
                _, ext = os.path.splitext(n)
                if ext: ext = f"{ext[1:]} "
                ret.append(_FileTreeWidgetItem(
                                [ TTkString()+TTkCfg.theme.fileNameColor+n, size, f"{ext}File", time],
                                path=nodePath,
                                type=_FileTreeWidgetItem.FILE,
                                icon=TTkCfg.theme.getFileIcon(n),
                                childIndicatorPolicy=TTkK.DontShowIndicator))
            elif os.path.islink(nodePath):
                pass
            elif os.path.ismount(nodePath):
                pass
        return ret

    @staticmethod
    def _folderExpanded(item):
        item.setIcon(0, TTkCfg.theme.folderIconOpen)

    @staticmethod
    def _folderCollapsed(item):
        item.setIcon(0, TTkCfg.theme.folderIconClose)

    @staticmethod
    def _updateChildren(item):
        if item.children(): return
        for i in TTkFileDialogPicker._getFileItems(item.getPath()):
            item.addChild(i)


'''
for (dirpath, dirnames, filenames) in walk('/tmp'):
    print(f"{dirpath} {dirnames} {filenames}")
    break
'''

class TTkFileDialog:
    def getOpenFileName(caption, dir=".", filter="All Files (*)", options=None):
        pass