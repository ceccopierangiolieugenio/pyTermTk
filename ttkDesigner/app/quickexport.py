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

import TermTk as ttk

class QuickExport(ttk.TTkWindow):
    __slots__ = ('_data', '_te')
    def __init__(self, data, *args, **kwargs):
        self._data = data
        super().__init__(*args, **kwargs|{'layout':ttk.TTkGridLayout()})
        self.layout().addWidget(btnCompressed := ttk.TTkButton(text='Compressed', border=True, maxHeight=3), 0,1)
        self.layout().addWidget(btnNormal     := ttk.TTkButton(text='Normal', border=True, maxHeight=3), 0,0)
        self._te = ttk.TTkTextEdit(lineNumber=True, readOnly=False)
        self.layout().addWidget(self._te, 1,0,1,2)

        btnNormal.clicked.connect(self.useNormmal)
        btnCompressed.clicked.connect(self.useCompressed)

        self.useCompressed()

    ttk.pyTTkSlot()
    def useNormmal(self):
        self._te.setLineWrapMode(ttk.TTkK.WidgetWidth)
        self._te.setWordWrapMode(ttk.TTkK.WordWrap)
        self._te.setText('from TermTk import TTkUtil, TTkUiLoader, TTk\n')
        self._te.append(f'# Data generated using ttkDesigner')
        self._te.append('widget = TTkUiLoader.loadDict(')
        self._te.append(str(self._data)+ '")')
        self._te.append('\nroot=TTk()\nroot.layout().addWidget(widget)\nroot.mainloop()\n')

    ttk.pyTTkSlot()
    def useCompressed(self):
        self._te.setLineWrapMode(ttk.TTkK.NoWrap)
        b64str = ttk.TTkUtil.obj_inflate_2_base64(self._data)
        self._te.setText('from TermTk import TTkUtil, TTkUiLoader, TTk\n')
        self._te.append(f'# Data generated using ttkDesigner')
        self._te.append('widget = TTkUiLoader.loadDict(TTkUtil.base64_deflate_2_obj(')
        b64list = '    "' + '" +\n    "'.join([b64str[i:i+128] for i in range(0,len(b64str),128)]) + '"))'
        self._te.append(b64list)
        self._te.append('\nroot=TTk()\nroot.layout().addWidget(widget)\nroot.mainloop()\n')

