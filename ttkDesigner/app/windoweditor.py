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

# Yaml is not included by default
# import yaml
import json
from random import randint

import TermTk as ttk

class SuperControlWidget(ttk.TTkResizableFrame):
    def __init__(self, wid, *args, **kwargs):
        self._wid = wid
        self._widPos = self._wid.pos()
        self._draggable = False
        self._mouseDelta = (0,0)
        kwargs['maxSize'] = [v+2 for v in wid.maximumSize()]
        kwargs['minSize'] = [v+2 for v in wid.minimumSize()]
        kwargs['size']    = [v+2 for v in wid.size()       ]
        super().__init__(*args, **kwargs)

    def _alignWidToPos(self, pos):
        x,y = self.pos()
        ox,oy = pos
        wx,wy = self._wid.pos()
        self._wid.move(wx+x-ox, wy+y-oy)
        self.update()
        return super().move(x,y)

    def resizeEvent(self, w, h):
        self._wid.resize(w-2,h-2)
        self._wid._canvas.updateSize()
        return super().resizeEvent(w, h)

    def mouseReleaseEvent(self, evt) -> bool:
        self._draggable = False
        return super().mouseReleaseEvent(evt)

    def mousePressEvent(self, evt):
        self._draggable = False
        self._mouseDelta = (evt.x, evt.y)
        w,h = self.size()
        x,y = evt.x, evt.y
        if x==0 or x==w-1 or y==0 or y==h-1:
            return super().mousePressEvent(evt)
        self._draggable = True
        return True

    def mouseDragEvent(self, evt):
        bkPos = self.pos()
        if self._draggable:
            x,y = self.pos()
            dx = evt.x-self._mouseDelta[0]
            dy = evt.y-self._mouseDelta[1]
            self.move(x+dx, y+dy)
            self._alignWidToPos(bkPos)
            return True
        ret = super().mouseDragEvent(evt)
        self._alignWidToPos(bkPos)
        return ret

    def paintEvent(self):
        w,h = self.size()
        self._wid.paintEvent()
        self._wid.paintChildCanvas()
        self._canvas.paintCanvas(
                self._wid.getCanvas(),
                (    1,     1, w, h), # geometry
                (    0,     0, w, h), # slice
                (    0,     0, w, h)) # bound
        self._canvas.drawBox(pos=(0,0),size=self.size())
        self._canvas.drawChar(pos=(  0,   0), char='▛')
        self._canvas.drawChar(pos=(w-1,   0), char='▜')
        self._canvas.drawChar(pos=(  0, h-1), char='▙')
        self._canvas.drawChar(pos=(w-1, h-1), char='▟')

