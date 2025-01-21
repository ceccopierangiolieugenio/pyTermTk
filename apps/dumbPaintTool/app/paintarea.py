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

__all__ = ['PaintArea','PaintScrollArea','CanvasLayer']

import TermTk as ttk

from .canvaslayer import CanvasLayer
from .const       import ToolType
from .glbls       import glbls

class PaintArea(ttk.TTkAbstractScrollView):
    __slots__ = ('_transparentColor',
                 '_documentPos','_documentSize',
                 '_mouseMove', '_mouseDrag', '_mousePress', '_mouseRelease',
                 '_moveData','_resizeData',
                 '_clipboard',
                 '_tool',
                 '_glyph', '_glyphColor', '_glyphEnabled', '_areaBrush')

    def __init__(self, *args, **kwargs):
        self._transparentColor = {'base':ttk.TTkColor.RST,'dim':ttk.TTkColor.RST}
        self._glyph = 'X'
        self._glyphColor = ttk.TTkColor.RST
        self._glyphEnabled = True
        self._areaBrush = CanvasLayer()
        self._areaBrush.changed.connect(self.update)
        self._moveData = None
        self._resizeData = None
        self._mouseMove = None
        self._mouseDrag = None
        self._mousePress   = None
        self._mouseRelease = None
        self._tool = 0
        self._documentPos    = (6,3)
        self._documentSize   = ( 0, 0)
        self._clipboard = ttk.TTkClipboard()
        super().__init__(*args, **kwargs)
        self.setTrans(ttk.TTkColor.bg('#FF00FF'))
        self.resizeCanvas(*glbls.documentSize)
        self.setFocusPolicy(ttk.TTkK.ClickFocus + ttk.TTkK.TabFocus)

        glbls.brush.toolTypeChanged.connect(self.setTool)
        glbls.brush.areaChanged.connect(    self.setAreaBrush)
        glbls.brush.glyphChanged.connect(       self.updateGlyph)
        glbls.brush.colorChanged.connect(       self.updateGlyph)
        glbls.brush.glyphEnabledChanged.connect(self.updateGlyph)

        glbls.layers.changed.connect(self.update)
        glbls.layers.layerAdded.connect(self.update)
        glbls.layers.layerDeleted.connect(self.update)
        glbls.layers.layerSelected.connect(self.update)
        glbls.layers.layersOrderChanged.connect(self.update)

        # Retrieve the default values
        self.setTool(      glbls.brush.toolType())
        self.updateGlyph()

    def _getGeometry(self):
        dx,dy = self._documentPos
        dw,dh = self._documentSize
        ww,wh = self.size()
        x1,y1 = min(0,dx),min(0,dy)
        x2,y2 = max(dx+dw,ww),max(dy+dh,wh)
        for cl in glbls.layers.layers():
            lx,ly = cl.pos()
            lw,lh = cl.size()
            x1 = min(x1,dx+lx)
            y1 = min(y1,dy+ly)
            x2 = max(x2,dx+lx+lw)
            y2 = max(y2,dy+ly+lh)
        # ttk.TTkLog.debug(f"{x1=},{y1=},{x2-x1=},{y2-y1=}")
        return x1,y1,x2-x1,y2-y1

    def _retuneGeometry(self):
            ox, oy = self.getViewOffsets()
            dx,dy = self._documentPos
            x1,y1,_,_ = self._getGeometry()
            dx1,dy1 = max(0,dx,dx-x1),max(0,dy,dy-y1)
            self._documentPos = dx1,dy1
            self.viewChanged.emit()
            # dx,dy = self._documentPos
            # self.chan
            self.viewMoveTo(ox+dx1-dx,oy+dy1-dy)
            # If the area move to be adapted to the
            # Negative coordinates, the reference values used in
            # mouse press, moveData, resizeData need to be
            # adapted to the new topology
            if mp:=self._mousePress:
                mpx,mpy = mp
                self._mousePress = (mpx-x1,mpy-y1)
            if md:=self._moveData:
                mx,my=md['pos']
                md['pos']=(mx+dx1-dx,my+dy1-dy)
            # if rd:=self._resizeData:
            #     rx,ry,rw,rh=rd['geometry']
            #     # rd['geometry']=(rx+dx1-dx,ry+dy1-dy,rw,rh)

    def viewFullAreaSize(self) -> tuple[int,int]:
        _,_,w,h = self._getGeometry()
        return w+1,h+1

    def viewDisplayedSize(self) -> tuple:
        return self.size()

    def maximumWidth(self):   return 0x10000
    def maximumHeight(self):  return 0x10000
    def minimumWidth(self):   return 0
    def minimumHeight(self):  return 0

    def resizeCanvas(self, w, h):
        self._documentSize = (w,h)
        glbls.documentSize = (w,h)
        self._retuneGeometry()
        self.update()

    def superResize(self,x,y,w,h):
        dx,dy = self._documentPos
        dw,dh = self._documentSize
        if (x,y,w,h) == (dx,dy,dw,dh): return
        if w<0: x=dx;w=dw
        if h<0: y=dy;h=dh
        if self._documentPos  != (x,y):
            diffx = dx-x
            diffy = dy-y
            for l in glbls.layers.layers():
                lx,ly = l.pos()
                l.move(lx+diffx,ly+diffy)
            self._documentPos = (x,y)
        self._documentSize = (w,h)
        glbls.documentSize = (w,h)
        self.update()

    def exportLayer(self, full=False, palette=True, crop=True) -> dict:
        if glbls.layers.selected():
            return glbls.layers.selected().exportLayer(full=full,palette=palette,crop=crop)
        return {}

    def exportDocument(self, full=True, palette=True, crop=True) -> dict:
        pw,ph = self._documentSize
        outData  = {
            'type':'DumbPaintTool/Document',
            'version':'1.0.1',
            'size':(pw,ph),
            'layers':[cl.exportLayer(full=full,palette=palette,crop=crop) for cl in reversed(glbls.layers.layers())]}
        return outData

    def exportImage(self) -> str:
        pw,ph = self._documentSize
        image = ttk.TTkCanvas(width=pw,height=ph)
        for cl in reversed(glbls.layers.layers()):
            lx,ly = cl.pos()
            cl.drawInCanvas(pos=(lx,ly),canvas=image)
        return image.toAnsi()

    def leaveEvent(self, evt):
        self._mouseMove = None
        self._moveData  = None
        if current := glbls.layers.selected():
            current.cleanPreview()
        self.update()
        return super().leaveEvent(evt)

    @ttk.pyTTkSlot(ToolType)
    def setTool(self, tool):
        self._tool = tool
        self.update()

    def _handleAction(self):
        if not glbls.layers.selected(): return
        dx,dy = self._documentPos
        dw,dh = self._documentSize
        ox, oy = self.getViewOffsets()
        mp = self._mousePress
        mm = self._mouseMove
        md = self._mouseDrag
        mr = self._mouseRelease
        l = glbls.layers.selected()
        lx,ly = l.pos()

        if self._tool & ToolType.PICKGLYPH:
            if mp:
                mpx,mpy = mp
                color = ttk.TTkColor.RST
                glyph = None
                for lm in glbls.layers.layers():
                    lmx,lmy = lm.pos()
                    if lm.isOpaque(mpx-lmx-dx,mpy-lmy-dy):
                        _gl, _co = lm.glyphColorAt(mpx-lmx-dx,mpy-lmy-dy)
                        if not glyph and color == ttk.TTkColor.RST:
                            glyph = _gl
                            color = _co
                        elif color.hasBackground():
                            if _co.hasBackground():
                                if color.hasForeground():
                                    color = color.foreground() + _co.background()
                                else:
                                    color = _co.background()
                        else:
                            break
                glbls.brush.setColor(color)
                glbls.brush.setGlyph(glyph if glyph else ' ')
            if mr:
                glbls.brush.setToolType(self._tool & ~ToolType.PICKGLYPH)
                self._mousePress   = None
                self._mouseMove    = None
                self._mouseDrag    = None
                self._mouseRelease = None
        elif self._tool & ToolType.MOVE and mp and not md:
            if self._tool & ToolType.RESIZE and not md:
                mpx,mpy = mp
                self._resizeData = None
                def _getSelected(_x,_y,_w,_h):
                    _selected = ttk.TTkK.NONE
                    if _x <= mpx < _x+_w and mpy == _y:      _selected |= ttk.TTkK.TOP
                    if _x <= mpx < _x+_w and mpy == _y+_h-1: _selected |= ttk.TTkK.BOTTOM
                    if _y <= mpy < _y+_h and mpx == _x:      _selected |= ttk.TTkK.LEFT
                    if _y <= mpy < _y+_h and mpx == _x+_w-1: _selected |= ttk.TTkK.RIGHT
                    return _selected
                # Main Area Resize Borders
                if selected :=  _getSelected(dx-1,dy-1,dw+2,dh+2):
                    self._resizeData = {'type':PaintArea,'selected':selected,'cb':self.superResize,'geometry':(dx,dy,dw,dh)}
                elif  l:
                    # Selected Layer Resize Borders
                    lx,ly = l.pos()
                    lw,lh = l.size()
                    if selected := _getSelected(dx+lx-1,dy+ly-1,lw+2,lh+2):
                        self._resizeData = {'type':CanvasLayer,'selected':selected,'cb':l.superResize,'geometry':(lx,ly,lw,lh)}
            if not self._resizeData:
                # Get The Layer to Move
                self._moveData = None
                for lm in glbls.layers.layers():
                    mpx,mpy = mp
                    lmx,lmy = lm.pos()
                    self._moveData = {'type':PaintArea,'pos':(dx,dy)}
                    if lm.isOpaque(mpx-lmx-dx,mpy-lmy-dy):
                        tml = lm
                        self._moveData = {'type':CanvasLayer,'pos':tml.pos(),'layer':tml}
                        glbls.layers.selectLayer(lm)
                        break

        elif self._tool & ToolType.MOVE and mp and md:
            # Move/Resize Tool
            if self._tool & ToolType.RESIZE and (rData:=self._resizeData):
                _rx,_ry,_rw,_rh = rData['geometry']
                _rdx,_rdy,_rdw,_rdh=(_rx,_ry,_rw,_rh)
                mpx,mpy = mp
                mdx,mdy = md
                diffx = mdx-mpx
                diffy = mdy-mpy
                if rData['selected'] & ttk.TTkK.TOP:    _rdh-=diffy ; _rdy+=diffy
                if rData['selected'] & ttk.TTkK.BOTTOM: _rdh+=diffy
                if rData['selected'] & ttk.TTkK.LEFT:   _rdw-=diffx ; _rdx+=diffx
                if rData['selected'] & ttk.TTkK.RIGHT:  _rdw+=diffx
                rData['cb'](_rdx,_rdy,_rdw,_rdh)
            if not self._resizeData and (mData:=self._moveData):
                mpx,mpy = mp
                mdx,mdy = md
                pdx,pdy = mdx-mpx,mdy-mpy
                if mData['type']==CanvasLayer:
                    px,py = self._moveData['pos']
                    self._moveData['layer'].move(px+pdx,py+pdy)
                    glbls.layers.selectLayer(self._moveData['layer'])
                elif mData['type']==PaintArea:
                    px,py = self._moveData['pos']
                    self._documentPos = (px+pdx,py+pdy)
            self._retuneGeometry()

        elif self._tool & ToolType.BRUSH:
            if mp and self._tool & ToolType.PICKAREA:
                glbls.brush.setToolType(self._tool & ~ToolType.PICKAREA)
                mpx,mpy = mp
                for lm in glbls.layers.layers():
                    lmx,lmy = lm.pos()
                    if lm.isOpaque(mpx-lmx-dx,mpy-lmy-dy):
                        glbls.brush.setArea(lm.trim().toTTkString())
                        break
                self._mousePress   = None
                self._mouseMove    = None
                self._mouseDrag    = None
                self._mouseRelease = None
            elif self._tool & ToolType.PICKAREA:
                pass # Do not show any preview if we are in picking mode
            elif mp or md:
                if md: mx,my = md
                else:  mx,my = mp
                preview=False
                transparent=self._tool & ToolType.TRANSPARENT
                if self._tool & ToolType.GLYPH:
                    glbls.layers.selected().placeGlyph(mx-lx-dx,my-ly-dy,self._glyph,self._glyphColor,self._glyphEnabled,preview)
                if self._tool & ToolType.AREA:
                    glbls.layers.selected().placeArea(mx-lx-dx,my-ly-dy,self._areaBrush,transparent,preview)
            elif mm:
                mx,my = mm
                preview=True
                transparent=self._tool & ToolType.TRANSPARENT
                if self._tool & ToolType.GLYPH:
                    glbls.layers.selected().placeGlyph(mx-lx-dx,my-ly-dy,self._glyph,self._glyphColor,self._glyphEnabled,preview)
                if self._tool & ToolType.AREA:
                    glbls.layers.selected().placeArea(mx-lx-dx,my-ly-dy,self._areaBrush,transparent,preview)

        elif self._tool in (ToolType.RECTEMPTY, ToolType.RECTFILL):
            if mr and mp:
                mpx,mpy = mp
                mrx,mry = mr
                preview=False
                glbls.layers.selected().placeFill((mpx-lx-dx,mpy-ly-dy,mrx-lx-dx,mry-ly-dy),self._tool,self._glyph,self._glyphColor,self._glyphEnabled,preview)
            elif md and mp:
                mpx,mpy = mp
                mrx,mry = md
                preview=True
                glbls.layers.selected().placeFill((mpx-lx-dx,mpy-ly-dy,mrx-lx-dx,mry-ly-dy),self._tool,self._glyph,self._glyphColor,self._glyphEnabled,preview)
            elif mm:
                mpx,mpy = mm
                mrx,mry = mm
                preview=True
                glbls.layers.selected().placeFill((mpx-lx-dx,mpy-ly-dy,mrx-lx-dx,mry-ly-dy),self._tool,self._glyph,self._glyphColor,self._glyphEnabled,preview)
        self.update()

    def mouseMoveEvent(self, evt) -> bool:
        ox, oy = self.getViewOffsets()
        self._mouseMove = (evt.x+ox,evt.y+oy)
        self._mouseDrag = None
        self._handleAction()
        return True

    def mouseDragEvent(self, evt) -> bool:
        ox, oy = self.getViewOffsets()
        self._mouseDrag=(evt.x+ox,evt.y+oy)
        self._mouseMove= None
        self._handleAction()
        return True

    def mousePressEvent(self, evt) -> bool:
        ox, oy = self.getViewOffsets()
        self._mousePress=(evt.x+ox,evt.y+oy)
        self._moveData     = None
        self._mouseMove    = None
        self._mouseDrag    = None
        self._mouseRelease = None
        self._handleAction()
        return True

    def mouseReleaseEvent(self, evt) -> bool:
        ox, oy = self.getViewOffsets()
        self._mouseRelease=(evt.x+ox,evt.y+oy)
        self._mouseMove   = None
        self._handleAction()
        self._moveData     = None
        self._resizeData   = None
        self._mousePress   = None
        self._mouseDrag    = None
        self._mouseRelease = None
        glbls.saveSnapshot()
        return super().mousePressEvent(evt)

    def keyEvent(self, evt) -> bool:
        ret = None
        cl = glbls.layers.selected()
        if   cl and evt.key == ttk.TTkK.Key_Up:
            x,y = cl.pos()
            cl.move(x,y-1)
            ret = True
        elif cl and evt.key == ttk.TTkK.Key_Down:
            x,y = cl.pos()
            cl.move(x,y+1)
            ret = True
        elif cl and evt.key == ttk.TTkK.Key_Left:
            x,y = cl.pos()
            cl.move(x-1,y)
            ret = True
        elif cl and evt.key == ttk.TTkK.Key_Right:
            x,y = cl.pos()
            cl.move(x+1,y)
            ret = True
        elif evt.mod==ttk.TTkK.ControlModifier and evt.key == ttk.TTkK.Key_V:
            self.paste()
            ret = True
        elif evt.mod==ttk.TTkK.ControlModifier and evt.key == ttk.TTkK.Key_C:
            if glbls.layers.selected():
                text = glbls.layers.selected().toTTkString()
                self.copy(text)
                ret = True
        elif cl and evt.key == ttk.TTkK.Key_Delete:
            glbls.layers.delLayer()
            glbls.saveSnapshot()
        else:
            return super().keyEvent(evt)
        self._retuneGeometry()
        self.update()
        if ret is None:
            return super().keyEvent(evt)
        return ret

    @ttk.pyTTkSlot()
    def paste(self):
        txt = self._clipboard.text()
        self.pasteEvent(txt)

    @ttk.pyTTkSlot(ttk.TTkString)
    def copy(self, text):
        self._clipboard.setText(text)

    def pasteEvent(self, txt:str):
        glbls.layers.addLayer().importTTkString(ttk.TTkString(txt))
        glbls.saveSnapshot()
        self.update()
        return True

    @ttk.pyTTkSlot(ttk.TTkString)
    def setAreaBrush(self, ab:ttk.TTkString):
        self._areaBrush = CanvasLayer()
        self._areaBrush.importTTkString(ab)

    @ttk.pyTTkSlot()
    def updateGlyph(self):
        self.setGlyph(glbls.brush.glyph())
        self.setGlyphColor(glbls.brush.color())
        self._glyphEnabled = glbls.brush.glyphEnabled()

    def glyph(self):
        return self._glyph
    @ttk.pyTTkSlot(str)
    def setGlyph(self, glyph):
        if len(glyph) <= 0:
            return
        if isinstance(glyph,str):
            self._glyph = glyph[0]
        if isinstance(glyph,ttk.TTkString):
            self._glyph = glyph.charAt(0)
            self._glyphColor = glyph.colorAt(0)

    def glyphColor(self):
        return self._glyphColor
    @ttk.pyTTkSlot(ttk.TTkColor)
    def setGlyphColor(self, color):
        self._glyphColor = color

    @ttk.pyTTkSlot(ttk.TTkColor)
    def setTrans(self, color:ttk.TTkColor):
        r,g,b = color.bgToRGB()
        self._transparentColor = {
            'base':color,
            'dim':     ttk.TTkColor.bg(f'#{int(r*0.3):02x}{int(g*0.3):02x}{int(b*0.3):02x}'),
            'layer':   ttk.TTkColor.bg(f'#{int(r*0.6):02x}{int(g*0.6):02x}{int(b*0.6):02x}'),
            'layerDim':ttk.TTkColor.bg(f'#{int(r*0.2):02x}{int(g*0.2):02x}{int(b*0.2):02x}')}
        self.update()

    def paintEvent(self, canvas:ttk.TTkCanvas):
        dx,dy = self._documentPos
        ox, oy = self.getViewOffsets()
        dw,dh = self._documentSize
        dox,doy = dx-ox,dy-oy
        cw,ch = canvas.size()
        # w=min(cw,dw)
        # h=min(ch,dh)
        tcb = self._transparentColor['base']
        tcd = self._transparentColor['dim']

        if cl:=glbls.layers.selected():
            tclb = self._transparentColor['layer']
            tcld = self._transparentColor['layerDim']
            lx,ly = cl.pos()
            lw,lh = cl.size()
            canvas.fill(pos=(0     ,ly+doy),size=(cw,lh),color=tcld)
            canvas.fill(pos=(lx+dox,0     ),size=(lw,ch),color=tcld)
            canvas.fill(pos=(lx+dox,ly+doy),size=(lw,lh),color=tclb)
        canvas.fill(pos=(dx-ox,dy-oy),size=(dw,dh),color=tcb)
        canvas.fill(pos=(0    ,dy-oy-1), size=(cw,1),color=tcd)
        canvas.fill(pos=(0    ,dy-oy+dh),size=(cw,1),color=tcd)
        canvas.fill(pos=(dx-ox-2 ,0    ),size=(2,ch),color=tcd)
        canvas.fill(pos=(dx-ox+dw,0    ),size=(2,ch),color=tcd)

        for cl in reversed(glbls.layers.layers()):
            lx,ly = cl.pos()
            cl.drawInCanvas(pos=(lx+dox,ly+doy),canvas=canvas)

        if self._tool & ToolType.RESIZE:
            rd = self._resizeData
            def _drawResizeBorders(_rx,_ry,_rw,_rh,_sel,_color=ttk.TTkColor.RST):
                selColor = ttk.TTkColor.YELLOW + ttk.TTkColor.BG_BLUE
                # canvas.drawBox(pos=_pos,size=_size)
                canvas.drawText(pos=(_rx      ,_ry      ),text='─'*_rw, color=selColor if _sel & ttk.TTkK.TOP    else _color)
                canvas.drawText(pos=(_rx      ,_ry+_rh-1),text='─'*_rw, color=selColor if _sel & ttk.TTkK.BOTTOM else _color)
                for _y in range(_ry,_ry+_rh):
                    canvas.drawText(pos=(_rx      ,_y),text='│',color=selColor if _sel & ttk.TTkK.LEFT  else _color)
                    canvas.drawText(pos=(_rx+_rw-1,_y),text='│',color=selColor if _sel & ttk.TTkK.RIGHT else _color)
                canvas.drawChar(pos=(_rx      ,_ry      ), char='▛', color=_color)
                canvas.drawChar(pos=(_rx+_rw-1,_ry      ), char='▜', color=_color)
                canvas.drawChar(pos=(_rx      ,_ry+_rh-1), char='▙', color=_color)
                canvas.drawChar(pos=(_rx+_rw-1,_ry+_rh-1), char='▟', color=_color)

            sMain  = rd['selected'] if rd and rd['type'] == PaintArea   else ttk.TTkK.NONE
            sLayer = rd['selected'] if rd and rd['type'] == CanvasLayer else ttk.TTkK.NONE

            if cl:=glbls.layers.selected():
                lx,ly = cl.pos()
                lw,lh = cl.size()
                _drawResizeBorders(lx+dx-ox-1, ly+dy-oy-1, lw+2, lh+2, sLayer)

            _drawResizeBorders(dx-ox-1, dy-oy-1, dw+2, dh+2, sMain, _color=ttk.TTkColor.YELLOW)


class PaintScrollArea(ttk.TTkAbstractScrollArea):
    def __init__(self, pwidget:PaintArea, **kwargs):
        super().__init__(**kwargs)
        self.setViewport(pwidget)