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

from .superobj import SuperWidget,SuperWidgetContainer

import TermTk as ttk


class WindowEditorView(ttk.TTkAbstractScrollView):
    __slots__ = ('_designer', '_snapRootWidget', '_ttk')
    def __init__(self, designer, *args, **kwargs):
        self._designer = designer
        super().__init__(*args, **kwargs)
        self._ttk = None
        self.viewChanged.connect(self._viewChangedHandler)
        self.newContainer()

    def newThing(self, thing):
        if self._ttk:
            self._ttk.superResized.disconnect(self._superChanged)
            self._ttk.superMoved.disconnect(self._superChanged)
            self.layout().removeWidget(self._ttk)
        self._ttk = SuperWidget.swFromWidget(wid=thing(name = 'MainWindow'), designer=self._designer, pos=(4,2), superRootWidget=True)
        self._ttk.resize(self.width()-8,self.height()-4)
        self._snapRootWidget = True
        self.layout().addWidget(self._ttk)
        self._ttk.superResized.connect(self._superChanged)
        self._ttk.superMoved.connect(self._superChanged)

    @ttk.pyTTkSlot()
    def newWindow(self):    return self.newThing(ttk.TTkWindow)
    @ttk.pyTTkSlot()
    def newContainer(self): return self.newThing(ttk.TTkContainer)
    @ttk.pyTTkSlot()
    def newFrame(self):     return self.newThing(ttk.TTkFrame)
    @ttk.pyTTkSlot()
    def newResFrame(self):  return self.newThing(ttk.TTkResizableFrame)

    def importSuperWidget(self, sw):
        if self._ttk:
            self._ttk.superResized.disconnect(self._superChanged)
            self._ttk.superMoved.disconnect(self._superChanged)
            self.layout().removeWidget(self._ttk)
        self._snapRootWidget = False
        self._ttk = sw
        self._ttk.makeRootWidget()
        self.layout().addWidget(self._ttk)
        self._ttk.superResized.connect(self._superChanged)
        self._ttk.superMoved.connect(self._superChanged)

    def getTTk(self):
        return self._ttk

    def dumpDict(self):
        return self._ttk.dumpDict()

    @ttk.pyTTkSlot()
    def _superChanged(self):
        self._snapRootWidget = False
        self.viewChanged.emit()

    def resizeEvent(self, w, h):
        if self._snapRootWidget:
            self._ttk.resize(w-8,h-4)
            self._snapRootWidget = True
        return super().resizeEvent(w, h)

    @ttk.pyTTkSlot()
    def _viewChangedHandler(self):
        x,y = self.getViewOffsets()
        self.layout().setOffset(-x,-y)

    def viewFullAreaSize(self):
        x,y,w,h = self.layout().fullWidgetAreaGeometry()
        return x+w, y+h

    def viewDisplayedSize(self):
        return self.size()

    def paintEvent(self, canvas):
        w,h = self.size()
        # canvas.fill(pos=(0,0),size=(w,h), char="╳", color=ttk.TTkColor.fg("#444400")+ttk.TTkColor.bg("#000044"))
        canvas.fill(pos=(0,0),size=(w,h), char="#", color=ttk.TTkColor.fg("#220044")+ttk.TTkColor.bg("#000022"))

class WindowEditor(ttk.TTkAbstractScrollArea):
    __slots__ = ('getTTk', 'dumpDict', 'importSuperWidget',
                 # Forwarded slots
                 'newWindow', 'newWidget', 'newFrame', 'newResFrame')
    def __init__(self, designer, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setViewport(wev := WindowEditorView(designer))
        # Forward Methods
        self.getTTk            = wev.getTTk
        self.dumpDict          = wev.dumpDict
        self.importSuperWidget = wev.importSuperWidget
        self.newWindow         = wev.newWindow
        self.newContainer      = wev.newContainer
        self.newFrame          = wev.newFrame
        self.newResFrame       = wev.newResFrame