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
from TermTk.TTkWidgets.window import TTkWindow
from TermTk.TTkWidgets.tree import TTkTree
from TermTk.TTkWidgets.treewidgetitem import TTkTreeWidgetItem
from TermTk.TTkLayouts.gridlayout import TTkGridLayout
from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal

class _FileTreeWidgetItem(TTkTreeWidgetItem):
    __slots__ = ('_path')
    def __init__(self, *args, **kwargs):
        TTkTreeWidgetItem.__init__(self, *args, **kwargs)
        self._path = kwargs.get('path', '.')

    def getPath(self):
        return self._path

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

        fileTree = TTkTree()
        fileTree.setHeaderLabels(["Name", "Size", "Type", "Date Modified"])
        fileTree.itemExpanded.connect(TTkFileDialogPicker._updateChildren)

        for i in TTkFileDialogPicker._getFileItems(self._path):
            fileTree.addTopLevelItem(i)

        self.layout().addWidget(fileTree,0,0)

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
                ret.append(_FileTreeWidgetItem([ n, "",   "Dir",  time],path=nodePath, childIndicatorPolicy=TTkK.ShowIndicator))
            elif os.path.isfile(nodePath):
                ret.append(_FileTreeWidgetItem([ n, size, "File", time],path=nodePath, childIndicatorPolicy=TTkK.DontShowIndicator))
            elif os.path.islink(nodePath):
                pass
            elif os.path.ismount(nodePath):
                pass
        return ret

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