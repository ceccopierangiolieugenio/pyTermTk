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

__all__ = ['TTkFileTreeWidget']

import os
import datetime

from TermTk.TTkCore.color import TTkColor

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.cfg import TTkCfg
from TermTk.TTkCore.string import TTkString
from TermTk.TTkWidgets.TTkModelView.treewidget import TTkTreeWidget
from TermTk.TTkWidgets.TTkModelView.filetreewidgetitem import TTkFileTreeWidgetItem
from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal

class TTkFileTreeWidget(TTkTreeWidget):
    '''
    A :py:class:`TTkFileTreeWidget` provide a widget that allow users to select files or directories.

    The :py:class:`TTkFileTree` class enables a user to traverse the file system in order to select one or many files or a directory.

    ::

        Name                                 ▼╿Size         ╿Type        ╿Date Modified       ╿▲
         ∙ Makefile                           │      3.80 KB│File        │2024-11-04 20:37:22 │┊
         ∙ README.md                          │      7.50 KB│File        │2024-06-08 15:34:09 │┊
         - TermTk/                            │             │Folder      │2024-06-08 15:34:12 │┊
           + TTkAbstract/                     │             │Folder      │2024-11-04 20:37:22 │▓
           + TTkCore/                         │             │Folder      │2024-11-04 20:37:22 │▓
           + TTkCrossTools/                   │             │Folder      │2024-06-08 15:34:12 │▓
           + TTkGui/                          │             │Folder      │2024-11-04 20:37:22 │▓
           + TTkLayouts/                      │             │Folder      │2024-11-04 20:37:22 │▓
           - TTkTemplates/                    │             │Folder      │2024-11-04 20:37:22 │┊
             ∙ __init__.py                    │    120 bytes│File        │2024-11-04 20:37:22 │┊
             + __pycache__/                   │             │Folder      │2024-11-05 08:47:38 │┊
             ∙ dragevents.py                  │      2.79 KB│File        │2024-11-04 20:37:22 │┊
             ∙ keyevents.py                   │      2.52 KB│File        │2024-11-04 20:37:22 │┊
             ∙ mouseevents.py                 │      5.16 KB│File        │2024-11-04 20:37:22 │┊
           + TTkTestWidgets/                  │             │Folder      │2024-11-04 20:37:22 │┊
           + TTkTheme/                        │             │Folder      │2024-06-08 15:34:12 │┊
           + TTkTypes/                        │             │Folder      │2024-06-08 15:34:12 │┊
           + TTkUiTools/                      │             │Folder      │2024-11-04 20:37:22 │┊
           + TTkWidgets/                      │             │Folder      │2024-11-04 20:37:22 │┊
           ∙ __init__.py                      │    327 bytes│File        │2024-11-04 19:56:26 │▼

    Quickstart:

    .. code-block:: python

        import TermTk as ttk

        root = ttk.TTk(layout=ttk.TTkGridLayout())

        fileTree = ttk.TTkFileTree(parent=root, path='.')

        root.mainloop()
    '''

    fileClicked:pyTTkSignal
    '''
    This signal is emitted when a file is clicked

    :param file:
    :type  file: :py:class:`TTkFileTreeWidgetItem`
    '''
    folderClicked:pyTTkSignal
    '''
    This signal is emitted when a folder is clicked

    :param folder:
    :type  folder: :py:class:`TTkFileTreeWidgetItem`
    '''
    fileDoubleClicked:pyTTkSignal
    '''
    This signal is emitted when a file is doubleclicked

    :param file:
    :type  file: :py:class:`TTkFileTreeWidgetItem`
    '''
    folderDoubleClicked:pyTTkSignal
    '''
    This signal is emitted when a folder is doubleclicked

    :param folder:
    :type  folder: :py:class:`TTkFileTreeWidgetItem`
    '''
    fileActivated:pyTTkSignal
    '''
    This signal is emitted when a file is activated

    :param file:
    :type  file: :py:class:`TTkFileTreeWidgetItem`
    '''
    folderActivated:pyTTkSignal
    '''
    This signal is emitted when a fiilder is activated

    :param folder:
    :type  folder: :py:class:`TTkFileTreeWidgetItem`
    '''

    __slots__ = ('_path', '_filter',
                 # Signals
                 'fileClicked', 'folderClicked', 'fileDoubleClicked', 'folderDoubleClicked', 'fileActivated', 'folderActivated')
    def __init__(self,
                 path:str='.',
                 **kwargs) -> None:
        '''
        :param path: the starting path opened by the :py:class:`TTkFileTreeWidget`, defaults to the current path ('.')
        :type  path: str, optional
        '''
        # Signals
        self.fileClicked         = pyTTkSignal(TTkFileTreeWidgetItem)
        self.folderClicked       = pyTTkSignal(TTkFileTreeWidgetItem)
        self.fileDoubleClicked   = pyTTkSignal(TTkFileTreeWidgetItem)
        self.folderDoubleClicked = pyTTkSignal(TTkFileTreeWidgetItem)
        self.fileActivated       = pyTTkSignal(TTkFileTreeWidgetItem)
        self.folderActivated     = pyTTkSignal(TTkFileTreeWidgetItem)
        self._path   = path
        self._filter = '*'
        super().__init__(**kwargs)
        self.setHeaderLabels(["Name", "Size", "Type", "Date Modified"])
        self.openPath(self._path)
        self.resizeColumnToContents(0)
        self.resizeColumnToContents(1)
        self.resizeColumnToContents(2)
        self.resizeColumnToContents(3)
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
        if not os.path.exists(path): return
        self._path = path

        self.clear()
        for i in TTkFileTreeWidget._getFileItems(path):
            self.addTopLevelItem(i)
        self.setFilter(self._filter)

    @staticmethod
    def _getFileItems(path):
        path = os.path.abspath(path)
        if not os.path.exists(path): return []
        dir_list = os.listdir(path)
        ret = []
        for n in dir_list:
            nodePath = os.path.join(path,n)

            def _getStat(_path):
                info = os.stat(_path)
                time = datetime.datetime.fromtimestamp(info.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
                if info.st_size > (1024*1024*1024):
                    size = f"{info.st_size/(1024*1024*1024):.2f} GB"
                if info.st_size > (1024*1024):
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
                    name = TTkString()+TTkCfg.theme.linkNameColor+n+'/'+TTkColor.RST+' -> '+TTkCfg.theme.folderNameColor+os.readlink(nodePath)
                    typef = "Folder Link"
                else:
                    name = TTkString()+color+n+'/'
                    typef = "Folder"

                ret.append(TTkFileTreeWidgetItem(
                                [ name, "", typef, time],
                                raw = [ n , -1 , typef , rawTime ],
                                path=nodePath,
                                type=TTkFileTreeWidgetItem.DIR,
                                icon=TTkString() + TTkCfg.theme.folderIconColor + TTkCfg.theme.fileIcon.folderClose + TTkColor.RST,
                                childIndicatorPolicy=TTkK.ShowIndicator))

            elif os.path.isfile(nodePath) or os.path.islink(nodePath):
                if os.path.exists(nodePath):
                    time, size, rawTime, rawSize = _getStat(nodePath)
                    if os.access(nodePath, os.X_OK):
                        color = TTkCfg.theme.executableColor
                        typef="Exec"
                    else:
                        color = TTkCfg.theme.fileNameColor
                        typef="File"
                else:
                    time, size, rawTime, rawSize = "", "", 0, 0
                    color = TTkCfg.theme.failNameColor
                    typef="Broken"

                if os.path.islink(nodePath):
                    name = TTkString()+TTkCfg.theme.linkNameColor+n+TTkColor.RST+' -> '+color+os.readlink(nodePath)
                    typef += " Link"
                else:
                    name = TTkString()+color+n

                _, ext = os.path.splitext(n)
                if ext: ext = f"{ext[1:]} "
                ret.append(TTkFileTreeWidgetItem(
                                [ name, size, typef, time],
                                raw = [ n , rawSize , typef , rawTime ],
                                path=nodePath,
                                type=TTkFileTreeWidgetItem.FILE,
                                icon=TTkString() + TTkCfg.theme.fileIconColor + TTkCfg.theme.fileIcon.getIcon(n) + TTkColor.RST,
                                childIndicatorPolicy=TTkK.DontShowIndicator))
        return ret

    @staticmethod
    def _folderExpanded(item):
        item.setIcon(0, TTkString() + TTkCfg.theme.folderIconColor + TTkCfg.theme.fileIcon.folderOpen + TTkColor.RST,)

    @staticmethod
    def _folderCollapsed(item):
        item.setIcon(0, TTkString() + TTkCfg.theme.folderIconColor + TTkCfg.theme.fileIcon.folderClose + TTkColor.RST,)

    @pyTTkSlot(TTkFileTreeWidgetItem)
    def _updateChildren(self, item):
        if item.children(): return
        item.addChildren(children := TTkFileTreeWidget._getFileItems(item.path()))
        for i in children:
            # TODO: Find a better way than calling an internal function
            i._processFilter(self._filter)

    @pyTTkSlot(TTkFileTreeWidgetItem, int)
    def _activated(self, item, _):
        path = item.path()
        if os.path.isdir(path):
            self.folderActivated.emit(item)
        elif os.path.isfile(path):
            self.fileActivated.emit(item)