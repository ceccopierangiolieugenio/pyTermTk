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

__all__ = ['TTkComboBoxProperties']

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.string import TTkString
from TermTk.TTkWidgets.combobox import TTkComboBox

TTkComboBoxProperties = {
    'properties' : {
        'Editable' : {
                'init': {'name':'editable', 'type':bool } ,
                'get':  {'cb':TTkComboBox.isEditable,   'type':bool } ,
                'set':  {'cb':TTkComboBox.setEditable,  'type':bool } },
        'Text Align.' : {
                'init': {'name':'textAlign', 'type':'singleflag',
                    'flags': {
                        'None'   : TTkK.Alignment.NONE,
                        'Left'   : TTkK.Alignment.LEFT_ALIGN,
                        'Right'  : TTkK.Alignment.RIGHT_ALIGN,
                        'Center' : TTkK.Alignment.CENTER_ALIGN,
                        'Justify': TTkK.Alignment.JUSTIFY } },
                'get':  {'cb':TTkComboBox.textAlign,    'type':'singleflag',
                    'flags': {
                        'None'   : TTkK.Alignment.NONE,
                        'Left'   : TTkK.Alignment.LEFT_ALIGN,
                        'Right'  : TTkK.Alignment.RIGHT_ALIGN,
                        'Center' : TTkK.Alignment.CENTER_ALIGN,
                        'Justify': TTkK.Alignment.JUSTIFY } } ,
                'set':  {'cb':TTkComboBox.setTextAlign, 'type':'singleflag',
                    'flags': {
                        'None'   : TTkK.Alignment.NONE,
                        'Left'   : TTkK.Alignment.LEFT_ALIGN,
                        'Right'  : TTkK.Alignment.RIGHT_ALIGN,
                        'Center' : TTkK.Alignment.CENTER_ALIGN,
                        'Justify': TTkK.Alignment.JUSTIFY } } },
        'Insert Policy' : {
                'init': {'name':'insertPolicy', 'type':'singleflag',
                    'flags': {
                        'No Insert'   : TTkK.InsertPolicy.NoInsert,
                        'At Top'      : TTkK.InsertPolicy.InsertAtTop,
                        'At Bottom'   : TTkK.InsertPolicy.InsertAtBottom } },
                'get':  {'cb':TTkComboBox.insertPolicy,    'type':'singleflag',
                    'flags': {
                        'No Insert'   : TTkK.InsertPolicy.NoInsert,
                        'At Top'      : TTkK.InsertPolicy.InsertAtTop,
                        'At Bottom'   : TTkK.InsertPolicy.InsertAtBottom } },
                'set':  {'cb':TTkComboBox.setInsertPolicy, 'type':'singleflag',
                    'flags': {
                        'No Insert'   : TTkK.InsertPolicy.NoInsert,
                        'At Top'      : TTkK.InsertPolicy.InsertAtTop,
                        'At Bottom'   : TTkK.InsertPolicy.InsertAtBottom } } },
    },'signals' : {},'slots' : {}
}
