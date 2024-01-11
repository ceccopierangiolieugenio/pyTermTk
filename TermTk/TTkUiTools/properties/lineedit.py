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

__all__ = ['TTkLineEditProperties']

from TermTk.TTkCore.string import TTkString
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkWidgets.lineedit import TTkLineEdit

TTkLineEditProperties = {
    'properties' : {
        'Input Type' : {
                'init': {'name':'inputType', 'type':'singleflag',
                    'flags': {
                        'Text'    : TTkK.Input_Text   ,
                        'Number'  : TTkK.Input_Number } },
                'get': {'cb':TTkLineEdit.inputType,      'type':'singleflag',
                    'flags': {
                        'Text'    : TTkK.Input_Text   ,
                        'Number'  : TTkK.Input_Number } },
                'set': {'cb':TTkLineEdit.setInputType,   'type':'singleflag',
                    'flags': {
                        'Text'    : TTkK.Input_Text   ,
                        'Number'  : TTkK.Input_Number } } },
        'Echo Mode' : {
                'init': {'name':'echoMode', 'type':'singleflag',
                    'flags': {
                        'Normal'      : TTkLineEdit.EchoMode.Normal ,
                        'No Echo'     : TTkLineEdit.EchoMode.NoEcho ,
                        'Password'    : TTkLineEdit.EchoMode.Password ,
                        'Password, Echo on Edit' : TTkLineEdit.EchoMode.PasswordEchoOnEdit } },
                'get': {'cb':TTkLineEdit.echoMode,      'type':'singleflag',
                    'flags': {
                        'Normal'      : TTkLineEdit.EchoMode.Normal ,
                        'No Echo'     : TTkLineEdit.EchoMode.NoEcho ,
                        'Password'    : TTkLineEdit.EchoMode.Password ,
                        'Password, Echo on Edit' : TTkLineEdit.EchoMode.PasswordEchoOnEdit } },
                'set': {'cb':TTkLineEdit.setEchoMode,   'type':'singleflag',
                    'flags': {
                        'Normal'      : TTkLineEdit.EchoMode.Normal ,
                        'No Echo'     : TTkLineEdit.EchoMode.NoEcho ,
                        'Password'    : TTkLineEdit.EchoMode.Password ,
                        'Password, Echo on Edit' : TTkLineEdit.EchoMode.PasswordEchoOnEdit } } },
        'Text' : {
                'init': {'name':'text', 'type':'singleLineTTkString',  } ,
                'get':  {'cb':TTkLineEdit.text,     'type':'singleLineTTkString' } ,
                'set':  {'cb':TTkLineEdit.setText,  'type':'singleLineTTkString' } }
    },'signals' : {
        'textChanged(str)' : {'name': 'textChanged',   'type': str},
        'textEdited(str)'  : {'name': 'textEdited',    'type': str},
        'returnPressed()'  : {'name': 'returnPressed', 'type': None},
    },'slots' : {
        'setText(str)' : {'name':'setText', 'type':None},
    }
}
