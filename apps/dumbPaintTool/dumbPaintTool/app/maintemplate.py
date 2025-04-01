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

import os, json

import TermTk as ttk

from .paintarea    import PaintArea, PaintScrollArea
from .toolspanel   import ToolsPanel
from .canvaslayer  import CanvasLayer
from .painttoolkit import PaintToolKit
from .textarea     import TextArea
from .layersctrl   import LayersControl
from .about        import About
from .const        import ToolType
from .filters      import HueChromaLightness,BrightnessContrast
from .importimage  import ImportImage
from .exportarea   import ExportArea
from .glbls        import glbls



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
        self._layers = layers = LayersControl()
        ptoolkit = PaintToolKit()
        tarea    = TextArea()
        expArea  = ExportArea(parea)

        toolsPanel = ToolsPanel()

        rightPanel = ttk.TTkSplitter(orientation=ttk.TTkK.VERTICAL)
        rightPanel.addWidget(tarea)
        # rightPanel.addItem(expArea, title="Export")
        # rightPanel.setSizes([None,5])
        rightPanel.addItem(layers, title='Layers')
        rightPanel.setSizes([None,9])

        self.setItem(expArea, self.BOTTOM, title="Export")

        self.setItem(toolsPanel     , self.LEFT,  size=16*2)
        self.setWidget(PaintScrollArea(parea) , self.MAIN)
        self.setWidget(ptoolkit      , self.TOP,   fixed=True, title=glbls.fileName())
        self.setItem(rightPanel    , self.RIGHT, size=40)

        glbls.fileNameChanged.connect(lambda _n : self.setTitle(self.TOP,_n))

        self.setMenuBar(appMenuBar:=ttk.TTkMenuBarLayout(), self.TOP)
        fileMenu      = appMenuBar.addMenu("&File")
        fileMenu.addMenu("&New"       ).menuButtonClicked.connect(self._new)
        fileMenu.addMenu("&Open"      ).menuButtonClicked.connect(self._open)
        fileMenu.addMenu("&Save"      ).menuButtonClicked.connect(self._save)
        fileMenu.addMenu("Save &As...").menuButtonClicked.connect(self._saveAs)
        fileMenu.addSpacer()
        fileMenu.addMenu("&Import").menuButtonClicked.connect(self.importDictWin)
        fileMenu.addMenu("Import Image").menuButtonClicked.connect(self._openImage)
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

        colorMenu      = appMenuBar.addMenu("&Color")
        colorMenu.addMenu("&Hue Chroma Lightness").menuButtonClicked.connect(self._hueChromaLightness)
        colorMenu.addMenu("&Brightness Contrast").menuButtonClicked.connect(self._brightnessContrast)

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

        # Paint Area Transparency color
        ptoolkit.updatedTrans.connect(self._parea.setTrans)

        glbls.layers.addLayer(name="Background")
        if fileName:
            self._openFile(fileName)
        else:
            glbls.clearSnapshot()
            glbls.saveSnapshot()

        ttk.ttkConnectDragOpen(ttk.TTkEncoding.APPLICATION_JSON, self._openDragData)
        ttk.ttkConnectDragOpen(ttk.TTkEncoding.IMAGE, self._openImageData)

        ttk.TTkShortcut(ttk.TTkK.CTRL | ttk.TTkK.Key_Z).activated.connect(glbls.undo)
        ttk.TTkShortcut(ttk.TTkK.CTRL | ttk.TTkK.Key_Y).activated.connect(glbls.redo)

        # Debug import image
        # from PIL import Image
        # pilImage = Image.open("experiments/Peppered/euDock-purple.png")
        # newWindow = ImportImage(pilImage,minSize=(60,30))
        # newWindow.exportedImage.connect(parea.pasteEvent)
        # ttk.TTkHelper.overlay(None, newWindow, 10, 4, modal=True)

    @ttk.pyTTkSlot()
    def _new(self):
        glbls.layers.clear()
        glbls.layers.addLayer(name="Background")

    @ttk.pyTTkSlot()
    def _open(self):
        ttk.ttkCrossOpen(
                path='.',
                encoding=ttk.TTkEncoding.APPLICATION_JSON,
                filter="DumbPaintTool Files (*.DPT.json);;Json Files (*.json);;All Files (*)",
                cb=self._openDragData)

    @ttk.pyTTkSlot()
    def _openImage(self):
        ttk.ttkCrossOpen(
                path='.',
                encoding=ttk.TTkEncoding.IMAGE,
                filter="Images (*.png *.jpg *.gif *.ico);;All Files (*)",
                cb=self._openImageData)

    @ttk.pyTTkSlot()
    def _save(self):
        doc = self._parea.exportDocument()
        ttk.ttkCrossSave(glbls.fileName(), json.dumps(doc, indent=1), ttk.TTkEncoding.APPLICATION_JSON)

    @ttk.pyTTkSlot()
    def _saveAs(self):
        doc = self._parea.exportDocument()
        ttk.ttkCrossSaveAs(glbls.fileName(), json.dumps(doc, indent=1), ttk.TTkEncoding.APPLICATION_JSON,
                           filter="DumbPaintTool Files (*.DPT.json);;Json Files (*.json);;All Files (*)",
                           cb=lambda _d:glbls.setFilename(_d['name']))

    @ttk.pyTTkSlot()
    def _saveAsAnsi(self):
        image = self._parea.exportImage()
        text = ttk.TTkString(image)
        ttk.ttkCrossSaveAs(glbls.fileName(), text.toAnsi(), ttk.TTkEncoding.TEXT_PLAIN_UTF8,
                           filter="Ansi text Files (*.Ansi.txt);;Text Files (*.txt);;All Files (*)")

    @ttk.pyTTkSlot()
    def _saveAsAscii(self):
        image = self._parea.exportImage()
        text = ttk.TTkString(image)
        ttk.ttkCrossSaveAs('untitled.DPT.ASCII.txt', text.toAscii(), ttk.TTkEncoding.TEXT_PLAIN_UTF8,
                           filter="ASCII Text Files (*.ASCII.txt);;Text Files (*.txt);;All Files (*)")

    @ttk.pyTTkSlot(dict)
    def _openImageData(self, data):
        newWindow = ImportImage(data['data'])
        newWindow.exportedImage.connect(self._parea.pasteEvent)
        ttk.TTkHelper.overlay(None, newWindow, 10, 4, modal=True)

    @ttk.pyTTkSlot(dict)
    def _openDragData(self, data):
        dd = json.loads(data['data'])
        glbls.setFilename(data['name'])
        if 'layers' in dd:
            self.importDocument(dd)
        else:
            glbls.layers.importLayer(dd,"Import")

    def importDocument(self, data):
        glbls.layers.clear()
        if (
            ( 'version' in data and data['version'] == '1.0.0' ) or
            ( 'version' in data and data['version'] == '1.0.1' and data['type'] == 'DumbPaintTool/Document') ):
            for ld in data['layers']:
                glbls.layers.addLayer().importLayer(ld)
        else:
            ttk.TTkLog.error("File Format not recognised")


    def _openFile(self, fileName):
        ttk.TTkLog.info(f"Open: {fileName}")
        glbls.setFilename(fileName)

        with open(fileName) as fp:
            # dd = json.load(fp)
            # text = fp.read()
            # dd = eval(text)
            dd = json.load(fp)
            if 'layers' in dd:
                self.importDocument(dd)
            else:
                glbls.layers.importLayer(dd,"Import")
            glbls.clearSnapshot()
            glbls.saveSnapshot()

    @ttk.pyTTkSlot()
    def _hueChromaLightness(self):
        newWindow = HueChromaLightness(glbls.layers.selected())
        ttk.TTkHelper.overlay(None, newWindow, 10, 4, modal=True)

    @ttk.pyTTkSlot()
    def _brightnessContrast(self):
        newWindow = BrightnessContrast(glbls.layers.selected())
        ttk.TTkHelper.overlay(None, newWindow, 10, 4, modal=True)

    @ttk.pyTTkSlot()
    def importDictWin(self):
        newWindow = ttk.TTkUiLoader.loadFile(os.path.join(os.path.dirname(os.path.abspath(__file__)),"../tui/quickImport.tui.json"))
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
                glbls.layers.addLayer().importLayer(dd)

            newWindow.close()

        newWindow.getWidgetByName("BtnDict"   ).clicked.connect(_importDict)
        ttk.TTkHelper.overlay(None, newWindow, 10, 4, modal=True)

