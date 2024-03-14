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
from .layers    import Layers,LayerData

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
            if ra_move.isChecked():
                tool = PaintArea.Tool.MOVE
            elif ra_brush.isChecked():
                tool = PaintArea.Tool.BRUSH
            elif ra_rect.isChecked():
                if ra_rect_e.isChecked():
                    tool = PaintArea.Tool.RECTEMPTY
                else:
                    tool = PaintArea.Tool.RECTFILL
            self.toolSelected.emit(tool)

        ra_rect.toggled.connect(ra_rect_f.setEnabled)
        ra_rect.toggled.connect(ra_rect_e.setEnabled)

        ra_move.toggled.connect(  _emitTool)
        ra_select.toggled.connect(  _emitTool)
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
    def __init__(self, paintArea:PaintArea, **kwargs):
        self._paintArea:PaintArea = paintArea
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
        btn_exPr.clicked.connect(self._exportDocument)

    @ttk.pyTTkSlot()
    def _exportLayer(self):
        dd = self._paintArea.exportLayer()
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
            if i in ('data','colors'): continue
            outTxt += f"  '{i}':'{dd[i]}',\n"
        for l in dd['data']:
            outTxt += f"    {l},\n"
        outTxt += "  ],'colors':[\n"
        for l in dd['colors']:
            outTxt += f"    {l},\n"
        outTxt += "  ],'palette':["
        for i,l in enumerate(dd['palette']):
            if not i%10:
                outTxt += f"\n    "
            outTxt += f"{l},"
        outTxt += "]}\n"
        self._te.append(outTxt)

    @ttk.pyTTkSlot()
    def _exportDocument(self):
        dd = self._paintArea.exportDocument()
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
    __slots__ = ('_parea','_layers')
    def __init__(self, border=False, **kwargs):
        super().__init__(border, **kwargs)
        self._parea  = parea = PaintArea()
        self._layers = layers = Layers()
        ptoolkit = PaintToolKit()
        tarea    = TextArea()
        expArea  = ExportArea(parea)

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

        @ttk.pyTTkSlot(LayerData)
        def _layerSelected(l:LayerData):
            parea.setCurrentLayer(l.data())

        layers.layerAdded.connect(self._layerAdded)
        layers.layerSelected.connect(_layerSelected)
        layers.addLayer(name="Background")

    # Connect and handle Layers event
    @ttk.pyTTkSlot(LayerData)
    def _layerAdded(self, l:LayerData):
        nl = self._parea.newLayer()
        nl.setName(l.name())
        l.setData(nl)

    def importDocument(self, dd):
        self._parea.importDocument(dd)
        self._layers.clear()
        # Little Hack that I don't know how to overcome
        self._layers.layerAdded.disconnect(self._layerAdded)
        for l in self._parea.canvasLayers():
            self._layers.addLayer(name=l.name(),data=l)
        self._layers.layerAdded.connect(self._layerAdded)

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

            if 'layers' in dd:
                self.importDocument(dd)
            else:
                self._layers.addLayer(name="Import")
                self._parea.importLayer(dd)

            newWindow.close()

        newWindow.getWidgetByName("BtnDict"   ).clicked.connect(_importDict)
        ttk.TTkHelper.overlay(None, newWindow, 10, 4, modal=True)

