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


__all__ = ['TTkTableWidget']

from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.cfg import TTkCfg
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.string import TTkString
from TermTk.TTkCore.color import TTkColor
# from TermTk.TTkWidgets.TTkModelView.tablewidgetitem import TTkTableWidgetItem
from TermTk.TTkAbstract.abstractscrollview import TTkAbstractScrollView
from TermTk.TTkAbstract.abstracttablemodel import TTkAbstractTableModel
from TermTk.TTkCore.signal import pyTTkSignal, pyTTkSlot

class _DefaultTableModel(TTkAbstractTableModel):
    def __init__(self, **args):
        super().__init__(**args)
    def rowCount(self):
        return 15
    def columnCount(self):
        return 10
    def data(self, row, col):
        return f"{row}x{col}"

class _HeaderView():
    '''_HeaderView
    This is a placeholder for a future "TTkHeaderView"
    '''
    __slots__ = ('_visible','visibilityUpdated')
    def __init__(self) -> None:
        self.visibilityUpdated = pyTTkSignal(bool)
        self._visible = True

    @pyTTkSlot(bool)
    def setVisible(self, visible: bool):
        '''setVisible'''
        if self._visible == visible: return
        self._visible = visible
        self.visibilityUpdated.emit(visible)

    @pyTTkSlot()
    def show(self):
        '''show'''
        self.setVisible(True)

    @pyTTkSlot()
    def hide(self):
        '''hide'''
        self.setVisible(False)

    def isVisible(self) -> bool:
        return self._visible

