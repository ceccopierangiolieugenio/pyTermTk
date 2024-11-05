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

__all__ = ['TTkFileTree']

from TermTk.TTkWidgets.TTkModelView.tree import TTkTree
from TermTk.TTkWidgets.TTkModelView.filetreewidget import TTkFileTreeWidget

class TTkFileTree(TTkTree):
    __doc__ = '''
    :py:class:`TTkFileTree` is a container widget which place :py:class:`TTkFileTreeWidget` in a scrolling area with on-demand scroll bars.

    ''' + TTkFileTreeWidget.__doc__

    __slots__ = tuple(
        ['_fileTreeWidget'] +
        (_forwardedSignals:=[# Forwarded Signals from TTkFileTreeWidget
                  *TTkTree._forwardedSignals,
                 'fileClicked', 'folderClicked', 'fileDoubleClicked', 'folderDoubleClicked', 'fileActivated', 'folderActivated']) +
        (_forwardedMethods:=[# Forwarded Methods From TTkTreeWidget
                  *TTkTree._forwardedMethods,
                 'openPath', 'getOpenPath',
                 'setFilter'])
    )
    _forwardWidget = TTkFileTreeWidget

    def __init__(self, **kwargs) -> None:
        wkwargs = kwargs.copy()
        wkwargs.pop('parent',None)
        wkwargs.pop('visible',None)
        self._fileTreeWidget = TTkFileTreeWidget(**wkwargs)

        super().__init__(**kwargs, treeWidget=self._fileTreeWidget)

        for _attr in self._forwardedSignals+self._forwardedMethods:
            setattr(self,_attr,getattr(self._fileTreeWidget,_attr))
