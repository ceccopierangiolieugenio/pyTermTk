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

class SuperWidget(ttk.TTkWidget):
    def __init__(self, wid, weModified, thingSelected, *args, **kwargs):
        self.weModified = weModified
        self.thingSelected = thingSelected
        self._wid = wid
        self._wid.move(*kwargs['pos'])
        self._wid._canvas.show()
        self._superLayout = so.SuperLayout(lay=self._wid.layout(), weModified=self.weModified, thingSelected=self.thingSelected,)
        self._superRootWidget = kwargs.get('superRootWidget',False)
        kwargs['layout'] = ttk.TTkGridLayout()
        kwargs['layout'].addWidget(self._superLayout)
        kwargs['maxSize'] = wid.maximumSize()
        kwargs['minSize'] = wid.minimumSize()
        kwargs['size']    = wid.size()
        padt, padb, padl, padr = wid.getPadding()
        kwargs['paddingTop'] = padt
        kwargs['paddingBottom'] = padb
        kwargs['paddingLeft'] = padl
        kwargs['paddingRight'] = padr
        super().__init__(*args, **kwargs)
        #self.resize(*self._wid.size())
        h,s,l = randint(0,359),100,randint(60,80)
        r,g,b = ttk.TTkColor.hsl2rgb(((h+5)%360,s,l))
        self._layoutColor    = ttk.TTkColor.bg(f"#{r:02X}{g:02X}{b:02X}", modifier=ttk.TTkColorGradient(increment=+2))
        r,g,b = ttk.TTkColor.hsl2rgb(((h+5)%360,s,l))
        self._layoutPadColor = ttk.TTkColor.bg(f"#{r:02X}{g:02X}{b:02X}", modifier=ttk.TTkColorGradient(increment=-2))
        self.setFocusPolicy(ttk.TTkK.ClickFocus)
        SuperWidget.toggleHighlightLayout.connect(self._toggleHighlightLayout)

    _showLayout = False
    toggleHighlightLayout = ttk.pyTTkSignal(bool)

    @ttk.pyTTkSlot(bool)
    def _toggleHighlightLayout(self, state):
        SuperWidget._showLayout = state
        self.update()

    def dumpDict(self):
        wid = self._wid
        ret = {
            'class'  : wid.__class__.__name__,
            'params' : SuperObject.dumpParams(wid),
            'layout': self._superLayout.dumpDict()
        }
        return ret

    @staticmethod
    def swFromWidget(wid, *args, **kwargs):
        # layout = wid.layout()
        #newLayout = ttk.TTkLayout()
        ## copy layout compatible properties
        #for att in newLayout.__slots__:
        #    if hasattr(layout,att):
        #        setattr(newLayout,att,getattr(layout,att))
        #wid.setLayout(newLayout)

        #if issubclass(type(data),ttk.TTkVBoxLayout):
        #    sl = so.SuperLayoutVBox(pos=(x,y), size=(w,h), lay=lay, weModified=self.weModified, thingSelected=self.thingSelected, selectable=True)
        #elif issubclass(type(data),ttk.TTkHBoxLayout):
        #    sl = so.SuperLayoutHBox(pos=(x,y), size=(w,h), lay=lay, weModified=self.weModified, thingSelected=self.thingSelected, selectable=True)
        #elif issubclass(type(data),ttk.TTkGridLayout):
        #    sl = so.SuperLayoutGrid(pos=(x,y), size=(w,h), lay=lay, weModified=self.weModified, thingSelected=self.thingSelected, selectable=True)
        #else:
        #    sl = so.SuperLayout(    pos=(x,y), size=(w,h), lay=lay, weModified=self.weModified, thingSelected=self.thingSelected, selectable=True)

        layout = wid.layout()
        sw = so.SuperWidget(wid=wid, *args, **kwargs)
        sw.changeSuperLayout(type(layout))
        for ch in layout.children():
            x,y,w,h = ch.geometry()
            if ch.layoutItemType == ttk.TTkK.WidgetItem:
                sch = so.SuperWidget.swFromWidget(ch.widget(), *args, **(kwargs|{'pos':(x,y),'size':(w,h)}))
            else:
                sch = so.SuperLayout.slFromLayout(ch, *args, **(kwargs|{'pos':(x,y),'size':(w,h),'selectable':True}))
            if issubclass(type(layout),ttk.TTkGridLayout):
                sw._superLayout.layout().addWidget(sch,ch._row,ch._col,ch._rowspan,ch._colspan)
            else:
                sw._superLayout.layout().addWidget(sch)
        return sw

    @staticmethod
    def loadDict(parent, widProp):
        ttkClass = getattr(ttk,widProp['class'])
        if issubclass(ttkClass,ttk.TTkLayout):
            demiProp = {
                'version':'1.0.0',
                'tui':{
                    'class'  : widProp['class'],
                    'params' : widProp['params'],
                    'children' : []
                },
                'connections':[]
            }
            layout = ttk.TTkUiLoader.loadDict(demiProp)
            x,y,w,h = layout.geometry()
            sl = sup = so.SuperLayout.slFromLayout(layout=layout, lay=ttk.TTkLayout(), pos=(x,y), size=(w,h), weModified=parent.weModified, thingSelected=parent.thingSelected, selectable=True)
            children = widProp['children']
        else:
            demiProp = {
                'version':'1.0.0',
                'tui':{
                    'class'  : widProp['class'],
                    'params' : widProp['params']|{'Layout':'TTkLayout'},
                    'layout': {
                        'class'  : 'TTkLayout',
                        'params' : widProp['layout']['params'],
                        'children' : []
                    }
                },
                'connections':[]
            }
            wid = ttk.TTkUiLoader.loadDict(demiProp)
            sup = so.SuperWidget(wid=wid, pos=wid.pos(), weModified=parent.weModified, thingSelected=parent.thingSelected)
            sup.changeSuperLayout(getattr(ttk,widProp['layout']['class']))
            sl = sup._superLayout
            children = widProp['layout']['children']

        for ch in children:
            sch = SuperWidget.loadDict(parent, ch)
            if issubclass(type(sl),so.SuperLayoutGrid):
                sl.layout().addWidget(sch,ch['row'],ch['col'],ch['rowspan'],ch['colspan'])
            else:
                sl.layout().addWidget(sch)
        return sup

    def changeSuperLayout(self, layout):
        sl = self._superLayout
        self.layout().removeWidget(sl)
        if layout == ttk.TTkVBoxLayout:
            sl = so.SuperLayoutVBox(lay=self._wid.layout(), weModified=self.weModified, thingSelected=self.thingSelected, selectable=False)
        elif layout == ttk.TTkHBoxLayout:
            sl = so.SuperLayoutHBox(lay=self._wid.layout(), weModified=self.weModified, thingSelected=self.thingSelected, selectable=False)
        elif layout == ttk.TTkGridLayout:
            sl = so.SuperLayoutGrid(lay=self._wid.layout(), weModified=self.weModified, thingSelected=self.thingSelected, selectable=False)
        else:
            sl = so.SuperLayout(    lay=self._wid.layout(), weModified=self.weModified, thingSelected=self.thingSelected, selectable=False)
        self._superLayout = sl
        self._wid.setLayout(layout())
        self.layout().addWidget(sl)

    def updateAll(self):
        self.resize(*(self._wid.size()))
        self.move(*(self._wid.pos()))
        self.setPadding(*(self._wid.getPadding()))
        self.setMaximumSize(*(self._wid.maximumSize()))
        self.setMinimumSize(*(self._wid.minimumSize()))
        self.update()

    def mousePressEvent(self, evt) -> bool:
        return True

    def makeRootWidget(self):
        self._superRootWidget = True

    def pushSuperControlWidget(self):
        if self._superRootWidget: return False
        scw = so.SuperControlWidget(self)
        ttk.TTkHelper.removeOverlay()
        ttk.TTkHelper.overlay(self, scw, -1,-1, forceBoundaries=False)

    def mouseReleaseEvent(self, evt) -> bool:
        self.pushSuperControlWidget()
        self.thingSelected.emit(self._wid,self)
        return True

    def mouseDragEvent(self, evt) -> bool:
        if self._superRootWidget: return False
        drag = ttk.TTkDrag()
        data = self
        data.paintChildCanvas()
        drag.setHotSpot(evt.x, evt.y)
        drag.setPixmap(data.getCanvas())
        drag.setData(data)
        drag.exec()
        self.parentWidget().removeSuperWidget(self)
        return True

    def superChild(self):
        return self._wid

    def dropEvent(self, evt) -> bool:
        padt, padb, padl, padr = self._wid.getPadding()
        # evt = evt.copy()
        evt.x-=padl
        evt.y-=padt
        return self._superLayout.dropEvent(evt)

    def move(self, x: int, y: int):
        self._wid.move(x,y)
        self.update()
        return super().move(x, y)

    def resizeEvent(self, w, h):
        self._wid.resize(w,h)
        self._wid._canvas.updateSize()
        return super().resizeEvent(w, h)

    def paintEvent(self):
        w,h = self.size()
        if SuperWidget._showLayout:
            t,b,l,r = self._wid.getPadding()
            for y in range(h):
                self._canvas.drawText(pos=(0,y),text='',width=w,color=self._layoutColor)
            for y in range(t,h-b):
                self._canvas.drawText(pos=(l,y),text='',width=w-r-l,color=self._layoutPadColor)
            # self._canvas.fill(color=self._layoutColor)
            # self._canvas.fill(pos=(l,t), size=(w-r-l,h-b-t), color=self._layoutPadColor)
        else:
            self._wid.getCanvas().updateSize()
            self._wid.paintEvent()
            self._canvas.paintCanvas(
                    self._wid.getCanvas(),
                    (    0,     0, w, h), # geometry
                    (    0,     0, w, h), # slice
                    (    0,     0, w, h)) # bound