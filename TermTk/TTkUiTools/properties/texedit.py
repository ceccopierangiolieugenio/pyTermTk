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

__all__ = ['TTkTextEditProperties']

# from TermTk.TTkCore.string import TTkString
# from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkWidgets.texedit import TTkTextEdit

TTkTextEditProperties = {
    'properties' : {
        'Line Number': {
                'init': {'name':'lineNumber',            'type':bool } ,
                'get':  {'cb':TTkTextEdit.getLineNumber, 'type':bool } ,
                'set':  {'cb':TTkTextEdit.setLineNumber, 'type':bool } },
        'Line Number Starting': {
                'init': {'name':'lineNumberStarting',            'type':int } ,
                'get':  {'cb':TTkTextEdit.lineNumberStarting,    'type':int } ,
                'set':  {'cb':TTkTextEdit.setLineNumberStarting, 'type':int } },
        'Read Only' : {
                'init': {'name':'readOnly',                'type':bool } ,
                'get':  {'cb':lambda w:   w.isReadOnly(),  'type':bool } ,
                'set':  {'cb':lambda w,v: w.setReadOnly(v),'type':bool } },
        'Multi Line' : {
                'init': {'name':'multiLine',           'type':bool } ,
                'get':  {'cb':lambda w: w.multiLine(), 'type':bool } },
    },'signals' : {
        'currentColorChanged(TTkColor)' : {'name': 'currentColorChanged', 'type':TTkColor},
        'undoAvailable(bool)' : {'name': 'undoAvailable', 'type': bool},
        'redoAvailable(bool)' : {'name': 'redoAvailable', 'type': bool},
        'textChanged()' :       {'name': 'textChanged',   'type': None},
    },'slots' : {
        'setText(str)' : {'name':'setText', 'type':None},
        'setColor(TTkColor)'         : {'name':'setColor', 'type':TTkColor},
        'setLineNumber(bool)'        : {'name':'setLineNumber',         'type':bool},
        'setLineNumberStarting(int)' : {'name':'setLineNumberStarting', 'type':int},
        'append(str)' :  {'name':'append',  'type':None},
        'undo()' :       {'name':'undo',    'type':None},
        'redo()' :       {'name':'redo',    'type':None},
        'clear()' :      {'name':'clear',   'type':None},
        'copy()' :       {'name':'copy',    'type':None},
        'cut()' :        {'name':'cut',     'type':None},
        'paste()' :      {'name':'paste',   'type':None},
    }
}