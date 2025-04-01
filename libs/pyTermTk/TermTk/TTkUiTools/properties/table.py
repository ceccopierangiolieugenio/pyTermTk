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

__all__ = ['TTkTableProperties']

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkWidgets.TTkModelView.table import TTkTable
from TermTk.TTkWidgets.TTkModelView.tablewidget import TTkTableWidget, TTkHeaderView


TTkTableProperties = {
    'properties'  : {
        'H Header' : {
                'init': {'name':'hHeader',                             'type':bool } ,
                'get':  { 'cb':TTkHeaderView.isVisible,  'type':bool, 'fw_obj':lambda _obj: _obj.viewport().horizontalHeader() } ,
                'set':  { 'cb':TTkHeaderView.setVisible, 'type':bool, 'fw_obj':lambda _obj: _obj.viewport().horizontalHeader() } },
        'V Header' : {
                'init': {'name':'vHeader',                             'type':bool } ,
                'get':  { 'cb':TTkHeaderView.isVisible,  'type':bool, 'fw_obj':lambda _obj: _obj.viewport().verticalHeader() } ,
                'set':  { 'cb':TTkHeaderView.setVisible, 'type':bool, 'fw_obj':lambda _obj: _obj.viewport().verticalHeader() } },
        'H Separator' : {
                'init': {'name':'hSeparator',                          'type':bool } ,
                'get':  { 'cb':TTkTableWidget.hSeparatorVisibility,    'type':bool, 'fw_obj':TTkTable.viewport } ,
                'set':  { 'cb':TTkTableWidget.setHSeparatorVisibility, 'type':bool, 'fw_obj':TTkTable.viewport } },
        'V Separator' : {
                'init': {'name':'vSeparator',                          'type':bool } ,
                'get':  { 'cb':TTkTableWidget.vSeparatorVisibility,    'type':bool, 'fw_obj':TTkTable.viewport } ,
                'set':  { 'cb':TTkTableWidget.setVSeparatorVisibility, 'type':bool, 'fw_obj':TTkTable.viewport } },
        'Sorting' : {
                'init': {'name':'sortingEnabled',                      'type':bool } ,
                'get':  { 'cb':TTkTableWidget.isSortingEnabled,        'type':bool, 'fw_obj':TTkTable.viewport } ,
                'set':  { 'cb':TTkTableWidget.setSortingEnabled,       'type':bool, 'fw_obj':TTkTable.viewport } },
    },'signals' : {
        'cellChanged(int,int)'                : {'name' : 'cellChanged'       ,  'type':(int, int)},
        'cellClicked(int,int)'                : {'name' : 'cellClicked'       ,  'type':(int, int)},
        'cellDoubleClicked(int,int)'          : {'name' : 'cellDoubleClicked' ,  'type':(int, int)},
        'cellEntered(int,int)'                : {'name' : 'cellEntered'       ,  'type':(int, int)},
        'currentCellChanged(int,int,int,int)' : {'name' : 'currentCellChanged',  'type':(int, int, int, int)},
    },'slots' : {
        'undo()'  : {'name' : 'undo'  , 'type': None },
        'redo()'  : {'name' : 'redo'  , 'type': None },
        'copy()'  : {'name' : 'copy'  , 'type': None },
        'cut()'   : {'name' : 'cut'   , 'type': None },
        'paste()' : {'name' : 'paste' , 'type': None },

        'setSortingEnabled(bool)'     : {'name' : 'copy' , 'type':  bool },
        'sortByColumn(int,SortOrder)' : {'name' : 'copy' , 'type': (int,TTkK.SortOrder), },
        'setColumnWidth(int,int)'     : {'name' : 'copy' , 'type': (int,int) },
        'resizeColumnToContents(int)' : {'name' : 'copy' , 'type':  int },
        'resizeColumnsToContents()'   : {'name' : 'copy' , 'type':  None },
        'setRowHeight(int,int)'       : {'name' : 'copy' , 'type': (int,int) },
        'resizeRowToContents(int)'    : {'name' : 'copy' , 'type':  int },
        'resizeRowsToContents()'      : {'name' : 'copy' , 'type':  None },
    }
}
