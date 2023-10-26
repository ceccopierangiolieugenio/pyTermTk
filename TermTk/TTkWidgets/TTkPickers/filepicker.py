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

__all__ = ['TTkFileDialog', 'TTkFileDialogPicker', 'TTkFileButtonPicker']

import os
import re

from TermTk.TTkCore.color import TTkColor

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.cfg import TTkCfg
from TermTk.TTkCore.helper import TTkHelper
from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal
from TermTk.TTkCore.string import TTkString
from TermTk.TTkWidgets.lineedit import TTkLineEdit
from TermTk.TTkWidgets.window import TTkWindow
from TermTk.TTkWidgets.splitter import TTkSplitter
from TermTk.TTkWidgets.combobox import TTkComboBox
from TermTk.TTkWidgets.button import TTkButton
from TermTk.TTkWidgets.label import TTkLabel
from TermTk.TTkWidgets.list_ import TTkList
from TermTk.TTkLayouts.gridlayout import TTkGridLayout
from TermTk.TTkWidgets.TTkModelView.filetree import TTkFileTree
from TermTk.TTkWidgets.TTkModelView.filetreewidgetitem import TTkFileTreeWidgetItem

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

class TTkFileDialogPicker(TTkWindow):
    ''' TTkFileDialogPicker:

    ::

        ╔═════════════════════════════════════════════════════════════════════════╗
        ║ Pick Something                                                    [^][x]║
        ╟─────────────────────────────────────────────────────────────────────────╢
        ║Look in:      [/home/one/github/Varie/pyTermTk                ^][<][>][^]║
        ║┌──────────╥────────────────────────────────────────────────────────────┐║
        ║│∙ Computer║Name               ▼╿Size     ╿Type   ╿Date Modified      ╿▲│║
        ║│∙ Home    ║   - TTkUiTools/    │         │Folder │2023-04-18 16:38:03│┊│║
        ║│          ║     ∙ __init__.py  │ 75 bytes│File   │2023-04-18 16:38:03│┊│║
        ║│          ║     + __pycache__/ │         │Folder │2023-04-18 23:54:33│┊│║
        ║│          ║     + properties/  │         │Folder │2023-04-18 16:38:03│┊│║
        ║│          ║     ∙ uiloader.py  │  7.96 KB│File   │2023-04-18 16:38:03│┊│║
        ║│          ║     ∙ uiproperties.│  2.39 KB│File   │2023-04-18 16:38:03│▓│║
        ║│          ║   + TTkWidgets/    │         │Folder │2023-04-18 16:38:03│▓│║
        ║│          ║   ∙ __init__.py    │272 bytes│File   │2023-04-18 16:38:03│▓│║
        ║│          ║   + __pycache__/   │         │Folder │2023-04-18 23:54:33│▓│║
        ║│          ║ + demo/            │         │Folder │2023-04-18 16:38:03│┊│║
        ║│          ║ + docs/            │         │Folder │2023-04-27 22:16:30│┊│║
        ║│          ║ + experiments/     │         │Folder │2023-04-27 13:10:29│┊│║
        ║│          ║ ∙ pippo.py         │  1.72 KB│File   │2023-04-26 21:01:53│┊│║
        ║│          ║ ∙ profiler.bin     │256.71 KB│File   │2023-04-10 06:01:03│▼│║
        ║└──────────╨────────────────────────────────────────────────────────────┘║
        ║File name:    /home/one/github/Varie/pyTermTk/TermTk/TTkUiTools/ [ Open ]║
        ║Files of type:[All Files (*)                                   ^][Cancel]║
        ╚═════════════════════════════════════════════════════════════════════════╝

    Demo: `formwidgets.py <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/demo/showcase/filepicker.py>`_
    (`Try Online <https://ceccopierangiolieugenio.github.io/pyTermTk/sandbox/sandbox.html?fileUri=https://raw.githubusercontent.com/ceccopierangiolieugenio/pyTermTk/main/demo/showcase/filepicker.py>`__)

    `ttkdesigner Tutorial <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/tutorial/ttkDesigner/textEdit/textEdit.rst>`_

    :param path: the current path used in the file dialog, defaults to "."
    :type path: str, optional

    :param caption: the title of the dialog, defaults to "**File Dialog**"
    :type caption: str, optional

    :param filter: List of filters separated with "**;;**", defaults to "**All Files (*)**".

            Example:

            ::

                filter="Images (*.png *.xpm *.jpg);;Text files (*.txt);;XML files (*.xml)"

    :type filter: str, optional


    :param fileMode: The file mode defines the number and type of items that the user is expected to select in the dialog, defaults to :class:`~TermTk.TTkCore.constant.TTkConstant.FileMode.Anyfile`
    :type fileMode: :class:`~TermTk.TTkCore.constant.TTkConstant.FileMode`, optional

    :param acceptMode: TThe action mode defines whether the dialog is for opening or saving files, defaults to :class:`~TermTk.TTkCore.constant.TTkConstant.AcceptMode.AcceptOpen`
    :type acceptMode: :class:`~TermTk.TTkCore.constant.TTkConstant.AcceptMode`, optional

    +-----------------------------------------------------------------------------------------------+
    | `Signals <https://ceccopierangiolieugenio.github.io/pyTermTk/tutorial/003-signalslots.html>`_ |
    +-----------------------------------------------------------------------------------------------+

        .. py:method:: pathPicked(pathName)
            :signal:

            This signal is emitted whenever any path is picked (Files/Dir)

            :param pathName: the name of the path
            :type pathName: str

        .. py:method:: filePicked(fileName)
            :signal:

            This signal is emitted whenever any file is picked

            :param fileName: the name of the file
            :type fileName: str

        .. py:method:: folderPicked(dirName)
            :signal:

            This signal is emitted whenever any folder is picked

            :param dirName: the name of the folder
            :type dirName: str
    '''
    __slots__ = ('_path', '_recentPath', '_recentPathId', '_filters', '_filter', '_caption', '_fileMode', '_acceptMode',
                 # Widgets
                 '_fileTree', '_lookPath', '_btnPrev', '_btnNext', '_btnUp',
                 '_fileName', '_fileType', '_btnOpen', '_btnCancel',
                 # Signals
                 'pathPicked', 'filePicked', 'filesPicked', 'folderPicked')

    def __init__(self, *args, **kwargs):
        # Signals
        self.pathPicked = pyTTkSignal(str)
        self.filePicked = pyTTkSignal(str)
        self.filesPicked = pyTTkSignal(list)
        self.folderPicked = pyTTkSignal(str)

        super().__init__(*args, **kwargs)
        self.setWindowFlag(TTkK.WindowFlag.WindowMaximizeButtonHint | TTkK.WindowFlag.WindowCloseButtonHint)

        self._recentPathId = -1
        self._recentPath = []

        self._path     = os.path.abspath(kwargs.get('path','.'))
        if os.path.isdir(self._path) and self._path[-1]!='/':
            self._path += '/'
        self._filter   = '*'
        self._filters  = kwargs.get('filter','All Files (*)')
        self._caption  = kwargs.get('caption','File Dialog')
        self._fileMode = kwargs.get('fileMode',TTkK.FileMode.AnyFile)
        self._acceptMode = kwargs.get('acceptMode',TTkK.AcceptMode.AcceptOpen)

        self.setTitle(self._caption)
        self.setLayout(TTkGridLayout())

        # Top (absPath)
        topLayout = TTkGridLayout()
        self.layout().addItem(topLayout,0,0)

        self._lookPath = TTkComboBox(textAlign=TTkK.LEFT_ALIGN)
        self._btnPrev  = TTkButton(text="<",maxWidth=3, enabled=False)
        self._btnNext  = TTkButton(text=">",maxWidth=3, enabled=False)
        self._btnUp    = TTkButton(text="^",maxWidth=3, enabled=True)
        self._btnPrev.clicked.connect(self._openPrev)
        self._btnNext.clicked.connect(self._openNext)
        self._btnUp.clicked.connect(  self._openUp)

        topLayout.addWidget(TTkLabel(text="Look in:",maxWidth=14),      0,0)
        topLayout.addWidget(self._lookPath , 0,1)
        topLayout.addWidget(self._btnPrev  , 0,2)
        topLayout.addWidget(self._btnNext  , 0,3)
        topLayout.addWidget(self._btnUp    , 0,4)

        # Bottom (File Name, Controls)
        self._fileName  = TTkLineEdit()
        self._fileType  = TTkComboBox(textAlign=TTkK.LEFT_ALIGN)
        self._btnOpen   = TTkButton(text="Open" if self._acceptMode == TTkK.AcceptMode.AcceptOpen else "Save",  maxWidth=8, enabled=False)
        self._btnCancel = TTkButton(text="Cancel",maxWidth=8)

        for f in self._filters.split(';;'):
            if re.match(r".*\(.*\)",f):
                self._fileType.addItem(f)
        self._fileType.setCurrentIndex(0)
        self._fileType.currentTextChanged.connect(self._fileTypeChanged)

        self._btnOpen.clicked.connect(self._open)
        self._btnCancel.clicked.connect(self.close)

        self._fileName.returnPressed.connect(self._open)
        self._fileName.textChanged.connect(self._checkFileName)
        self._fileName.textEdited.connect(self._checkFileName)


        bottomLayout = TTkGridLayout()
        self.layout().addItem(bottomLayout,2,0)
        bottomLayout.addWidget(TTkLabel(text="File name:"     ,maxWidth=14),      0,0)
        bottomLayout.addWidget(TTkLabel(text="Files of type:" ,maxWidth=14),      1,0)
        bottomLayout.addWidget(self._fileName  , 0,1)
        bottomLayout.addWidget(self._fileType  , 1,1)
        bottomLayout.addWidget(self._btnOpen   , 0,2)
        bottomLayout.addWidget(self._btnCancel , 1,2)

        # Center (self._fileTree, Bookmarks)
        splitter = TTkSplitter(border=True)
        self.layout().addWidget(splitter,1,0)

        bookmarks = TTkList(parent=splitter)
        bookmarks.addItem(TTkString() + TTkCfg.theme.fileIconColor + TTkCfg.theme.fileIcon.computer + TTkColor.RST+" Computer", data='/')
        bookmarks.addItem(TTkString() + TTkCfg.theme.fileIconColor + TTkCfg.theme.fileIcon.home     + TTkColor.RST+" Home", data=os.path.expanduser("~"))
        def _bookmarksCallback(item):
            self._openNewPath(item.data())
        bookmarks.itemClicked.connect(_bookmarksCallback)

        # Home Folder (Win Compatible):
        #   os.path.expanduser("~")

        self._fileTree = TTkFileTree(parent=splitter)
        splitter.setSizes([10,None])

        self._fileTree.itemClicked.connect(self._selectedItem)
        self._fileTree.itemActivated.connect(self._activatedItem)

        self._lookPath.currentTextChanged.connect(self._openNewPath)
        self._fileName.setText(self._path)
        if os.path.isdir(self._path):
            self._openNewPath(self._path, True)
        else:
            self._openNewPath(os.path.dirname(self._path), True)
        self._fileTypeChanged(self._fileType.currentText())

    def acceptMode(self) -> TTkK.AcceptMode:
        return self._acceptMode

    def setAcceptMode(self, mode:TTkK.AcceptMode):
        self._acceptMode = mode
        self._btnOpen.setText("Open" if mode == TTkK.AcceptMode.AcceptOpen else "Save")

    @pyTTkSlot(str)
    def _fileTypeChanged(self, type):
        self._filter = re.match(r".*\((.*)\)",type).group(1)
        self._fileTree.setFilter(self._filter)

    @pyTTkSlot(str)
    def _checkFileName(self, fileName):
        fileName = str(fileName)
        valid = False
        if self._fileMode == TTkK.FileMode.ExistingFile:
            valid = os.path.exists(fileName) and os.path.isfile(fileName)
        elif self._fileMode == TTkK.FileMode.Directory:
            valid = os.path.exists(fileName) and os.path.isdir(fileName)
        elif self._fileMode == TTkK.FileMode.AnyFile:
            valid = os.path.isdir(os.path.dirname(fileName)) and not os.path.isdir(fileName)
        else:
            pass
        if valid:
            self._btnOpen.setEnabled()
        else:
            self._btnOpen.setDisabled()

    @pyTTkSlot()
    def _open(self):
        fileName = str(self._fileName.text())
        if self._fileMode != TTkK.FileMode.AnyFile      and not os.path.exists(fileName): return
        if self._fileMode == TTkK.FileMode.ExistingFile and not os.path.isfile(fileName): return
        if self._fileMode == TTkK.FileMode.Directory    and not os.path.isdir(fileName):  return
        self.close()
        if self._fileMode in (TTkK.FileMode.AnyFile,TTkK.FileMode.ExistingFile):
            self.filePicked.emit(fileName)
        if self._fileMode == TTkK.FileMode.Directory:
            self.folderPicked.emit(fileName)
        self.pathPicked.emit(fileName)

    @pyTTkSlot(TTkFileTreeWidgetItem, int)
    def _selectedItem(self, item, _):
        path = item.path()
        if os.path.isdir(path) and path[-1]!='/':
            path = path+'/'
        self._fileName.setText(path)

    @pyTTkSlot(TTkFileTreeWidgetItem, int)
    def _activatedItem(self, item, _):
        path = str(item.path())
        if os.path.isdir(path):
             self._openNewPath(path, True)
        elif os.path.isfile(path):
            self._open()

    def filemode(self):
        return self._fileMode

    def setFileMode(self, fileMode):
        self._fileMode = fileMode

    def _openPrev(self):
        if self._recentPathId<=0 or self._recentPathId>=len(self._recentPath):
            self._btnPrev.setDisabled()
            return
        self._recentPathId -= 1
        self._openNewPath(self._recentPath[self._recentPathId],False)
        if self._recentPathId<=0:
            self._btnPrev.setDisabled()
        self._btnNext.setEnabled()

    def _openNext(self):
        if self._recentPathId<0 or self._recentPathId>=len(self._recentPath)-1:
            self._btnNext.setDisabled()
            return
        self._recentPathId += 1
        self._openNewPath(self._recentPath[self._recentPathId],False)
        if self._recentPathId>=len(self._recentPath)-1:
            self._btnNext.setDisabled()
        self._btnPrev.setEnabled()

    def _openUp(self):
        path = os.path.abspath(self._recentPath[self._recentPathId])
        path, e = os.path.split(path)
        if e:
            self._openNewPath(path, True)

    def _openNewPath(self, path, addToRecent=True):
        self._path = path
        if addToRecent:
            self._recentPathId = len(self._recentPath)
            self._recentPath.append(path)
            if self._recentPathId:
                self._btnPrev.setEnabled()
            self._btnNext.setDisabled()
        self._fileTree.openPath(path)
        self._lookPath.currentTextChanged.disconnect(self._openNewPath)
        self._lookPath.clear()
        self._lookPath.addItems(TTkFileDialogPicker._getListLook(self._path))
        self._lookPath.setCurrentIndex(0)
        self._lookPath.currentTextChanged.connect(self._openNewPath)

    @staticmethod
    def _getListLook(path):
        path = os.path.abspath(path)
        ret = [path]
        while True:
            path, e = os.path.split(path)
            if e:
                ret.append(path)
            if not path or path=='/' or path[1:]==":\\":
                break
        return ret
