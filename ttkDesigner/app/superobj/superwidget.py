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
    __slots__ = ('_wid', '_superLayout', '_superRootWidget', '_designer',
                 'superMoved', 'superResized')
    def __init__(self, designer, wid, *args, **kwargs):
        self.superMoved   = ttk.pyTTkSignal(int,int)
        self.superResized = ttk.pyTTkSignal(int,int)
        self._designer = designer
        self._wid = wid
        self._wid.move(*kwargs['pos'])
        self._wid._canvas.show()
        self._superLayout = so.SuperLayout(designer=designer, lay=self._wid.layout(),)
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

    @ttk.pyTTkSlot(str)
    def setSuperName(self, name):
        if name and name not in [w.name() for w in self._designer.getWidgets()]:
            oldName = self._wid._name
            self._wid._name = name
            self._designer.widgetNameChanged.emit(oldName, name)
            self._designer.weModified.emit()

    def getSuperProperties(self):
        exceptions = {
            'Name': {
                'get':  { 'cb':ttk.TTkWidget.name,               'type':str} ,
                'set':  { 'cb':lambda _,n: self.setSuperName(n), 'type':str} },
            'Layout' : {
                'get':  { 'cb': lambda _: self._superLayout.layout().__class__ , 'type':'singleflag',
                    'flags': {
                        'TTkLayout'     : ttk.TTkLayout     ,
                        'TTkGridLayout' : ttk.TTkGridLayout ,
                        'TTkVBoxLayout' : ttk.TTkVBoxLayout ,
                        'TTkHBoxLayout' : ttk.TTkHBoxLayout } },
                'set':  { 'cb': lambda _,l: self.changeSuperLayout(l) , 'type':'singleflag',
                    'flags': {
                        'TTkLayout'     : ttk.TTkLayout     ,
                        'TTkGridLayout' : ttk.TTkGridLayout ,
                        'TTkVBoxLayout' : ttk.TTkVBoxLayout ,
                        'TTkHBoxLayout' : ttk.TTkHBoxLayout } },
            }
        }
        exclude = []
        return exceptions, exclude

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
    def _swFromWidget(wid, *args, **kwargs):
        sw = so.SuperWidget(wid=wid, *args, **kwargs)
        sw.changeSuperLayout(type(wid.layout()))
        return sw

    @staticmethod
    def swFromWidget(wid, *args, **kwargs):
        swClass = {
            ttk.TTkTextEdit: so.SuperWidgetTextEdit,
            ttk.TTkRadioButton: so.SuperWidgetRadioButton,
                }.get(type(wid),so.SuperWidget)
        return swClass._swFromWidget(wid=wid, *args, **kwargs)

    @staticmethod
    def loadDict(designer, parent, widProp):
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
            sl = sup = so.SuperLayout.slFromLayout(designer=designer, layout=layout, lay=ttk.TTkLayout(), pos=(x,y), size=(w,h), selectable=True)
            children = widProp['children']
        else:
            setLayout = 'layout' in widProp
            tui = {
                'class'  : widProp['class'],
                'params' : widProp['params'] }
            tui |= {
                'layout': {
                    'class'  : widProp['layout']['class'],
                    'params' : widProp['layout']['params'],
                    'children' : []
                    } } if setLayout else {}
            demiProp = {
                'version':'1.0.0',
                'tui': tui,
                'connections':[]
            }
            wid = ttk.TTkUiLoader.loadDict(demiProp)
            sup = so.SuperWidget.swFromWidget(designer=designer, wid=wid, pos=wid.pos())
            sl = sup._superLayout
            children = widProp['layout']['children'] if setLayout else []

        for ch in children:
            sch = SuperWidget.loadDict(designer, parent, ch)
            if issubclass(type(sl),so.SuperLayoutGrid):
                sl.layout().addWidget(sch,ch['row'],ch['col'],ch['rowspan'],ch['colspan'])
                sch._superLayout.setDropBorder(1)
            else:
                sl.layout().addWidget(sch)
                sch._superLayout.setDropBorder(0)
        return sup

    def changeSuperLayout(self, layout):
        sl = self._superLayout
        self.layout().removeWidget(sl)
        if layout == ttk.TTkVBoxLayout:
            sl = so.SuperLayoutVBox(designer=self._designer, lay=self._wid.layout(), selectable=False)
        elif layout == ttk.TTkHBoxLayout:
            sl = so.SuperLayoutHBox(designer=self._designer, lay=self._wid.layout(), selectable=False)
        elif layout == ttk.TTkGridLayout:
            sl = so.SuperLayoutGrid(designer=self._designer, lay=self._wid.layout(), selectable=False)
        else:
            sl = so.SuperLayout(    designer=self._designer, lay=self._wid.layout(), selectable=False)
        self._superLayout = sl
        self._wid.setLayout(layout())
        self.layout().addWidget(sl)
        self._designer.weModified.emit()

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
        # if self._superRootWidget: return False
        scw = so.SuperControlWidget(self)
        ttk.TTkHelper.removeOverlay()
        ttk.TTkHelper.overlay(self, scw, -1,-1, forceBoundaries=False)

    def mouseReleaseEvent(self, evt) -> bool:
        self.pushSuperControlWidget()
        self._designer.thingSelected.emit(self._wid,self)
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
        self.superMoved.emit(x,y)
        return super().move(x, y)

    def resizeEvent(self, w, h):
        self._wid.resize(w,h)
        self._wid._canvas.updateSize()
        self.superResized.emit(w,h)
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