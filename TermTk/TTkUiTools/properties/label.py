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

__all__ = ['TTkLabelProperties']

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.string import TTkString
from TermTk.TTkWidgets.label import TTkLabel

TTkLabelProperties = {
    'properties' : {
        'Text' : {
                'init': {'name':'text',         'type':TTkString },
                'get':  {'cb':TTkLabel.text,    'type':TTkString } ,
                'set':  {'cb':TTkLabel.setText, 'type':TTkString } },
        'Color' : {
                'init': {'name':'color',         'type':TTkColor },
                'get':  {'cb':TTkLabel.color,    'type':TTkColor } ,
                'set':  {'cb':TTkLabel.setColor, 'type':TTkColor } },
        'Alignment': {
                'init': {'name':'alignment',        'type':'singleflag',
                    'flags': {
                        'None'    : TTkK.NONE         ,
                        'Left'    : TTkK.LEFT_ALIGN   ,
                        'Right'   : TTkK.RIGHT_ALIGN  ,
                        'Center'  : TTkK.CENTER_ALIGN ,
                        'Justify' : TTkK.JUSTIFY      } } ,
                'get':  {'cb':TTkLabel.alignment,   'type':'singleflag',
                    'flags': {
                        'None'    : TTkK.NONE         ,
                        'Left'    : TTkK.LEFT_ALIGN   ,
                        'Right'   : TTkK.RIGHT_ALIGN  ,
                        'Center'  : TTkK.CENTER_ALIGN ,
                        'Justify' : TTkK.JUSTIFY      } },
                'set':  {'cb':TTkLabel.setAlignment,'type':'singleflag',
                    'flags': {
                        'None'    : TTkK.NONE         ,
                        'Left'    : TTkK.LEFT_ALIGN   ,
                        'Right'   : TTkK.RIGHT_ALIGN  ,
                        'Center'  : TTkK.CENTER_ALIGN ,
                        'Justify' : TTkK.JUSTIFY      } } },
    },'signals' : {
    },'slots' : {
        'setText(str)'            : {'name': 'setText',      'type':str},
        'setAlignment(Alignment)' : {'name': 'setAlignment', 'type':TTkK.Alignment},
    }
}