class SuperWidget(ttk.TTkWidget):
    def __init__(self, wid, *args, **kwargs):
        self._wid = wid
        self._wid.move(*kwargs['pos'])
        self._wid._canvas.show()
        self._superRootWidget = kwargs.get('superRootWidget',False)
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
        r,g,b = randint(0,0xFF),randint(0,0xFF),randint(0,0xFF)
        self._layoutColor    = ttk.TTkColor.bg(f"#{r:02X}{g:02X}{b:02X}")
        self._layoutPadColor = ttk.TTkColor.bg(f"#{r*9//10:X}{g*9//10:X}{b*9//10:X}")
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
        def _dumpPrimitive(val):
            return val
        def _dumpTTkString(val):
            return val.toAnsi()
        def _dumpTTkColor(val):
            return str(val)
        def _dumpTTkLayout(val):
            return type(val).__name__
        def _dumpFlag(val):
            return val
        def _dumpList(val, propType):
            ret = []
            for i,t in enumerate(propType):
                if t['type'] in (int,str,float,bool):
                    ret.append(_dumpPrimitive(val[i]))
                elif type(t['type']) in (list,tuple):
                    ttk.TTkLog.warn("Feature not Implemented yet")
                elif t['type'] is ttk.TTkLayout:
                    ret.append(_dumpTTkLayout(val[i]))
                elif t['type'] is ttk.TTkString:
                    ret.append(_dumpTTkString(val[i]))
                elif t['type'] is ttk.TTkColor:
                    ret.append(_dumpTTkColor(val[i]))
                elif t['type'] in ('singleFlag','multiFlag'):
                    ret.append(_dumpFlag(val[i]))
                else:
                    ttk.TTkLog.warn("Type not Recognised")
            return ret
        children = []
        for w in self.layout().children():
            children.append(w.widget().dumpDict())
        params = {}
        for cc in reversed(type(wid).__mro__):
            # if hasattr(cc,'_ttkProperties'):
            if issubclass(cc, ttk.TTkWidget):
                ccName = cc.__name__
                if ccName in ttk.TTkUiProperties:
                    for p in ttk.TTkUiProperties[ccName]:
                        prop = ttk.TTkUiProperties[ccName][p]
                        propType = prop['get']['type']
                        propCb = prop['get']['cb']
                        # ttk.TTkLog.debug(ccName)
                        if propType in (int,str,float,bool):
                            params |= {p: _dumpPrimitive(propCb(wid))}
                        elif type(propType) in (list,tuple):
                            params |= {p: _dumpList(propCb(wid), propType)}
                        elif propType is ttk.TTkLayout:
                            params |= {p: _dumpTTkLayout(propCb(wid))}
                        elif propType is ttk.TTkString:
                            params |= {p: _dumpTTkString(propCb(wid))}
                        elif propType is ttk.TTkColor:
                            params |= {p: _dumpTTkColor(propCb(wid))}
                        elif propType in ('singleflag','multiflags'):
                            params |= {p: _dumpFlag(propCb(wid))}
                        else:
                            ttk.TTkLog.warn("Type not Recognised")

        ret = {
            'class'  : wid.__class__.__name__,
            'params' : params,
            'children': children
        }
        return ret

    def updateAll(self):
        self.update()

    def mousePressEvent(self, evt) -> bool:
        return True

    def pushSuperControlWidget(self):
        if self._superRootWidget: return False
        scw = SuperControlWidget(self)
        ttk.TTkHelper.removeOverlay()
        ttk.TTkHelper.overlay(self, scw, -1,-1, forceBoundaries=False)

    def mouseReleaseEvent(self, evt) -> bool:
        self.pushSuperControlWidget()
        self.widgetSelected.emit(self._wid,self)
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
        self.parentWidget().layout().removeWidget(self)
        self.parentWidget().update()
        return True

    def dropEvent(self, evt) -> bool:
        data = evt.data()
        hsx,hsy = evt.hotSpot()
        padt, padb, padl, padr = self._wid.getPadding()
        ttk.TTkLog.debug(f"Drop ({data.__class__.__name__}) -> pos={evt.pos()}")
        if issubclass(type(data),ttk.TTkWidget):
            if issubclass(type(data), SuperWidget):
                sw = data
                self.layout().addWidget(sw)
                data = data._wid
                sw.move(evt.x-hsx-padl, evt.y-hsy-padt)
                sw.show()
            else:
                self.layout().addWidget(sw := SuperWidget(wid=data, pos=(evt.x-hsx-padl, evt.y-hsy-padt)))
            self._wid.addWidget(data)
            data.move(evt.x-hsx-padl, evt.y-hsy-padt)
            sw.weModified = self.weModified
            sw.widgetSelected = self.widgetSelected
            self.update()
            self.weModified.emit()
            return True
        return False

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
            w,h = self.size()
            self._canvas.fill(color=self._layoutColor)
            self._canvas.fill(pos=(l,t), size=(w-r-l,h-b-t), color=self._layoutPadColor)
        else:
            self._wid.paintEvent()
            self._canvas.paintCanvas(
                    self._wid.getCanvas(),
                    (    0,     0, w, h), # geometry
                    (    0,     0, w, h), # slice
                    (    0,     0, w, h)) # bound

class WindowEditorView(ttk.TTkAbstractScrollView):
    def __init__(self, *args, **kwargs):
        self.weModified = ttk.pyTTkSignal()
        self.widgetSelected = ttk.pyTTkSignal(ttk.TTkWidget, ttk.TTkWidget)
        super().__init__(*args, **kwargs)
        self.viewChanged.connect(self._viewChangedHandler)
        self._ttk = SuperWidget(wid=ttk.TTkWidget(name = 'TTk'), pos=(4,2), size=(self.width()-8,self.height()-4), superRootWidget=True)
        self._ttk.weModified = self.weModified
        self._ttk.widgetSelected = self.widgetSelected
        self.layout().addWidget(self._ttk)

    def getTTk(self):
        return self._ttk

    def getJson(self):
        return json.dumps(self._ttk.dumpDict(), indent=1)

    def resizeEvent(self, w, h):
        self._ttk.resize(w-8,h-4)
        return super().resizeEvent(w, h)

    @ttk.pyTTkSlot()
    def _viewChangedHandler(self):
        x,y = self.getViewOffsets()
        self.layout().setOffset(-x,-y)

    def viewFullAreaSize(self):
        _,_,w,h = self.layout().fullWidgetAreaGeometry()
        return w+1, h+1

    def viewDisplayedSize(self):
        return self.size()

    def paintEvent(self):
        w,h = self.size()
        self._canvas.fill(pos=(0,0),size=(w,h), char="╳", color=ttk.TTkColor.fg("#444400")+ttk.TTkColor.bg("#000044"))

class WindowEditor(ttk.TTkAbstractScrollArea):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setViewport(wev := WindowEditorView())
        self.getTTk  = wev.getTTk
        self.getJson = wev.getJson
