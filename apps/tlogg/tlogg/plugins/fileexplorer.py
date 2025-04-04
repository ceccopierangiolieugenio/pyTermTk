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

import TermTk as ttk

import tlogg

class FileTree(ttk.TTkContainer):
    __slots__ = (
        '_recentPath', '_recentPathId',
        '_controlsLayout',
        '_ftCbFollow', '_ftBtnPrev', '_ftBtnNext', '_ftBtnUp', '_fileTree',
        # Forwarded Methods
        'fileActivated')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._name = kwargs.get('name' , 'FileTree' )

        self.setLayout(ttk.TTkVBoxLayout())

        self._controlsLayout = ttk.TTkHBoxLayout()
        self.layout().addItem(self._controlsLayout)

        self._ftCbFollow = ttk.TTkCheckbox(text="Follow", maxWidth=9, checked=False)
        self._ftBtnPrev  = ttk.TTkButton(text="<",maxWidth=3, enabled=False)
        self._ftBtnNext  = ttk.TTkButton(text=">",maxWidth=3, enabled=False)
        self._ftBtnUp    = ttk.TTkButton(text="^",maxWidth=3, enabled=True)
        self._controlsLayout.addWidget(self._ftCbFollow)
        self._controlsLayout.addWidget(ttk.TTkSpacer())
        self._controlsLayout.addWidget(self._ftBtnPrev)
        self._controlsLayout.addWidget(self._ftBtnNext)
        self._controlsLayout.addWidget(self._ftBtnUp)

        self._fileTree = ttk.TTkFileTree(parent=self, path=".")

        self._recentPath = []
        self._recentPathId = -1
        self._addFolder(os.path.abspath('.'))

        self._ftBtnPrev.clicked.connect(self._openPrev)
        self._ftBtnNext.clicked.connect(self._openNext)
        self._ftBtnUp.clicked.connect(self._openUp)

        self._fileTree.folderActivated.connect(self._openFolder)

        # Forward Functions
        self._fileTree.fileActivated.connect(lambda x: tlogg.tloggProxy.openFile(x.path()))

        tlogg.tloggProxy.tloggFocussed.connect(self.follow)

    @ttk.pyTTkSlot(tlogg.TloggViewerProxy, str)
    def follow(self, _, path):
        if self._ftCbFollow.checkState() == ttk.TTkK.Checked:
            if os.path.isfile(path):
                path, _ = os.path.split(path)
            self._fileTree.openPath(path)

    def _addFolder(self, dir):
        if not self._recentPath or dir != self._recentPath[-1]:
            self._recentPath.append(dir)
        self._recentPathId = len(self._recentPath)-1
        if self._recentPathId:
            self._ftBtnPrev.setEnabled()
        self._ftBtnNext.setDisabled()

    @ttk.pyTTkSlot(ttk.TTkFileTreeWidgetItem)
    def _openFolder(self, dir):
        self._fileTree.openPath(dir.path())
        self._addFolder(dir.path())

    @ttk.pyTTkSlot()
    def _openPrev(self):
        if self._recentPathId<=0 or self._recentPathId>=len(self._recentPath):
            self._ftBtnPrev.setDisabled()
            return
        self._recentPathId -= 1
        self._fileTree.openPath(self._recentPath[self._recentPathId])
        if self._recentPathId<=0:
            self._ftBtnPrev.setDisabled()
        self._ftBtnNext.setEnabled()

    @ttk.pyTTkSlot()
    def _openNext(self):
        if self._recentPathId<0 or self._recentPathId>=len(self._recentPath)-1:
            self._ftBtnNext.setDisabled()
            return
        self._recentPathId += 1
        self._fileTree.openPath(self._recentPath[self._recentPathId])
        if self._recentPathId>=len(self._recentPath)-1:
            self._ftBtnNext.setDisabled()
        self._ftBtnPrev.setEnabled()

    @ttk.pyTTkSlot()
    def _openUp(self):
        path = os.path.abspath(self._fileTree.getOpenPath())
        path, e = os.path.split(path)
        if e:
            self._addFolder(path)
            self._fileTree.openPath(path)

tlogg.TloggPlugin(
    name="File Explorer",
    position=ttk.TTkK.LEFT,
    visible=True,
    widget=FileTree())