class TTkTableWidget(TTkAbstractScrollView):
    '''TTkTableWidget'''

    classStyle = {
                'default':     {
                    'color':          TTkColor.RST,
                    'lineColor':      TTkColor.fg("#444444"),
                    'headerColor':    TTkColor.fg("#FFFFFF")+TTkColor.bg("#444444")+TTkColor.BOLD,
                    'hoverColor':     TTkColor.fg("#4444FF")+TTkColor.bg("#AAAA44")+TTkColor.BOLD,
                    'selectedColor':  TTkColor.bg("#888800"),
                    'separatorColor': TTkColor.fg("#555555")+TTkColor.bg("#444444")},
                'disabled':    {
                    'color':          TTkColor.fg("#888888"),
                    'lineColor':      TTkColor.fg("#888888"),
                    'headerColor':    TTkColor.fg("#888888"),
                    'hoverColor':     TTkColor.bg("#888888"),
                    'selectedColor':  TTkColor.fg("#888888"),
                    'separatorColor': TTkColor.fg("#888888")},
            }

    __slots__ = ( '_tableModel',
                  '_vHeaderSize', '_hHeaderSize',
                  '_showVSeparators', '_showHSeparators',
                  '_verticalHeader', '_horizontallHeader',
                  '_colsPos', '_rowsPos',
                  '_internal',
                  '_selected', '_hSeparatorSelected', '_vSeparatorSelected',
                  '_hoverPos', '_dragPos',
                  '_sortColumn', '_sortOrder',
                  # Signals
                  # 'itemChanged', 'itemClicked', 'itemDoubleClicked', 'itemExpanded', 'itemCollapsed', 'itemActivated'
                  )

    def __init__(self, *,
                 tableModel:TTkAbstractTableModel=None,
                 vSeparator:bool=True, hSeparator:bool=True,
                 **kwargs) -> None:
        # Signals
        # self.itemActivated     = pyTTkSignal(TTkTableWidgetItem, int)
        # self.itemChanged       = pyTTkSignal(TTkTableWidgetItem, int)
        # self.itemClicked       = pyTTkSignal(TTkTableWidgetItem, int)
        # self.itemDoubleClicked = pyTTkSignal(TTkTableWidgetItem, int)
        # self.itemExpanded      = pyTTkSignal(TTkTableWidgetItem)
        # self.itemCollapsed     = pyTTkSignal(TTkTableWidgetItem)

        self._showHSeparators = vSeparator
        self._showVSeparators = hSeparator
        self._verticalHeader    = _HeaderView()
        self._horizontallHeader = _HeaderView()
        self._selected = None
        self._hoverPos = None
        self._dragPos = None
        self._internal = {}
        self._hSeparatorSelected = None
        self._vSeparatorSelected = None
        self._sortColumn = -1
        self._sortOrder = TTkK.AscendingOrder
        self._tableModel = tableModel if tableModel else _DefaultTableModel()
        self._refreshLayout()
        super().__init__(**kwargs)
        self.setMinimumHeight(1)
        self.setFocusPolicy(TTkK.ClickFocus)
        # self._rootItem = TTkTableWidgetItem(expanded=True)
        # self.clear()
        self.setPadding(1,0,0,0)
        self.viewChanged.connect(self._viewChangedHandler)
        self._verticalHeader.visibilityUpdated.connect(self.update)
        self._horizontallHeader.visibilityUpdated.connect(self.update)

    def _refreshLayout(self):
        rows = self._tableModel.rowCount()
        cols = self._tableModel.columnCount()
        self._vHeaderSize = vhs= 1+max(len(self._tableModel.headerData(_p, TTkK.VERTICAL)) for _p in range(rows) )
        self._hHeaderSize = hhs= 1
        if self._showVSeparators:
            self._colsPos  = [(1+x)*11 for x in range(cols)]
        else:
            self._colsPos  = [(1+x)*10 for x in range(cols)]
        if self._showHSeparators:
            self._rowsPos     = [1+x*2  for x in range(rows)]
        else:
            self._rowsPos     = [1+x    for x in range(rows)]
        self._selected = [[False]*cols for _ in range(rows)]

    # Overridden function
    def viewFullAreaSize(self) -> tuple[int, int]:
        w = self._vHeaderSize+self._colsPos[-1]
        h = self._hHeaderSize+self._rowsPos[-1]
        return w,h

    # Overridden function
    def viewDisplayedSize(self) -> tuple[int, int]:
        return self.size()

    def setSelection(self, pos, size, flags:TTkK.TTkItemSelectionModel):
        x,y = pos
        w,h = size
        for line in self._selected[y:y+h]:
            line[x:x+w]=[True]*w
        self.update()

    @pyTTkSlot()
    def _viewChangedHandler(self) -> None:
        x,y = self.getViewOffsets()
        self.layout().setOffset(-x,-y)

    def verticalHeader(self):
        pass
    def horizontalHeader(self):
        pass

    def setModel(self, model) -> None:
        self._tableModel = model
        self._refreshLayout()
        self.viewChanged.emit()

    def setSortingEnabled(self, enable) -> None:
        pass
    def resizeColumnsToContents(self) -> None:
        pass

    def focusOutEvent(self) -> None:
        self._hSeparatorSelected = None
        self._vSeparatorSelected = None

    def leaveEvent(self, evt):
        self._hoverPos = None
        self.update()
        return super().leaveEvent(evt)

    def _findCell(self, x, y):
        vhs = self._vHeaderSize
        hhs = self._hHeaderSize
        ox, oy = self.getViewOffsets()
        x,y = x+ox-vhs, y+oy-hhs
        rp = self._rowsPos
        cp = self._colsPos

        for row,py in enumerate(rp):
            if py>y:
                break
        for col,px in enumerate(cp):
            if px>x:
                break
        return row,col

    def mouseMoveEvent(self, evt) -> bool:
        vhs = self._vHeaderSize
        hhs = self._hHeaderSize
        x,y = evt.x,evt.y
        self._hoverPos = None
        if x<vhs or y<hhs:
            self.update()
            return True
        self._hoverPos = self._findCell(x,y)
        self.update()
        return True

    def mousePressEvent(self, evt) -> bool:
        x,y = evt.x, evt.y
        ox, oy = self.getViewOffsets()
        vhs = self._vHeaderSize
        hhs = self._hHeaderSize

        self._hSeparatorSelected = None
        self._vSeparatorSelected = None

        # Handle Header Events
        if y < hhs:
            x += ox-vhs
            for i, c in enumerate(self._colsPos):
                if x == c:
                    # I-th separator selected
                    self._hSeparatorSelected = i
                    self.update()
                    break
                elif x < c:
                    # # I-th header selected
                    # order = not self._sortOrder if self._sortColumn == i else TTkK.AscendingOrder
                    # self.sortItems(i, order)
                    break
            return True
        elif x < vhs:
            y += oy-hhs
            for i, r in enumerate(self._rowsPos):
                if y == r:
                    # I-th separator selected
                    self._vSeparatorSelected = i
                    self.update()
                    break
                elif y < r:
                    # # I-th header selected
                    # order = not self._sortOrder if self._sortColumn == i else TTkK.AscendingOrder
                    # self.sortItems(i, order)
                    break
            return True
        else:
            row,col = self._findCell(x,y)
            self._dragPos = [(row,col),(row,col)]
            if evt.mod==TTkK.ControlModifier:
                self._selected[row][col] = not self._selected[row][col]
            else:
                self._selected[row][col] = True
            self._hoverPos = None
            self.update()
            return True
        return True

    def mouseDragEvent(self, evt) -> bool:
        '''
        ::

            columnPos       (Selected = 2)
                0       1        2          3   4
            ----|-------|--------|----------|---|
            Mouse (Drag) Pos
                                    ^
            I consider at least 4 char (3+1) as spacing
            Min Selected Pos = (Selected+1) * 4

        '''
        x,y = evt.x, evt.y
        ox, oy = self.getViewOffsets()
        vhs = self._vHeaderSize
        hhs = self._hHeaderSize
        if self._dragPos and not self._hSeparatorSelected and not self._vSeparatorSelected:
            self._dragPos[1] = self._findCell(x,y)
            self.update()
            return True
        if self._hSeparatorSelected is not None:
            x += ox-vhs
            ss = self._hSeparatorSelected
            pos = max((ss+1)*4, x)
            diff = pos - self._colsPos[ss]
            # Align the previous Separators if pushed
            for i in range(ss):
                self._colsPos[i] = min(self._colsPos[i], pos-(ss-i)*4)
            # Align all the other Separators relative to the selection
            for i in range(ss, len(self._colsPos)):
                self._colsPos[i] += diff
            # self._alignWidgets()
            self.viewChanged.emit()
            self.update()
            return True
        if self._vSeparatorSelected is not None:
            y += oy-hhs
            ss = self._vSeparatorSelected
            pos = max((ss+1)*2, y)
            diff = pos - self._rowsPos[ss]
            # Align the previous Separators if pushed
            for i in range(ss):
                self._rowsPos[i] = min(self._rowsPos[i], pos-(ss-i)*2)
            # Align all the other Separators relative to the selection
            for i in range(ss, len(self._rowsPos)):
                self._rowsPos[i] += diff
            # self._alignWidgets()
            self.viewChanged.emit()
            self.update()
            return True
        return False

    def mouseReleaseEvent(self, evt) -> bool:
        if self._dragPos:
            rows = self._tableModel.rowCount()
            cols = self._tableModel.columnCount()
            state = True
            (rowa,cola),(rowb,colb) = self._dragPos
            if evt.mod==TTkK.ControlModifier:
                state = self._selected[rowa][cola]
            else:
                self._selected = [[False]*cols for _ in range(rows)]
            cola,colb=min(cola,colb),max(cola,colb)
            rowa,rowb=min(rowa,rowb),max(rowa,rowb)
            for line in self._selected[rowa:rowb+1]:
                line[cola:colb+1] = [state]*(colb-cola+1)
        self._hoverPos = None
        self._dragPos = None
        self.update()
        return True

    #   -1  X
    #        <-(0,0)->│<-(1,0)->│<-(2,0)->│<-(3,0)->│
    #    1   ─────────┼─────────┼─────────┼─────────┼
    #        <-(0,1)->│<-(1,1)->│<-(2,1)->│<-(3,1)->│
    #    3   ─────────┼─────────┼─────────┼─────────┼
    #        <-(0,2)->│<-(1,2)->│<-(2,2)->│<-(3,2)->│
    #    4   ─────────┼─────────┼─────────┼─────────┼
    #        <-(0,3)->│<-(1,3)->│<-(2,3)->│<-(3,3)->│ h-cell = 5 = 10-(4+1)
    #                 │ abc     │         │         │
    #                 │ de      │         │         │
    #                 │         │         │         │
    #                 │         │         │         │
    #   10   ─────────┼─────────┼─────────┼─────────┼
    #        <-(0,4)->│<-(1,4)->│<-(2,4)->│<-(3,4)->│
    #   12   ─────────┼─────────┼─────────┼─────────┼
    #        <-(0,5)->│<-(1,5)->│<-(2,5)->│<-(3,5)->│
    #   14   ─────────┼─────────┼─────────┼─────────┼
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    def paintEvent(self, canvas) -> None:
        style = self.currentStyle()

        color:TTkColor= style['color']
        lineColor:TTkColor= style['lineColor']
        headerColor:TTkColor= style['headerColor']
        hoverColor:TTkColor= style['hoverColor']
        selectedColor:TTkColor= style['selectedColor']
        separatorColor:TTkColor= style['separatorColor']

        vHSeparator = TTkString('▐', separatorColor)

        ox,oy = self.getViewOffsets()
        w,h = self.size()

        rows = self._tableModel.rowCount()
        cols = self._tableModel.columnCount()
        rp = self._rowsPos
        cp = self._colsPos
        vhs = self._vHeaderSize
        hhs = self._hHeaderSize

        sliceCol=list(zip([-1]+cp,cp))
        sliceRow=list(zip([-1]+rp,rp))

        def _drawCell(_col,_row,_xa,_xb,_ya,_yb,_color):
                txt = self._tableModel.data(_row, _col)
                if isinstance(txt,TTkString): pass
                elif type(txt) == str: txt = TTkString(txt, _color)
                else:                  txt = TTkString(f"{txt}", _color)
                txt = txt.completeColor(_color)
                for i,line in enumerate(txt.split('\n')):
                    y = i+_ya+1
                    if y == _yb: break
                    canvas.drawTTkString(pos=(1+_xa,y), text=line, width=_xb-_xa-1, color=_color)
                canvas.fill(pos=(1+_xa,y+1),size=(_xb-_xa-1,_yb-y),color=_color)

        # Draw Cells
        for row in range(rows):
            ya,yb = sliceRow[row]
            ya,yb = ya+hhs-oy, yb+hhs-oy
            if ya>h  : break
            if yb<hhs: continue
            for col in range(cols):
                xa,xb = sliceCol[col]
                xa,xb = xa+vhs-ox, xb+vhs-ox
                if xa>w  : break
                if xb<vhs: continue
                cellColor = selectedColor if self._selected[row][col] else color.mod(col,row)
                _drawCell(col,row,xa,xb,ya,yb,cellColor)

                lineColorMix = color.mod(0,row) + lineColor
                if cellColor==TTkColor.RST or col<cols-1:
                    canvas.fill(pos=(xb,ya), size=(1,yb-ya), char='│', color=lineColorMix)
                else:
                    canvas.fill(pos=(xb,ya), size=(1,yb-ya), char=' ', color=lineColorMix)


        hline = TTkString()
        lineC  = TTkString()
        lineB  = TTkString()
        # Draw header separators, cols
        for sx in cp:
            if sx<ox: continue
            lineC += TTkString('─'*(sx-len(lineC))+'┼')
            lineB += TTkString('─'*(sx-len(lineB))+'┴')

        # Draw rows separators
        for row in range(rows):
            y = rp[row]-oy+hhs
            if y > h  : break
            if y < hhs: continue
            bgA:TTkColor = c if (c:=color.mod(0,row).background()) else TTkColor.RST
            bgB:TTkColor = c if (c:=color.mod(0,row+1).background()) else TTkColor.RST
            lineColorMix:TTkColor = bgA + lineColor
            if bgA == bgB == TTkColor.RST:
                if row<rows-1:
                    canvas.drawTTkString(pos=(vhs-ox,y), text=lineC, color=lineColorMix)
                    canvas.drawChar(pos=(vhs-ox+cp[-1],y), char="┤", color=lineColorMix)
                else:
                    canvas.drawTTkString(pos=(vhs-ox,y), text=lineB, color=lineColorMix)
                    canvas.drawChar(pos=(vhs-ox+cp[-1],y), char="┘", color=lineColorMix)
            elif bgA == bgB:
                canvas.drawTTkString(pos=(vhs-ox,y), text=lineC, color=lineColorMix)
                canvas.drawChar(pos=(vhs-ox+cp[-1],y), char="─", color=lineColorMix)
            else:
                if row>=rows-1 or bgB==TTkColor.RST:
                    canvas.fill(char='▀', pos=(vhs,y), size=(1-ox+cp[-1],1), color=bgA.invertFgBg())
                else:
                    canvas.fill(char='▄', pos=(vhs,y), size=(1-ox+cp[-1],1), color=bgA+bgB.invertFgBg())

            canvas.drawTTkString(pos=(  vhs,y), text=hline)

        # Draw Top/Left Corner
        canvas.drawText(pos=(0,0), text=' ', width=vhs, color=separatorColor.invertFgBg() )

        selectedColorInv = selectedColor.background().invertFgBg()
        # Draw Select H-Edges
        for row in range(rows):
            y = rp[row]-oy+hhs
            if y > h  : break
            if y < hhs: continue
            # Draw Top Line
            # selMixA:TTkColor = c.background()+selectedColorInv if (row < rows-1 and (c:=color.mod(0,row  ).background())) else selectedColorInv
            # selMixB:TTkColor = c.background()+selectedColorInv if (row < rows-1 and (c:=color.mod(0,row+1).background())) else selectedColorInv
            selMixA:TTkColor = selectedColorInv
            selMixB:TTkColor = selectedColorInv
            for col in range(cols):
                xa,xb = sliceCol[col]
                xa = max(vhs,vhs+xa-ox)
                xb = max(vhs,vhs+xb-ox)
                if xa>w: break
                if xb<vhs: continue
                if row < rows-1:
                    chId = (
                        0x01 * self._selected[row  ][col  ] +
                        0x04 * self._selected[row+1][col  ] )
                else:
                    chId = 0x01 * self._selected[row  ][col]
                if not chId: continue
                if chId == 0x01:
                    canvas.fill(char='▀', pos=(xa,y), size=(xb-xa,1), color=selMixB)
                elif chId == 0x04:
                    canvas.fill(char='▄', pos=(xa,y), size=(xb-xa,1), color=selMixA)
                elif chId == (0x04|0x01):
                    canvas.fill(char='─', pos=(xa,y), size=(xb-xa,1), color=selectedColor)

        # Draw Select V-Edges
        for row in range(rows):
            ya,yb = sliceRow[row]
            ya = max(hhs,hhs+ya-oy)
            yb = max(hhs,hhs+yb-oy)
            if ya>h: break
            if yb<hhs: continue
            # Draw Top Line
            # selMix:TTkColor = c.background()+selectedColorInv if (c:=color.mod(0,row).background()) else selectedColorInv
            selMix:TTkColor = selectedColorInv
            for col in range(cols):
                x = cp[col]-ox+vhs
                if x>w: break
                if x<vhs: continue
                if col < cols-1:
                    chId = (
                        0x01 * self._selected[row][col  ] +
                        0x02 * self._selected[row][col+1] )
                else:
                    chId = (0x01+0x02) * self._selected[row][col]
                if not chId: continue
                if chId == 0x01:
                    canvas.fill(char='▌', pos=(x,ya), size=(1,yb-ya), color=selMix)
                elif chId == 0x02:
                    canvas.fill(char='▐', pos=(x,ya), size=(1,yb-ya), color=selMix)
                elif chId == (0x01|0x02) and col < cols-1:
                    canvas.fill(char='│', pos=(x,ya), size=(1,yb-ya), color=selectedColor)
                elif chId == (0x01|0x02):
                    canvas.fill(char=' ', pos=(x,ya), size=(1,yb-ya), color=selectedColor)

        # Draw Select corners
        for row in range(rows):
            y = rp[row]-oy+hhs
            if y > h : break
            if y < hhs: continue
            for col in range(cols):
                x = cp[col]-ox+vhs
                if x>w: break
                if x<vhs: continue
                if row<rows-1 and col<cols-1:
                    chId = (
                        0x01 * self._selected[row  ][col  ] +
                        0x02 * self._selected[row  ][col+1] +
                        0x04 * self._selected[row+1][col  ] +
                        0x08 * self._selected[row+1][col+1] )
                elif col<cols-1:
                    chId = (
                        0x01 * self._selected[row  ][col  ] +
                        0x02 * self._selected[row  ][col+1] )
                elif row<rows-1:
                    chId = (
                        (0x01+0x02) * self._selected[row  ][col  ] +
                        (0x04+0x08) * self._selected[row+1][col  ] )
                else:
                    chId = (
                        (0x01+0x02) * self._selected[row  ][col  ] )

                if not chId: continue
                if chId == 0x0F:
                    if col<cols-1:
                        canvas.drawChar(char='┼',pos=(x,y),color=selectedColor)
                    else:
                        canvas.drawChar(char='─',pos=(x,y),color=selectedColor)
                else:
                    char = [
                        # 0x00 0x01 0x02 0x03
                          ' ', '▘', '▝', '▀',
                        # 0x04 0x05 0x06 0x07
                          '▖', '▌', '▞', '▛',
                        # 0x08 0x09 0x0A 0x0B
                          '▗', '▚', '▐', '▜',
                        # 0x0C 0x0D 0x0E 0x0F
                          '▄', '▙', '▟', '█'][chId]
                    canvas.drawChar(char=char,pos=(x,y),color=selectedColorInv)

        if self._hoverPos:
            row,col = self._hoverPos
            ya,yb = sliceRow[row]
            xa,xb = sliceCol[col]
            ya,yb = ya+hhs-oy, yb+hhs-oy
            xa,xb = xa+vhs-ox, xb+vhs-ox
            _drawCell(col,row,xa,xb,ya,yb,hoverColor)

            # Draw Borders
            # Top, Bottom
            hoverColorInv = hoverColor.background().invertFgBg()
            canvas.drawTTkString(pos=(xa,ya), text=TTkString('▗'+('▄'*(xb-xa-1))+'▖',hoverColorInv))
            canvas.drawTTkString(pos=(xa,yb), text=TTkString('▝'+('▀'*(xb-xa-1))+'▘',hoverColorInv))
            # Left, Right
            canvas.fill(char='▐',pos=(xa,ya+1), size=(1,yb-ya-1), color=hoverColorInv)
            canvas.fill(char='▌',pos=(xb,ya+1), size=(1,yb-ya-1), color=hoverColorInv)

        if self._dragPos:
            (rowa,cola),(rowb,colb) = self._dragPos
            cola,colb=min(cola,colb),max(cola,colb)
            rowa,rowb=min(rowa,rowb),max(rowa,rowb)
            xa = sliceCol[cola][0]-ox+vhs
            xb = sliceCol[colb][1]-ox+vhs
            ya = sliceRow[rowa][0]-oy+hhs
            yb = sliceRow[rowb][1]-oy+hhs

            hoverColorInv = hoverColor.background().invertFgBg()
            canvas.drawTTkString(pos=(xa,ya), text=TTkString('▗'+('▄'*(xb-xa-1))+'▖',hoverColorInv))
            canvas.drawTTkString(pos=(xa,yb), text=TTkString('▝'+('▀'*(xb-xa-1))+'▘',hoverColorInv))
            canvas.fill(char='▐',pos=(xa,ya+1), size=(1,yb-ya-1), color=hoverColorInv)
            canvas.fill(char='▌',pos=(xb,ya+1), size=(1,yb-ya-1), color=hoverColorInv)

        # Draw H-Header first:
        for col in range(cols):
            txt = self._tableModel.headerData(col,TTkK.HORIZONTAL)
            if isinstance(txt,TTkString): pass
            elif type(txt) == str: txt = TTkString(txt)
            else:                  txt = TTkString(f"{txt}")
            hx  = 0 if col==0 else cp[col-1]+1
            hx1 = cp[col]
            canvas.drawText(pos=(vhs+hx-ox,0), text=txt, width=hx1-hx, color=headerColor)
            if col == self._sortColumn:
                s = '▼' if self._sortOrder == TTkK.AscendingOrder else '▲'
                canvas.drawText(pos=(vhs+hx1-ox-1,0), text=s, color=headerColor)
            canvas.drawChar(pos=(vhs+hx1-ox,0), char='╿', color=headerColor)

        # Draw V-Header :
        hlineHead = TTkString('╾'+'╌'*(vhs-2), color=headerColor) + vHSeparator
        for row in range(rows):
            ya = sliceRow[row][0]-oy+hhs
            yb = sliceRow[row][1]-oy+hhs
            if ya>h  : break
            if yb<hhs: continue
            txt = self._tableModel.headerData(row,TTkK.VERTICAL)
            if isinstance(txt,TTkString): pass
            elif type(txt) == str: txt = TTkString(txt)
            else:                  txt = TTkString(f"{txt}")
            canvas.drawTTkString(pos=(0    ,ya+1), text=txt, width=vhs, color=headerColor)
            canvas.drawTTkString(pos=(vhs-1,ya+1), text=vHSeparator)
            for y in range(ya+2,yb):
                canvas.drawTTkString(pos=(0,y), text=vHSeparator, width=vhs, alignment=TTkK.RIGHT_ALIGN, color=headerColor)
            canvas.drawTTkString(pos=(0,yb), text=hlineHead)





