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

import sys, os, json

sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk

from .paintarea    import PaintArea, PaintScrollArea
from .toolspanel   import ToolsPanel
from .canvaslayer  import CanvasLayer
from .painttoolkit import PaintToolKit
from .textarea     import TextArea
from .layers       import Layers,LayerData
from .about        import About

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
        crop    = self._cbCrop.isChecked()
        palette = self._cbPal.isChecked()
        full    = self._cbFull.isChecked()
        image = self._paintArea.exportImage()
        self._te.setText(image)

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
    def __init__(self, fileName=None, border=False, **kwargs):
        super().__init__(border, **kwargs)
        self._parea  = parea = PaintArea()
        self._layers = layers = Layers()
        ptoolkit = PaintToolKit()
        tarea    = TextArea()
        expArea  = ExportArea(parea)

        toolsPanel = ToolsPanel()
        palette = toolsPanel.palette()

        rightPanel = ttk.TTkSplitter(orientation=ttk.TTkK.VERTICAL)
        rightPanel.addWidget(tarea)
        # rightPanel.addItem(expArea, title="Export")
        # rightPanel.setSizes([None,5])
        rightPanel.addItem(layers, title='Layers')
        rightPanel.setSizes([None,9])

        self.setItem(expArea, self.BOTTOM, title="Export")

        self.setItem(toolsPanel     , self.LEFT,  size=16*2)
        self.setWidget(PaintScrollArea(parea) , self.MAIN)
        self.setWidget(ptoolkit      , self.TOP,   fixed=True)
        self.setItem(rightPanel    , self.RIGHT, size=40)

        self.setMenuBar(appMenuBar:=ttk.TTkMenuBarLayout(), self.TOP)
        fileMenu      = appMenuBar.addMenu("&File")
        fileMenu.addMenu("&Open"      ).menuButtonClicked.connect(self._open)
        fileMenu.addMenu("&Save"      ).menuButtonClicked.connect(self._save)
        fileMenu.addMenu("Save &As...").menuButtonClicked.connect(self._saveAs)
        fileMenu.addSpacer()
        fileMenu.addMenu("&Import").menuButtonClicked.connect(self.importDictWin)
        menuExport = fileMenu.addMenu("&Export")
        fileMenu.addSpacer()
        fileMenu.addMenu("Load Palette").setEnabled(False)
        fileMenu.addMenu("Save Palette").setEnabled(False)
        fileMenu.addSpacer()
        buttonExit    = fileMenu.addMenu("E&xit")
        buttonExit.menuButtonClicked.connect(ttk.TTkHelper.quit)

        menuExport.addMenu("Ascii/&Txt").menuButtonClicked.connect(self._saveAsAscii)
        menuExport.addMenu("&Ansi").menuButtonClicked.connect(self._saveAsAnsi)
        menuExport.addMenu("&Python").setEnabled(False)
        menuExport.addMenu("&Bash").setEnabled(False)


        # extraMenu = appMenuBar.addMenu("E&xtra")
        # extraMenu.addMenu("Scratchpad").menuButtonClicked.connect(self.scratchpad)
        # extraMenu.addSpacer()

        def _showAbout(btn):
            ttk.TTkHelper.overlay(None, About(), 30,10)
        def _showAboutTTk(btn):
            ttk.TTkHelper.overlay(None, ttk.TTkAbout(), 30,10)

        helpMenu = appMenuBar.addMenu("&Help", alignment=ttk.TTkK.RIGHT_ALIGN)
        helpMenu.addMenu("About ...").menuButtonClicked.connect(_showAboutTTk)
        helpMenu.addMenu("About DPT").menuButtonClicked.connect(_showAbout)

        palette.colorSelected.connect(self._parea.setGlyphColor)
        palette.colorSelected.connect(ptoolkit.setColor)

        ptoolkit.updatedColor.connect(self._parea.setGlyphColor)
        ptoolkit.updatedTrans.connect(self._parea.setTrans)

        tarea.charSelected.connect(ptoolkit.glyphFromString)
        tarea.charSelected.connect(parea.glyphFromString)
        tarea.charSelected.connect(toolsPanel.glyphFromString)

        toolsPanel.toolSelected.connect(parea.setTool)
        toolsPanel.areaChanged.connect(parea.setAreaBrush)

        self._parea.setGlyphColor(palette.color())
        ptoolkit.setColor(palette.color())

        ptoolkit.glyphFromString(ttk.TTkString('X'))
        parea.glyphFromString(ttk.TTkString('X'))
        toolsPanel.glyphFromString(ttk.TTkString('X'))
        parea.setTool(CanvasLayer.Tool.BRUSH|CanvasLayer.Tool.GLYPH)

        parea.layerSelected.connect(ptoolkit.updateLayer)
        parea.layerAdded.connect(self._canvasLayerAdded)
        parea.layerPicked.connect(toolsPanel.setAreaLayer)

        @ttk.pyTTkSlot(LayerData)
        def _layerSelected(l:LayerData):
            parea.setCurrentLayer(l.data())

        layers.layerAdded.connect(self._layerAdded)
        layers.layerSelected.connect(_layerSelected)
        layers.layersOrderChanged.connect(self._layersOrderChanged)
        layers.addLayer(name="Background")
        if fileName:
            self._openFile(fileName)

        ttk.ttkConnectDragOpen(ttk.TTkEncoding.APPLICATION_JSON, self._openDragData)

    @ttk.pyTTkSlot()
    def _open(self):
        ttk.ttkCrossOpen(
                path='.',
                encoding=ttk.TTkEncoding.APPLICATION_JSON,
                filter="DumbPaintTool Files (*.DPT.json);;Json Files (*.json);;All Files (*)",
                cb=self._openDragData)

    @ttk.pyTTkSlot()
    def _save(self):
        doc = self._parea.exportDocument()
        ttk.ttkCrossSave('untitled.DPT.json', json.dumps(doc, indent=1), ttk.TTkEncoding.APPLICATION_JSON)

    @ttk.pyTTkSlot()
    def _saveAs(self):
        doc = self._parea.exportDocument()
        ttk.ttkCrossSaveAs('untitled.DPT.json', json.dumps(doc, indent=1), ttk.TTkEncoding.APPLICATION_JSON,
                           filter="DumbPaintTool Files (*.DPT.json);;Json Files (*.json);;All Files (*)")

    @ttk.pyTTkSlot()
    def _saveAsAnsi(self):
        image = self._parea.exportImage()
        text = ttk.TTkString(image)
        ttk.ttkCrossSaveAs('untitled.DPT.Ansi.txt', text.toAnsi(), ttk.TTkEncoding.TEXT_PLAIN_UTF8,
                           filter="Ansi text Files (*.Ansi.txt);;Text Files (*.txt);;All Files (*)")

    @ttk.pyTTkSlot()
    def _saveAsAscii(self):
        image = self._parea.exportImage()
        text = ttk.TTkString(image)
        ttk.ttkCrossSaveAs('untitled.DPT.ASCII.txt', text.toAscii(), ttk.TTkEncoding.TEXT_PLAIN_UTF8,
                           filter="ASCII Text Files (*.ASCII.txt);;Text Files (*.txt);;All Files (*)")

    @ttk.pyTTkSlot(dict)
    def _openDragData(self, data):
        dd = json.loads(data['data'])
        if 'layers' in dd:
            self.importDocument(dd)
        else:
            self._layers.addLayer(name="Import")
            self._parea.importLayer(dd)

    def _openFile(self, fileName):
        ttk.TTkLog.info(f"Open: {fileName}")

        with open(fileName) as fp:
            # dd = json.load(fp)
            # text = fp.read()
            # dd = eval(text)
            dd = json.load(fp)
            if 'layers' in dd:
                self.importDocument(dd)
            else:
                self._layers.addLayer(name="Import")
                self._parea.importLayer(dd)

    # Connect and handle Layers event
    @ttk.pyTTkSlot(LayerData)
    def _layerAdded(self, l:LayerData):
        self._parea.layerAdded.disconnect(self._canvasLayerAdded)
        nl = self._parea.newLayer()
        self._parea.layerAdded.connect(self._canvasLayerAdded)
        nl.setName(l.name())
        l.setData(nl)
        l.nameChanged.connect(nl.setName)
        l.visibilityToggled.connect(nl.setVisible)
        l.visibilityToggled.connect(self._parea.update)

    @ttk.pyTTkSlot(CanvasLayer)
    def _canvasLayerAdded(self, l:CanvasLayer=None):
        self._layers.clear()
        self._layers.layerAdded.disconnect(self._layerAdded)
        for l in self._parea.canvasLayers():
            ld = self._layers.addLayer(name=l.name(),data=l)
            ld.nameChanged.connect(l.setName)
            ld.visibilityToggled.connect(l.setVisible)
            ld.visibilityToggled.connect(self._parea.update)
        self._layers.layerAdded.connect(self._layerAdded)

    @ttk.pyTTkSlot(list[LayerData])
    def _layersOrderChanged(self, layers:list[LayerData]):
        self._parea._canvasLayers = [ld.data() for ld in reversed(layers)]
        self._parea.update()

    def importDocument(self, dd):
        self._parea.layerAdded.disconnect(self._canvasLayerAdded)
        self._parea.importDocument(dd)
        self._canvasLayerAdded()
        self._parea.layerAdded.connect(self._canvasLayerAdded)

    @ttk.pyTTkSlot()
    def importDictWin(self):
        newWindow = ttk.TTkUiLoader.loadFile(os.path.join(os.path.dirname(os.path.abspath(__file__)),"tui/quickImport.tui.json"))
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

