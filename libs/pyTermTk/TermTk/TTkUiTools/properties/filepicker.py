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

__all__ = ['TTkFileButtonPickerProperties']

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkWidgets.TTkPickers.filepicker import TTkFileButtonPicker

TTkFileButtonPickerProperties = {
    'properties' : {
        'Path' : {
                'init': {'name':'path',                    'type':str },
                'get':  {'cb':TTkFileButtonPicker.path,    'type':str } ,
                'set':  {'cb':TTkFileButtonPicker.setPath, 'type':str } },
        'Caption' : {
                'init': {'name':'caption',                    'type':str },
                'get':  {'cb':TTkFileButtonPicker.caption,    'type':str } ,
                'set':  {'cb':TTkFileButtonPicker.setCaption, 'type':str } },
        'Filters' : {
                'init': {'name':'filter',                    'type':str },
                'get':  {'cb':TTkFileButtonPicker.filter,    'type':str } ,
                'set':  {'cb':TTkFileButtonPicker.setFilter, 'type':str } },
        'Accept Mode': {
                'init': {'name':'acceptMode', 'type':'singleflag',
                    'flags': {
                        'Open'      : TTkK.AcceptMode.AcceptOpen ,
                        'Save'      : TTkK.AcceptMode.AcceptSave } },
                'get':  {'cb':TTkFileButtonPicker.acceptMode,    'type':'singleflag',
                    'flags': {
                        'Open'      : TTkK.AcceptMode.AcceptOpen ,
                        'Save'      : TTkK.AcceptMode.AcceptSave } },
                'set':  {'cb':TTkFileButtonPicker.setAcceptMode, 'type':'singleflag',
                    'flags': {
                        'Open'      : TTkK.AcceptMode.AcceptOpen ,
                        'Save'      : TTkK.AcceptMode.AcceptSave } }, },
        'File Mode' : {
                'init': {'name':'fileMode', 'type':'singleflag',
                    'flags': {
                        'Any File'      : TTkK.FileMode.AnyFile    ,
                        'Existing File' : TTkK.FileMode.ExistingFile  ,
                        'Directory'     : TTkK.FileMode.Directory } },
                'get':  {'cb':TTkFileButtonPicker.fileMode,    'type':'singleflag',
                    'flags': {
                        'Any File'      : TTkK.FileMode.AnyFile    ,
                        'Existing File' : TTkK.FileMode.ExistingFile  ,
                        'Directory'     : TTkK.FileMode.Directory } },
                'set':  {'cb':TTkFileButtonPicker.setFileMode, 'type':'singleflag',
                    'flags': {
                        'Any File'      : TTkK.FileMode.AnyFile    ,
                        'Existing File' : TTkK.FileMode.ExistingFile  ,
                        'Directory'     : TTkK.FileMode.Directory } }, }, },
    'signals' : {
        'pathPicked(str)'   : {'name' : 'pathPicked'  , 'type' : str},
        'filePicked(str)'   : {'name' : 'filePicked'  , 'type' : str},
        'folderPicked(str)' : {'name' : 'folderPicked', 'type' : str},
    },
    'slots' : {
    }
}
