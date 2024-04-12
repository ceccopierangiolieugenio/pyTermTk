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

from random import randint

import TermTk as ttk
import ttkDesigner.app.superobj as so
from .superobj import SuperObject

class SuperLayout(ttk.TTkContainer):
    __slots__ = ('_lay', '_dropBorder', '_superRootWidget', '_selectable', '_designer')
    def __init__(self, lay, designer, *args, **kwargs):
        self._designer = designer
        self._lay = lay
        self._dropBorder = 0 # This property is used to exclude the border from the drop routine
        self._superRootWidget = kwargs.get('superRootWidget',False)
        self._selectable = kwargs.get('selectable', False)

        # kwargs['pos']  = (x,y) = lay.pos()
        # x,y = kwargs.get('pos',lay.pos())
        # kwargs['size'] = (w,h) = lay.size()
        # kwargs['layout'] = lay # .__class__()
        # self._lay.setGeometry(x,y,w,h)

        super().__init__(*args, **kwargs)

        self.getCanvas().setTransparent(True)
        # r,g,b = randint(0,0xFF),randint(0,0xFF),randint(0,0xFF)
        # self._layoutColor    = ttk.TTkColor.bg(f"#{r:02X}{g:02X}{b:02X}")
        self.setFocusPolicy(ttk.TTkK.ClickFocus)
        so.SuperWidget.toggleHighlightLayout.connect(self._toggleHighlightLayout)

    # TODO: Find a better way to handle this exception
    # It may require some major rewrite
    def hasControlWidget(self):
        return True

    def getSuperProperties(self):
        additions = {}
        exceptions = {}
        exclude = []
        return additions, exceptions, exclude

    @ttk.pyTTkSlot(bool)
    def _toggleHighlightLayout(self, state):
        so.SuperWidget._showLayout = state
        self.update()

    def setDropBorder(self, db):
        self._dropBorder = db

    def dropBorder(self):
        return self._dropBorder

    def dumpDict(self):
        children=[]
        for w in self.layout().children():
            layoutItemParams = {
                'row':w._row,
                'col':w._col,
                'rowspan':w._rowspan,
                'colspan':w._colspan,
            }
            children.append(w.widget().dumpDict()|layoutItemParams)
        ret = {'class': self.layout().__class__.__name__,
               # 'params' : SuperObject.dumpParams(self._lay),
               'params' : SuperObject.dumpParams(self.layout())|{'Geometry':self.geometry()},
               'children':children}
        return ret

    def updateAll(self):
        # self.resize(*(self._lay.size()))
        # self.move(*(self._lay.pos()))
        # self.setPadding(*(self._lay.getPadding()))
        # self.setMaximumSize(*(self._lay.maximumSize()))
        # self.setMinimumSize(*(self._lay.minimumSize()))
        self.update()

    def mousePressEvent(self, evt) -> bool:
        return self._selectable and not self._superRootWidget

    def pushSuperControlWidget(self):
        if self._superRootWidget or not self._selectable: return False
        scw = so.SuperControlWidget(self)
        ttk.TTkHelper.removeOverlay()
        ttk.TTkHelper.overlay(self, scw, -1,-1, forceBoundaries=False)

    def mouseReleaseEvent(self, evt) -> bool:
        if self._superRootWidget or not self._selectable: return False
        self.pushSuperControlWidget()
        self._designer.thingSelected.emit(self._lay,self)
        return True

    def mouseDragEvent(self, evt) -> bool:
        if self._superRootWidget or not self._selectable: return False
        drag = ttk.TTkDrag()
        data = self
        canvas = self.getCanvas()
        canvas.clean()
        self.paintEvent(canvas)
        ttk.TTkWidget._paintChildCanvas(canvas, self.layout(), self.layout().geometry(), self.layout().offset())
        drag.setHotSpot(evt.x, evt.y)
        drag.setPixmap(canvas)
        drag.setData(data)
        drag.exec()
        self.parentWidget().removeSuperWidget(self)
        return True

    def isRootWidget(self):
        return self._superRootWidget

    def makeRootWidget(self):
        self._superRootWidget = True

    def superChild(self):
        return self._lay

    @staticmethod
    def slFromLayout(layout: ttk.TTkLayout, *args, **kwargs):
        if 'lay' not in kwargs:
            kwargs |= {'lay':layout}
        if issubclass(type(layout),ttk.TTkVBoxLayout):
            sl = so.SuperLayoutVBox(*args, **kwargs)
        elif issubclass(type(layout),ttk.TTkHBoxLayout):
            sl = so.SuperLayoutHBox(*args, **kwargs)
        elif issubclass(type(layout),ttk.TTkGridLayout):
            sl = so.SuperLayoutGrid(*args, **kwargs)
        else:
            sl = so.SuperLayout(    *args, **kwargs)
        return sl

    def addSuperWidget(self, sw):
        self.layout().addWidget(sw)

    def removeSuperWidget(self, sw):
        self._lay.removeItem(self._lay)
        sc = sw.superChild()
        if issubclass(type(sc),ttk.TTkLayout):
            self._lay.removeItem(sc)
        else:
            self._lay.removeWidget(sc)
        self.layout().removeWidget(sw)
        self.layout().update()
        self.update()

    def isInDropBorder(self,x,y):
        if db := self._dropBorder:
            w,h = self.size()
            if not (db < x < w-1-db and db < y < h-1-db):
                return True
        return False

    def dropEvent(self, evt) -> bool:
        # Skip the drop event if dropborder is set and the cursor is along the edges
        if self.isInDropBorder(evt.x, evt.y): return False
        data = evt.data()
        hsx,hsy = evt.hotSpot()
        ttk.TTkLog.debug(f"Drop ({data.__class__.__name__}) -> pos={evt.pos()}")
        if issubclass(type(data),ttk.TTkLayout):
            _,__,w,h = data.geometry()
            x,y = evt.x-hsx, evt.y-hsy
            lay = ttk.TTkLayout(pos=(x,y), size=(w,h))
            sl = SuperLayout.slFromLayout(layout=data, designer=self._designer, lay=lay, pos=(x,y), size=(w,h), selectable=True)
            self.addSuperWidget(sl)
            self._lay.addItem(lay)
        elif issubclass(type(data), so.SuperLayout):
            sl = data
            self.addSuperWidget(sl)
            self._lay.addItem(sl._lay)
            sl.show()
            sl.move(evt.x-hsx, evt.y-hsy)
        elif issubclass(type(data), so.SuperWidgetContainer):
            sw = data
            self.addSuperWidget(sw)
            self._lay.addWidget(sw._wid)
            sl = sw._superLayout
            sw.move(evt.x-hsx, evt.y-hsy)
            sw.show()
        elif issubclass(type(data), so.SuperWidget):
            sw = data
            self.addSuperWidget(sw)
            self._lay.addWidget(sw._wid)
            sl = None
            sw.move(evt.x-hsx, evt.y-hsy)
            sw.show()
        elif issubclass(type(data),ttk.TTkTextEdit):
            self.addSuperWidget(sw := so.SuperWidget.swFromWidget(designer=self._designer, wid=data, pos=(evt.x-hsx, evt.y-hsy)))
            self._lay.addWidget(data)
            sw.move(evt.x-hsx, evt.y-hsy)
            sl = None
        elif issubclass(type(data),ttk.TTkContainer):
            self.addSuperWidget(sw := so.SuperWidget.swFromWidget(designer=self._designer, wid=data, pos=(evt.x-hsx, evt.y-hsy)))
            self._lay.addWidget(data)
            sw.move(evt.x-hsx, evt.y-hsy)
            sl = sw._superLayout
        elif issubclass(type(data),ttk.TTkWidget):
            self.addSuperWidget(sw := so.SuperWidget.swFromWidget(designer=self._designer, wid=data, pos=(evt.x-hsx, evt.y-hsy)))
            self._lay.addWidget(data)
            sw.move(evt.x-hsx, evt.y-hsy)
            sl = None
        else:
            return False

        self.layout().update()

        # set the Drop Border in case this layout auto resize
        if sl:
            if issubclass(type(self.layout()),ttk.TTkGridLayout):
                sl.setDropBorder(1)
            else:
                sl.setDropBorder(0)

        self.update()
        self._designer.weModified.emit()
        return True

    def move(self, x: int, y: int):
        w,h = self._lay.size()
        self._lay.setGeometry(x,y,w,h)
        return super().move(x, y)

    def resizeEvent(self, w, h):
        x,y = self._lay.pos()
        self._lay.setGeometry(x,y,w,h)
        return super().resizeEvent(w, h)

    def paintEvent(self, canvas):
        if self._selectable:
            if so.SuperWidget._showLayout:
                w,h = self.size()
                canvas.drawBox(pos=(0,0),size=(w,h), color=ttk.TTkColor.fg('#88DD88', modifier=ttk.TTkColorGradient(increment=+1)))
            else:
                w,h = self.size()
                canvas.drawBox(pos=(0,0),size=(w,h), color=ttk.TTkColor.fg('#223322', modifier=ttk.TTkColorGradient(increment=+1)))
