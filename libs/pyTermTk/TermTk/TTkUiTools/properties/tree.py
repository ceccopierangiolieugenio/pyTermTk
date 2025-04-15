# MIT License
#
# Copyright (c) 2024 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

__all__ = ['TTkTreeProperties']

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkWidgets.TTkModelView.tree import TTkTree
from TermTk.TTkWidgets.TTkModelView.treewidget import TTkTreeWidget
from TermTk.TTkWidgets.TTkModelView.treewidgetitem import TTkTreeWidgetItem

TTkTreeProperties = {
    'properties'  : {
        'Sorting' : {
                'init': {'name':'sortingEnabled',                     'type':bool } ,
                'get':  { 'cb':TTkTreeWidget.isSortingEnabled,        'type':bool, 'fw_obj':TTkTree.viewport } ,
                'set':  { 'cb':TTkTreeWidget.setSortingEnabled,       'type':bool, 'fw_obj':TTkTree.viewport } },
    },'signals' : {
        'itemActivated(TTkTreeWidgetItem,int)'     : {'name' : 'itemActivated'     ,  'type':(TTkTreeWidgetItem,int)},
        'itemChanged(TTkTreeWidgetItem,int)'       : {'name' : 'itemChanged'       ,  'type':(TTkTreeWidgetItem,int)},
        'itemClicked(TTkTreeWidgetItem,int)'       : {'name' : 'itemClicked'       ,  'type':(TTkTreeWidgetItem,int)},
        'itemDoubleClicked(TTkTreeWidgetItem,int)' : {'name' : 'itemDoubleClicked' ,  'type':(TTkTreeWidgetItem,int)},
        'itemExpanded(TTkTreeWidgetItem)'          : {'name' : 'itemExpanded'      ,  'type': TTkTreeWidgetItem},
        'itemCollapsed(TTkTreeWidgetItem)'         : {'name' : 'itemCollapsed'     ,  'type': TTkTreeWidgetItem},
    },'slots' : {
        'expandAll()'   : {'name': 'expandAll',   'type':None},
        'collapseAll()' : {'name': 'collapseAll', 'type':None},
    }
}
