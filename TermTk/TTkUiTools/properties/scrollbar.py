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

__all__ = ['TTkScrollBarProperties']

from TermTk.TTkCore.string import TTkString
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkWidgets.scrollbar import TTkScrollBar

TTkScrollBarProperties = {
    'properties' : {
        'Orientation' : {
                'init': {'name':'orientation', 'type':'singleflag',
                    'flags': {
                        'Horizontal' : TTkK.HORIZONTAL ,
                        'Vertical'   : TTkK.VERTICAL   } } ,
                'get':  {'cb':TTkScrollBar.orientation,     'type':'singleflag',
                    'flags': {
                        'Horizontal' : TTkK.HORIZONTAL ,
                        'Vertical'   : TTkK.VERTICAL   } } },
        'Value' : {
                'init': {'name':'value',              'type':int } ,
                'get':  { 'cb':TTkScrollBar.value,    'type':int } ,
                'set':  { 'cb':TTkScrollBar.setValue, 'type':int } },
        'Minimum' : {
                'init': {'name':'minimum',              'type':int } ,
                'get':  { 'cb':TTkScrollBar.minimum,    'type':int } ,
                'set':  { 'cb':TTkScrollBar.setMinimum, 'type':int } },
        'Maximum' : {
                'init': {'name':'maximum',              'type':int } ,
                'get':  { 'cb':TTkScrollBar.maximum,    'type':int } ,
                'set':  { 'cb':TTkScrollBar.setMaximum, 'type':int } },
        'Single Step' : {
                'init': {'name':'singleStep',              'type':int } ,
                'get':  { 'cb':TTkScrollBar.singleStep,    'type':int } ,
                'set':  { 'cb':TTkScrollBar.setSingleStep, 'type':int } },
        'Page Step' : {
                'init': {'name':'pageStep',              'type':int } ,
                'get':  { 'cb':TTkScrollBar.pageStep,    'type':int } ,
                'set':  { 'cb':TTkScrollBar.setPageStep, 'type':int } },
    },'signals' : {
        'valueChanged(int)'     : {'name' : 'valueChanged', 'type': int },
        'rangeChanged(int,int)' : {'name' : 'rangeChanged', 'type':(int,int)},
        'sliderMoved(int)'      : {'name' : 'sliderMoved' , 'type': int },
    },'slots' : {
        'setValue(int)'      : {'name' : 'setValue'      , 'type': int },
        'setSingleStep(int)' : {'name' : 'setSingleStep' , 'type': int },
        'setPageStep(int)'   : {'name' : 'setPageStep'   , 'type': int },
        'setRangeTo(int)'    : {'name' : 'setRangeTo'    , 'type': int },
        'setRange(int,int)'  : {'name' : 'setRange'      , 'type':(int,int)},
    }
}