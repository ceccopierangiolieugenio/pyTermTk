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

__all__ = ['TTkCheckboxProperties']

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.string import TTkString
from TermTk.TTkWidgets.checkbox import TTkCheckbox

TTkCheckboxProperties = {
    'properties' : {
       'Text' : {
                'init': {'name':'text', 'type':'singleLineTTkString' } ,
                'get':  {'cb':TTkCheckbox.text,     'type':'singleLineTTkString' } ,
                'set':  {'cb':TTkCheckbox.setText,  'type':'singleLineTTkString' } },
        'Tristate' : {
                'init': {'name':'tristate', 'type':bool } ,
                'get':  {'cb':TTkCheckbox.isTristate,   'type':bool } ,
                'set':  {'cb':TTkCheckbox.setTristate,  'type':bool } },
        'Checked' : {
                'init': {'name':'checked', 'type':bool } ,
                'get':  {'cb':TTkCheckbox.isChecked,   'type':bool } ,
                'set':  {'cb':TTkCheckbox.setChecked,  'type':bool } },
        'Check State' : {
                'init': { 'name':'checked', 'type':'singleflag',
                    'flags': {
                        'Checked'          : TTkK.Checked    ,
                        'Unchecked'        : TTkK.Unchecked  ,
                        'Partially Checked': TTkK.PartiallyChecked } },
                'get' : { 'cb':TTkCheckbox.checkState,      'type':'singleflag',
                    'flags': {
                        'Checked'          : TTkK.Checked    ,
                        'Unchecked'        : TTkK.Unchecked  ,
                        'Partially Checked': TTkK.PartiallyChecked } },
                'set' : { 'cb':TTkCheckbox.setCheckState,   'type':'singleflag',
                    'flags': {
                        'Checked'          : TTkK.Checked    ,
                        'Unchecked'        : TTkK.Unchecked  ,
                        'Partially Checked': TTkK.PartiallyChecked } },
         },
    },
    'signals' : {
        'clicked(bool)' :            {'name' : 'clicked',      'type' : bool},
        'toggled(bool)' :            {'name' : 'toggled',      'type' : bool},
        'stateChanged(CheckState)' : {'name' : 'stateChanged', 'type' : TTkK.CheckState},
    },
    'slots' : {
        'setChecked(bool)' :          {'name' : 'setChecked'    , 'type' : bool},
        'setCheckState(CheckState)' : {'name' : 'setCheckState' , 'type' : TTkK.CheckState},
        'setText(str)' :              {'name' : 'setText'       , 'type' : str}
    }
}
