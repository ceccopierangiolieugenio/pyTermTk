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

__all__ = ['PaintTemplate']

import sys, os

sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk

from .paintarea import PaintArea, PaintToolKit
from .palette   import Palette
from .textarea  import TextArea
from .layers    import Layers

class LeftPanel(ttk.TTkVBoxLayout):
    __slots__ = ('_palette',
                 # Signals
                 'toolSelected')
    def __init__(self, *args, **kwargs):
        self.toolSelected = ttk.pyTTkSignal(PaintArea.Tool)
        super().__init__(*args, **kwargs)
        self._palette  = Palette(maxHeight=12)
        self.addWidget(self._palette)

        # Layout for the toggle buttons
        lToggleFgBg = ttk.TTkHBoxLayout()
        cb_p_fg = ttk.TTkCheckbox(text="-FG-", checked=ttk.TTkK.Checked)
        cb_p_bg = ttk.TTkCheckbox(text="-BG-", checked=ttk.TTkK.Checked)
        lToggleFgBg.addWidgets([cb_p_fg,cb_p_bg])
        lToggleFgBg.addItem(ttk.TTkLayout())
        cb_p_fg.toggled.connect(self._palette.enableFg)
        cb_p_bg.toggled.connect(self._palette.enableBg)
        self.addItem(lToggleFgBg)

        # Toolset
        lTools = ttk.TTkGridLayout()
        ra_move   = ttk.TTkRadioButton(radiogroup="tools", text="Move",  enabled=True)
        ra_select = ttk.TTkRadioButton(radiogroup="tools", text="Select",enabled=False)
        ra_brush  = ttk.TTkRadioButton(radiogroup="tools", text="Brush", checked=True)
        ra_line   = ttk.TTkRadioButton(radiogroup="tools", text="Line",  enabled=False)
        ra_rect   = ttk.TTkRadioButton(radiogroup="tools", text="Rect")
        ra_oval   = ttk.TTkRadioButton(radiogroup="tools", text="Oval",  enabled=False)

        ra_rect_f = ttk.TTkRadioButton(radiogroup="toolsRectFill", text="Fill" , enabled=False, checked=True)
        ra_rect_e = ttk.TTkRadioButton(radiogroup="toolsRectFill", text="Empty", enabled=False)

        @ttk.pyTTkSlot(bool)
        def _emitTool(checked):
            if not checked: return
            tool = PaintArea.Tool.BRUSH
            if ra_brush.isChecked():
                tool = PaintArea.Tool.BRUSH
            elif ra_rect.isChecked():
                if ra_rect_e.isChecked():
                    tool = PaintArea.Tool.RECTEMPTY
                else:
                    tool = PaintArea.Tool.RECTFILL
            self.toolSelected.emit(tool)

        ra_rect.toggled.connect(ra_rect_f.setEnabled)
        ra_rect.toggled.connect(ra_rect_e.setEnabled)

        ra_brush.toggled.connect(  _emitTool)
        ra_line.toggled.connect(   _emitTool)
        ra_rect.toggled.connect(   _emitTool)
        ra_rect_f.toggled.connect( _emitTool)
        ra_rect_e.toggled.connect( _emitTool)
        ra_oval.toggled.connect(   _emitTool)

        lTools.addWidget(ra_move  ,0,0)
        lTools.addWidget(ra_select,1,0)
        lTools.addWidget(ra_brush ,2,0)
        lTools.addWidget(ra_line  ,3,0)
        lTools.addWidget(ra_rect  ,4,0)
        lTools.addWidget(ra_rect_f,4,1)
        lTools.addWidget(ra_rect_e,4,2)
        lTools.addWidget(ra_oval  ,5,0)
        self.addItem(lTools)

        # brush
        # line
        # rettangle [empty,fill]
        # oval [empty,fill]
        self.addItem(ttk.TTkLayout())



    def palette(self):
        return self._palette

class ExportArea(ttk.TTkGridLayout):
    __slots__ = ('_paintArea', '_te')
    def __init__(self, paintArea, **kwargs):
        self._paintArea = paintArea
        super().__init__(**kwargs)
        self._te = ttk.TTkTextEdit(lineNumber=True, readOnly=False)
        btn_exIm   = ttk.TTkButton(text="Export Image")
        btn_exLa   = ttk.TTkButton(text="Export Layer")
        btn_exPr   = ttk.TTkButton(text="Export Document")
        btn_cbCrop = ttk.TTkCheckbox(text="Crop",checked=True)
        self.addWidget(btn_exLa  ,0,0)
        self.addWidget(btn_exIm  ,0,1)
        self.addWidget(btn_exPr  ,0,2)
        self.addWidget(btn_cbCrop,0,3)
        self.addWidget(self._te,1,0,1,5)

        btn_exLa.clicked.connect(self._exportLayer)

    @ttk.pyTTkSlot()
    def _exportLayer(self):
        # Don't try this at home
        pw,ph  = self._paintArea._canvasSize
        data   = self._paintArea._canvasArea['data']
        colors = self._paintArea._canvasArea['colors']
        # get the bounding box
        xa,xb,ya,yb = pw,0,ph,0
        for y,row in enumerate(data):
            for x,d in enumerate(row):
                c = colors[y][x]
                if d != ' ' or c.background():
                    xa = min(x,xa)
                    xb = max(x,xb)
                    ya = min(y,ya)
                    yb = max(y,yb)

        if xa>xb or ya>yb:
            self._te.setText("No Picture Found!!!")
            return

        out      = "data = {'data': [\n"
        outData  = {'data':[], 'colors':[]}
        for row in data[ya:yb+1]:
            out += "        ["
            outData['data'].append(row[xa:xb+1])
            for c in row[xa:xb+1]:
                out += f"'{c}',"
            out += "],\n"
        out     += "          ],\n"
        out     += "        'colors': [\n"
        for row in colors[ya:yb+1]:
            out += "        ["
            outData['colors'].append([])
            for c in row[xa:xb+1]:
                fg = f"{c.getHex(ttk.TTkK.Foreground)}" if c.foreground() else None
                bg = f"{c.getHex(ttk.TTkK.Background)}" if c.background() else None
                out += f"('{fg}','{bg}'),"
                outData['colors'][-1].append((fg,bg))
            out += "],\n"
        out     += "          ]}\n"

        self._te.setText(out)

        self._te.append('\n# Compressed Data:')
        self._te.append('data = TTkUtil.base64_deflate_2_obj(')
        b64str = ttk.TTkUtil.obj_inflate_2_base64(outData)
        b64list = '    "' + '" +\n    "'.join([b64str[i:i+128] for i in range(0,len(b64str),128)]) + '")'
        self._te.append(b64list)




