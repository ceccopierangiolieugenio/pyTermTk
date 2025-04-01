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

__all__ = ['TTkColorButtonPickerProperties']

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkWidgets.TTkPickers.colorpicker import TTkColorButtonPicker,TTkColorDialogPicker

TTkColorButtonPickerProperties = {
    'properties' : {
        'Color' : {
                'init': {'name':'color',                     'type':TTkColor },
                'get':  {'cb':TTkColorButtonPicker.color,    'type':TTkColor } ,
                'set':  {'cb':TTkColorButtonPicker.setColor, 'type':TTkColor } },
        'Return Type' : {
                'init': {'name':'returnType',                     'type':'singleflag',
                    'flags': {
                        'Default'    : TTkK.ColorPickerReturnType.Default    ,
                        'Foreground' : TTkK.ColorPickerReturnType.Foreground ,
                        'Background' : TTkK.ColorPickerReturnType.Background } },
                'get':  {'cb':TTkColorButtonPicker.returnType,    'type':'singleflag',
                    'flags': {
                        'Default'    : TTkK.ColorPickerReturnType.Default    ,
                        'Foreground' : TTkK.ColorPickerReturnType.Foreground ,
                        'Background' : TTkK.ColorPickerReturnType.Background } } ,
                'set':  {'cb':TTkColorButtonPicker.setReturnType, 'type':'singleflag',
                    'flags': {
                        'Default'    : TTkK.ColorPickerReturnType.Default    ,
                        'Foreground' : TTkK.ColorPickerReturnType.Foreground ,
                        'Background' : TTkK.ColorPickerReturnType.Background } } } },
    'signals' : {
        'colorSelected(TTkColor)'   : {'name': 'colorSelected',   'type' : TTkColor},
        'colorSelectedFG(TTkColor)' : {'name': 'colorSelectedFG', 'type' : TTkColor},
        'colorSelectedBG(TTkColor)' : {'name': 'colorSelectedBG', 'type' : TTkColor},
    },
    'slots' : {
        'setColor(TTkColor)' : {'name': 'setColor', 'type' : TTkColor},
    }
}