class TTkFileDialog:
    @staticmethod
    def getOpenFileName(caption, dir=".", filter="All Files (*)", options=None):
        pass

class TTkFileButtonPicker(TTkButton):
    ''' TTkFileButtonPicker:

    ::

        ┌────┐
        │File│
        ╘════╛

        ╔═════════════════════════════════════════════════════════════════════════╗
        ║ Pick Something                                                    [^][x]║
        ╟─────────────────────────────────────────────────────────────────────────╢
        ║Look in:      [/home/one/github/Varie/pyTermTk                ^][<][>][^]║
        ║┌──────────╥────────────────────────────────────────────────────────────┐║
        ║│∙ Computer║Name               ▼╿Size     ╿Type   ╿Date Modified      ╿▲│║
        ║│∙ Home    ║   - TTkUiTools/    │         │Folder │2023-04-18 16:38:03│┊│║
        ║│          ║     ∙ __init__.py  │ 75 bytes│File   │2023-04-18 16:38:03│┊│║
        ║│          ║     + __pycache__/ │         │Folder │2023-04-18 23:54:33│┊│║
        ║│          ║     + properties/  │         │Folder │2023-04-18 16:38:03│┊│║
        ║│          ║     ∙ uiloader.py  │  7.96 KB│File   │2023-04-18 16:38:03│┊│║
        ║│          ║     ∙ uiproperties.│  2.39 KB│File   │2023-04-18 16:38:03│▓│║
        ║│          ║   + TTkWidgets/    │         │Folder │2023-04-18 16:38:03│▓│║
        ║│          ║   ∙ __init__.py    │272 bytes│File   │2023-04-18 16:38:03│▓│║
        ║│          ║   + __pycache__/   │         │Folder │2023-04-18 23:54:33│▓│║
        ║│          ║ + demo/            │         │Folder │2023-04-18 16:38:03│┊│║
        ║│          ║ + docs/            │         │Folder │2023-04-27 22:16:30│┊│║
        ║│          ║ + experiments/     │         │Folder │2023-04-27 13:10:29│┊│║
        ║│          ║ ∙ pippo.py         │  1.72 KB│File   │2023-04-26 21:01:53│┊│║
        ║│          ║ ∙ profiler.bin     │256.71 KB│File   │2023-04-10 06:01:03│▼│║
        ║└──────────╨────────────────────────────────────────────────────────────┘║
        ║File name:    /home/one/github/Varie/pyTermTk/TermTk/TTkUiTools/ [ Open ]║
        ║Files of type:[All Files (*)                                   ^][Cancel]║
        ╚═════════════════════════════════════════════════════════════════════════╝

    Demo: `formwidgets.py <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/demo/showcase/filepicker.py>`_
    (`Try Online <https://ceccopierangiolieugenio.github.io/pyTermTk/sandbox/sandbox.html?fileUri=https://raw.githubusercontent.com/ceccopierangiolieugenio/pyTermTk/main/demo/showcase/filepicker.py>`__)

    `ttkdesigner Tutorial <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/tutorial/ttkDesigner/textEdit/textEdit.rst>`_

    :param path: the current path used in the file dialog, defaults to "."
    :type path: str, optional

    :param caption: the title of the dialog, defaults to "**File Dialog**"
    :type caption: str, optional

    :param filter: List of filters separated with "**;;**", defaults to "**All Files (*)**".

            Example:

            ::

                filter="Images (*.png *.xpm *.jpg);;Text files (*.txt);;XML files (*.xml)"

    :type filter: str, optional


    :param fileMode: The file mode defines the number and type of items that the user is expected to select in the dialog, defaults to :class:`~TermTk.TTkCore.constant.TTkConstant.FileMode.Anyfile`
    :type fileMode: :class:`~TermTk.TTkCore.constant.TTkConstant.FileMode`, optional

    :param acceptMode: TThe action mode defines whether the dialog is for opening or saving files, defaults to :class:`~TermTk.TTkCore.constant.TTkConstant.AcceptMode.AcceptOpen`
    :type acceptMode: :class:`~TermTk.TTkCore.constant.TTkConstant.AcceptMode`, optional

    +-----------------------------------------------------------------------------------------------+
    | `Signals <https://ceccopierangiolieugenio.github.io/pyTermTk/tutorial/003-signalslots.html>`_ |
    +-----------------------------------------------------------------------------------------------+

        .. py:method:: pathPicked(pathName)
            :signal:

            This signal is emitted whenever any path is picked (Files/Dir)

            :param pathName: the name of the path
            :type pathName: str

        .. py:method:: filePicked(fileName)
            :signal:

            This signal is emitted whenever any file is picked

            :param fileName: the name of the file
            :type fileName: str

        .. py:method:: folderPicked(dirName)
            :signal:

            This signal is emitted whenever any folder is picked

            :param dirName: the name of the folder
            :type dirName: str
    '''
    __slots__ = ('_filter', '_caption', '_fileMode', '_acceptMode', '_path'
                 # Signals
                 'pathPicked', 'filePicked', 'filesPicked', 'folderPicked')
    def __init__(self, *args, **kwargs):
        # Signals
        self.pathPicked = pyTTkSignal(str)
        self.filePicked = pyTTkSignal(str)
        self.filesPicked = pyTTkSignal(list)
        self.folderPicked = pyTTkSignal(str)
        super().__init__(*args, **kwargs)
        self._path  = kwargs.get('path','.')
        self._filter   = kwargs.get('filter','All Files (*)')
        self._caption  = kwargs.get('caption','File Dialog')
        self._fileMode = kwargs.get('fileMode',TTkK.FileMode.AnyFile)
        self._acceptMode = kwargs.get('acceptMode',TTkK.AcceptMode.AcceptOpen)
        self.clicked.connect(self._fileButtonClicked)

    def filter(self): return self._filter
    def setFilter(self, filter): self._filter = filter

    def caption(self): return self._caption
    def setCaption(self, caption): self._caption = caption

    def acceptMode(self) -> TTkK.AcceptMode: return self._acceptMode
    def setAcceptMode(self, mode:TTkK.AcceptMode): self._acceptMode = mode

    def fileMode(self) -> TTkK.FileMode: return self._fileMode
    def setFileMode(self, fm:TTkK.FileMode): self._fileMode = fm

    def path(self): return self._path
    def setPath(self, path): self._path = path

    @pyTTkSlot()
    def _fileButtonClicked(self):
        filePicker = TTkFileDialogPicker(pos = (3,3), size=(80,30),
                                         caption=self._caption,
                                         path=self._path,
                                         filter=self._filter,
                                         acceptMode=self._acceptMode,
                                         fileMode=self._fileMode)
        filePicker.pathPicked.connect(self.pathPicked.emit)
        filePicker.filePicked.connect(self.filePicked.emit)
        filePicker.filesPicked.connect(self.filesPicked.emit)
        filePicker.folderPicked.connect(self.folderPicked.emit)
        TTkHelper.overlay(None, filePicker, 5, 5, True)
