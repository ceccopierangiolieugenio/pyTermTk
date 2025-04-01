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

__all__ = ['TTkListProperties']

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkWidgets.list_ import TTkList
from TermTk.TTkWidgets.listwidget import TTkListWidget, TTkAbstractListItem


TTkListProperties = {
    'properties' : {
        'Selection Mode' : {
            'init': {'name':'selectionMode', 'type':'singleflag',
                     'flags':{
                         'Single Seelction' : TTkK.SingleSelection,
                         'Multi Selection'  : TTkK.MultiSelection,
                     }},
            'get': {'cb':lambda w: w.selectionMode(), 'type':'singleflag',
                     'flags':{
                         'Single Seelction' : TTkK.SingleSelection,
                         'Multi Selection'  : TTkK.MultiSelection,
                     }},
            'set': {'cb':lambda w,v: w.setSelectionMode(v), 'type':'singleflag',
                     'flags':{
                         'Single Seelction' : TTkK.SingleSelection,
                         'Multi Selection'  : TTkK.MultiSelection,
                     }}},
        'DnD Mode' : {
            'init': {'name':'dragDropMode', 'type':'multiflags',
                     'flags':{
                         'Allow Drag' : TTkK.DragDropMode.AllowDrag,
                         'Allow Drop' : TTkK.DragDropMode.AllowDrop,
                     }},
            'get': {'cb':lambda w: w.dragDropMode(), 'type':'multiflags',
                     'flags':{
                         'Allow Drag' : TTkK.DragDropMode.AllowDrag,
                         'Allow Drop' : TTkK.DragDropMode.AllowDrop,
                     }},
            'set': {'cb':lambda w,v: w.setDragDropMode(v), 'type':'multiflags',
                     'flags':{
                         'Allow Drag' : TTkK.DragDropMode.AllowDrag,
                         'Allow Drop' : TTkK.DragDropMode.AllowDrop,
                     }}},
    },
    'signals' : {
        'itemClicked(TTkAbstractListItem)' : {'name': 'itemClicked', 'type' : TTkAbstractListItem},
        'textClicked(str)' :                 {'name': 'textClicked', 'type' : str},
    },
    'slots' : {}}