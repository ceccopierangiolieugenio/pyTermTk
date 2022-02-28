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
import re
import datetime

from TermTk.TTkCore.color import TTkColor

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.cfg import TTkCfg
from TermTk.TTkCore.string import TTkString
from TermTk.TTkWidgets.TTkModelView.treewidget import TTkTreeWidget
from TermTk.TTkWidgets.TTkModelView.filetreewidgetitem import TTkFileTreeWidgetItem
from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal


class TTkFileTreeWidget(TTkTreeWidget):
    __slots__ = (
        "_path",
        "_filter",
        # Signals
        "fileClicked",
        "folderClicked",
        "fileDoubleClicked",
        "folderDoubleClicked",
        "fileActivated",
        "folderActivated",
    )

    def __init__(self, *args, **kwargs):
        # Signals
        self.fileClicked = pyTTkSignal(TTkFileTreeWidgetItem)
        self.folderClicked = pyTTkSignal(TTkFileTreeWidgetItem)
        self.fileDoubleClicked = pyTTkSignal(TTkFileTreeWidgetItem)
        self.folderDoubleClicked = pyTTkSignal(TTkFileTreeWidgetItem)
        self.fileActivated = pyTTkSignal(TTkFileTreeWidgetItem)
        self.folderActivated = pyTTkSignal(TTkFileTreeWidgetItem)
        TTkTreeWidget.__init__(self, *args, **kwargs)
        self._name = kwargs.get("name", "TTkFileTreeWidget")
        self._path = kwargs.get("path", ".")
        self._filter = "*"
        self.setHeaderLabels(["Name", "Size", "Type", "Date Modified"])
        self.openPath(self._path)
        self.itemExpanded.connect(self._folderExpanded)
        self.itemCollapsed.connect(self._folderCollapsed)
        self.itemExpanded.connect(self._updateChildren)
        self.itemActivated.connect(self._activated)

    def setFilter(self, filter):
        self._filter = filter
        # TODO: Avoid to refer directly '_rootItem'
        TTkFileTreeWidgetItem.setFilter(self._rootItem, filter)

    def getOpenPath(self):
        return self._path

    def openPath(self, path):
        self._path = path

        self.clear()
        for i in TTkFileTreeWidget._getFileItems(path):
            self.addTopLevelItem(i)
        self.setFilter(self._filter)

    @staticmethod
    def _getFileItems(path):
        path = os.path.abspath(path)
        if not os.path.exists(path):
            return []
        dir_list = os.listdir(path)
        ret = []
        for n in dir_list:
            nodePath = os.path.join(path, n)

            def _getStat(_path):
                info = os.stat(_path)
                time = datetime.datetime.fromtimestamp(info.st_ctime).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                if info.st_size > (1024 * 1024 * 1024):
                    size = f"{info.st_size/(1024*1024*1024):.2f} GB"
                if info.st_size > (1024 * 1024):
                    size = f"{info.st_size/(1024*1024):.2f} MB"
                elif info.st_size > 1024:
                    size = f"{info.st_size/1024:.2f} KB"
                else:
                    size = f"{info.st_size} bytes"
                return time, size, info.st_ctime, info.st_size

            if os.path.isdir(nodePath):
                if os.path.exists(nodePath):
                    time, _, rawTime, _ = _getStat(nodePath)
                    color = TTkCfg.theme.folderNameColor
                else:
                    time, _, rawTime, _ = ""
                    color = TTkCfg.theme.failNameColor

                if os.path.islink(nodePath):
                    name = (
                        TTkString()
                        + TTkCfg.theme.linkNameColor
                        + n
                        + "/"
                        + TTkColor.RST
                        + " -> "
                        + TTkCfg.theme.folderNameColor
                        + os.readlink(nodePath)
                    )
                    typef = "Folder Link"
                else:
                    name = TTkString() + color + n + "/"
                    typef = "Folder"

                ret.append(
                    TTkFileTreeWidgetItem(
                        [name, "", typef, time],
                        raw=[n, -1, typef, rawTime],
                        path=nodePath,
                        type=TTkFileTreeWidgetItem.DIR,
                        icon=TTkString()
                        + TTkCfg.theme.folderIconColor
                        + TTkCfg.theme.fileIcon.folderClose
                        + TTkColor.RST,
                        childIndicatorPolicy=TTkK.ShowIndicator,
                    )
                )

            elif os.path.isfile(nodePath) or os.path.islink(nodePath):
                if os.path.exists(nodePath):
                    time, size, rawTime, rawSize = _getStat(nodePath)
                    if os.access(nodePath, os.X_OK):
                        color = TTkCfg.theme.executableColor
                        typef = "Exec"
                    else:
                        color = TTkCfg.theme.fileNameColor
                        typef = "File"
                else:
                    time, size, rawTime, rawSize = "", "", 0, 0
                    color = TTkCfg.theme.failNameColor
                    typef = "Broken"

                if os.path.islink(nodePath):
                    name = (
                        TTkString()
                        + TTkCfg.theme.linkNameColor
                        + n
                        + TTkColor.RST
                        + " -> "
                        + color
                        + os.readlink(nodePath)
                    )
                    typef += " Link"
                else:
                    name = TTkString() + color + n

                _, ext = os.path.splitext(n)
                if ext:
                    ext = f"{ext[1:]} "
                ret.append(
                    TTkFileTreeWidgetItem(
                        [name, size, typef, time],
                        raw=[n, rawSize, typef, rawTime],
                        path=nodePath,
                        type=TTkFileTreeWidgetItem.FILE,
                        icon=TTkString()
                        + TTkCfg.theme.fileIconColor
                        + TTkCfg.theme.fileIcon.getIcon(n)
                        + TTkColor.RST,
                        childIndicatorPolicy=TTkK.DontShowIndicator,
                    )
                )
        return ret

    @staticmethod
    def _folderExpanded(item):
        item.setIcon(
            0,
            TTkString()
            + TTkCfg.theme.folderIconColor
            + TTkCfg.theme.fileIcon.folderOpen
            + TTkColor.RST,
        )

    @staticmethod
    def _folderCollapsed(item):
        item.setIcon(
            0,
            TTkString()
            + TTkCfg.theme.folderIconColor
            + TTkCfg.theme.fileIcon.folderClose
            + TTkColor.RST,
        )

    @pyTTkSlot(TTkFileTreeWidgetItem)
    def _updateChildren(self, item):
        if item.children():
            return
        for i in TTkFileTreeWidget._getFileItems(item.path()):
            item.addChild(i)
            # TODO: Find a better way than calling an internal function
            i._processFilter(self._filter)

    @pyTTkSlot(TTkFileTreeWidgetItem, int)
    def _activated(self, item, _):
        path = item.path()
        if os.path.isdir(path):
            self.folderActivated.emit(item)
        elif os.path.isfile(path):
            self.fileActivated.emit(item)
