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

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal
from TermTk.TTkWidgets.TTkModelView.tree import TTkTree
from TermTk.TTkWidgets.TTkModelView.filetreewidget import TTkFileTreeWidget


class TTkFileTree(TTkTree):
    __slots__ = (
        "_fileTreeWidget",
        # Forwarded Methods
        "openPath",
        "getOpenPath",
        # Forwarded Signals
        "fileClicked",
        "folderClicked",
        "fileDoubleClicked",
        "folderDoubleClicked",
        "fileActivated",
        "folderActivated",
    )

    def __init__(self, *args, **kwargs):
        wkwargs = kwargs.copy()
        if "parent" in wkwargs:
            wkwargs.pop("parent")
        self._fileTreeWidget = TTkFileTreeWidget(*args, **wkwargs)

        TTkTree.__init__(self, *args, **kwargs, treeWidget=self._fileTreeWidget)
        self._name = kwargs.get("name", "TTkFileTree")

        # Forward Signals
        self.fileClicked = self._fileTreeWidget.fileClicked
        self.folderClicked = self._fileTreeWidget.folderClicked
        self.fileDoubleClicked = self._fileTreeWidget.fileDoubleClicked
        self.folderDoubleClicked = self._fileTreeWidget.folderDoubleClicked
        self.fileActivated = self._fileTreeWidget.fileActivated
        self.folderActivated = self._fileTreeWidget.folderActivated

        # Forward Methods
        self.openPath = self._fileTreeWidget.openPath
        self.getOpenPath = self._fileTreeWidget.getOpenPath
