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

__all__ = ['TTkSpinBoxProperties']

from TermTk.TTkWidgets.spinbox import TTkSpinBox

TTkSpinBoxProperties = {
    'properties' : {
        'Value' : {
                'init': {'name':'value',            'type':int } ,
                'get':  { 'cb':TTkSpinBox.value,    'type':int } ,
                'set':  { 'cb':TTkSpinBox.setValue, 'type':int } },
        'Minimum' : {
                'init': {'name':'minimum',            'type':int } ,
                'get':  { 'cb':TTkSpinBox.minimum,    'type':int } ,
                'set':  { 'cb':TTkSpinBox.setMinimum, 'type':int } },
        'Maximum' : {
                'init': {'name':'maximum',            'type':int } ,
                'get':  { 'cb':TTkSpinBox.maximum,    'type':int } ,
                'set':  { 'cb':TTkSpinBox.setMaximum, 'type':int } },
    },'signals' : {
        'valueChanged(int)' : {'name' : 'valueChanged', 'type': int },
    },'slots' : {
        'setValue(int)'   : {'name' : 'setValue'   , 'type': int },
        'setMinimum(int)' : {'name' : 'setMinimum' , 'type': int },
        'setMaximum(int)' : {'name' : 'setMaximum' , 'type': int },
    }
}
