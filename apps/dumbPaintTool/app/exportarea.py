# MIT License
#
# Copyright (c) 2024 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

__all__ = ['ExportArea']

import TermTk as ttk

from .paintarea    import PaintArea

class ExportArea(ttk.TTkGridLayout):
    __slots__ = ('_paintArea', '_te','_cbCrop', '_cbFull', '_cbPal')
    def __init__(self, paintArea:PaintArea, **kwargs):
        self._paintArea:PaintArea = paintArea
        super().__init__(**kwargs)
        self._te = ttk.TTkTextEdit(lineNumber=True, readOnly=False)
        btn_exIm   = ttk.TTkButton(text="Export Image")
        btn_exLa   = ttk.TTkButton(text="Export Layer")
        btn_exPr   = ttk.TTkButton(text="Export Document")
        self._cbCrop = ttk.TTkCheckbox(text="Crop",checked=True)
        self._cbFull = ttk.TTkCheckbox(text="Full",checked=True)
        self._cbPal  = ttk.TTkCheckbox(text="Palette",checked=True)
        self.addWidget(btn_exLa  ,0,0)
        self.addWidget(btn_exIm  ,0,1)
        self.addWidget(btn_exPr  ,0,2)
        self.addWidget(self._cbCrop,0,3)
        self.addWidget(self._cbFull,0,4)
        self.addWidget(self._cbPal ,0,5)
        self.addWidget(self._te,1,0,1,7)

        btn_exLa.clicked.connect(self._exportLayer)
        btn_exPr.clicked.connect(self._exportDocument)
        btn_exIm.clicked.connect(self._exportImage)

    @ttk.pyTTkSlot()
    def _exportImage(self):
        import base64, gzip
        crop    = self._cbCrop.isChecked()
        palette = self._cbPal.isChecked()
        full    = self._cbFull.isChecked()
        image = self._paintArea.exportImage()
        # trim the lines
        imagexxx = [line.rstrip() for line in image.split("\n")]
        image = "\n".join(imagexxx)
        self._te.setText(image)

        self._te.append("\n")
        self._te.append(ttk.TTkString("# Python Code",ttk.TTkColor.GREEN))
        lines = [f'     "{line}\\n"' for line in image.replace("\033","\\033").split('\n')]
        mergedLines = "\n".join(lines)
        self._te.append(f"image = (\n{mergedLines})")
        self._te.append('print(image)')

        self._te.append("\n")
        self._te.append(ttk.TTkString("# Python Code using pyTermTk archive",ttk.TTkColor.GREEN))
        self._te.append('from TermTk import TTkUtil\n')
        self._te.append('image = TTkUtil.base64_deflate_2_obj(')
        b64str = ttk.TTkUtil.obj_inflate_2_base64(image)
        b64list = '    "' + '" +\n    "'.join([b64str[i:i+128] for i in range(0,len(b64str),128)]) + '")'
        self._te.append(b64list)
        self._te.append('print(image)')

        self._te.append("\n")
        self._te.append(ttk.TTkString("# Python Code using standard archive libs",ttk.TTkColor.GREEN))
        b64str = base64.b64encode(gzip.compress(bytearray(image,encoding='utf8'))).decode("ascii")
        self._te.append('import zlib, pickle, base64\n')
        self._te.append('image = pickle.loads(zlib.decompress(base64.b64decode((')
        b64str = ttk.TTkUtil.obj_inflate_2_base64(image)
        b64list = '    "' + '" +\n    "'.join([b64str[i:i+128] for i in range(0,len(b64str),128)]) + '").encode("ascii"))))'
        self._te.append(b64list)
        self._te.append('print(image)')

        self._te.append("\n")
        self._te.append(ttk.TTkString("# Bash Code",ttk.TTkColor.GREEN))
        lines = [f'echo -e "{line}"' for line in image.replace("\033","\\033").split('\n')]
        mergedLines = "\n".join(lines)
        self._te.append(mergedLines)

        self._te.append("\n")
        self._te.append(ttk.TTkString("# Bash Code Compressed",ttk.TTkColor.GREEN))
        b64str = base64.b64encode(gzip.compress(bytearray(image,encoding='utf8'))).decode("ascii")
        b64list = "\n".join([b64str[i:i+128] for i in range(0,len(b64str),128)])
        self._te.append(f'echo "{b64list}" | base64 -d | zcat\n')

    @ttk.pyTTkSlot()
    def _exportLayer(self):
        crop    = self._cbCrop.isChecked()
        palette = self._cbPal.isChecked()
        full    = self._cbFull.isChecked()
        dd = self._paintArea.exportLayer(full=full,palette=palette,crop=crop)
        if not dd:
            self._te.setText('# No Data toi be saved!!!')
            return

        self._te.setText('# Compressed Data:')
        self._te.append('data = TTkUtil.base64_deflate_2_obj(')
        b64str = ttk.TTkUtil.obj_inflate_2_base64(dd)
        b64list = '    "' + '" +\n    "'.join([b64str[i:i+128] for i in range(0,len(b64str),128)]) + '")'
        self._te.append(b64list)

        self._te.append('\n# Uncompressed Data:')
        outTxt = '{\n'
        for i in dd:
            if i in ('data','colors','palette'): continue
            if type(dd[i]) == str:
                outTxt += f"  '{i}':'{dd[i]}',\n"
            else:
                outTxt += f"  '{i}':{dd[i]},\n"
        outTxt += "    'data':[\n"
        for l in dd['data']:
            outTxt += f"    {l},\n"
        outTxt += "  ],'colors':[\n"
        for l in dd['colors']:
            outTxt += f"    {l},\n"
        if 'palette' in dd:
            outTxt += "  ],'palette':["
            for i,l in enumerate(dd['palette']):
                if not i%10:
                    outTxt += f"\n    "
                outTxt += f"{l},"
        outTxt += "]}\n"
        self._te.append(outTxt)

    @ttk.pyTTkSlot()
    def _exportDocument(self):
        crop    = self._cbCrop.isChecked()
        palette = self._cbPal.isChecked()
        full    = self._cbFull.isChecked()
        dd = self._paintArea.exportDocument(full=full,palette=palette,crop=crop)
        if not dd:
            self._te.setText('# No Data to be saved!!!')
            return

        self._te.setText('# Compressed Data:')
        self._te.append('data = TTkUtil.base64_deflate_2_obj(')
        b64str = ttk.TTkUtil.obj_inflate_2_base64(dd)
        b64list = '    "' + '" +\n    "'.join([b64str[i:i+128] for i in range(0,len(b64str),128)]) + '")'
        self._te.append(b64list)

        self._te.append('\n# Uncompressed Data:')
        outTxt = '{\n'
        for i in dd:
            if i=='layers': continue
            if type(dd[i]) == str:
                outTxt += f"  '{i}':'{dd[i]}',\n"
            else:
                outTxt += f"  '{i}':{dd[i]},\n"
        outTxt +=  "  'layers':[\n"
        for l in dd['layers']:
            outTxt += f"    {l},\n"
        outTxt += "]}\n"
        self._te.append(outTxt)