# Layout:
#
#  Palette                           Brushes
#                Drawing Area        (Chars/Glyphs)
#  Tools
#
#                                    Layouts
#                 Export
#
class PaintTemplate(ttk.TTkAppTemplate):
    def __init__(self, border=False, **kwargs):
        super().__init__(border, **kwargs)
        self._parea    = PaintArea()
        ptoolkit = PaintToolKit()
        tarea    = TextArea()
        layers   = Layers()
        expArea  = ExportArea(self._parea)

        leftPanel = LeftPanel()
        palette = leftPanel.palette()

        rightPanel = ttk.TTkSplitter(orientation=ttk.TTkK.VERTICAL)
        rightPanel.addWidget(tarea)
        # rightPanel.addItem(expArea, title="Export")
        # rightPanel.setSizes([None,5])
        rightPanel.addItem(layers, title='Layers')
        rightPanel.setSizes([None,9])

        self.setItem(expArea, self.BOTTOM, title="Export")

        self.setItem(leftPanel     , self.LEFT,  size=16*2)
        self.setWidget(self._parea , self.MAIN)
        self.setItem(ptoolkit      , self.TOP,   fixed=True)
        self.setItem(rightPanel    , self.RIGHT, size=50)

        self.setMenuBar(appMenuBar:=ttk.TTkMenuBarLayout(), self.TOP)
        fileMenu      = appMenuBar.addMenu("&File")
        buttonOpen    = fileMenu.addMenu("&Open")
        buttonClose   = fileMenu.addMenu("&Save")
        buttonClose   = fileMenu.addMenu("Save &As...")
        fileMenu.addSpacer()
        fileMenu.addMenu("&Import").menuButtonClicked.connect(self.importDictWin)
        fileMenu.addSpacer()
        fileMenu.addMenu("Load Palette")
        fileMenu.addMenu("Save Palette")
        fileMenu.addSpacer()
        buttonExit    = fileMenu.addMenu("E&xit")
        buttonExit.menuButtonClicked.connect(ttk.TTkHelper.quit)

        # extraMenu = appMenuBar.addMenu("E&xtra")
        # extraMenu.addMenu("Scratchpad").menuButtonClicked.connect(self.scratchpad)
        # extraMenu.addSpacer()

        helpMenu = appMenuBar.addMenu("&Help", alignment=ttk.TTkK.RIGHT_ALIGN)
        helpMenu.addMenu("About ...").menuButtonClicked
        helpMenu.addMenu("About tlogg").menuButtonClicked

        palette.colorSelected.connect(self._parea.setGlyphColor)
        palette.colorSelected.connect(ptoolkit.setColor)
        ptoolkit.updatedColor.connect(self._parea.setGlyphColor)
        ptoolkit.updatedTrans.connect(self._parea.setTrans)
        tarea.charSelected.connect(ptoolkit.glyphFromString)
        tarea.charSelected.connect(self._parea.glyphFromString)
        leftPanel.toolSelected.connect(self._parea.setTool)

        self._parea.setGlyphColor(palette.color())
        ptoolkit.setColor(palette.color())

    @ttk.pyTTkSlot()
    def importDictWin(self):
        newWindow = ttk.TTkUiLoader.loadFile(os.path.join(os.path.dirname(os.path.abspath(__file__)),"quickImport.tui.json"))
        te = newWindow.getWidgetByName("TextEdit")

        @ttk.pyTTkSlot()
        def _importDict(te=te):
            def _probeCompressedText(_text):
                import re
                ret = ""
                for _t in _text.split('\n'):
                    if m := re.match(r'^ *["\']([A-Za-z0-9+/]+[=]{0,2})["\' +]*$',_t):
                        ret += m.group(1)
                    elif not re.match(r'^ *$',_t): # exclude empty lines
                        return ""
                return ret
            text = te.toPlainText()
            if compressed := _probeCompressedText(text):
                dd = ttk.TTkUtil.base64_deflate_2_obj(compressed)
            else:
                try:
                    dd = eval(text)
                except Exception as e:
                    ttk.TTkLog.error(str(e))
                    messageBox = ttk.TTkMessageBox(text= str(e),icon=ttk.TTkMessageBox.Icon.Warning)
                    ttk.TTkHelper.overlay(None, messageBox, 5, 5, True)
                    return

            if type(dd) is not dict:
                messageBox = ttk.TTkMessageBox(text= f"Input is {type(dd)}\nImport data must be a dict or \ncompressed String definition",icon=ttk.TTkMessageBox.Icon.Warning)
                ttk.TTkHelper.overlay(None, messageBox, 5, 5, True)
                return

            self._parea.importLayer(dd)

            newWindow.close()

        newWindow.getWidgetByName("BtnDict"   ).clicked.connect(_importDict)
        ttk.TTkHelper.overlay(None, newWindow, 10, 4, modal=True)

