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

class TTkTableWidget(TTkAbstractScrollView):
    '''TTkTableWidget'''

    classStyle = {
                'default':     {
                    'color': TTkColor.RST,
                    'lineColor': TTkColor.fg("#444444"),
                    'headerColor': TTkColor.fg("#ffffff")+TTkColor.bg("#444444")+TTkColor.BOLD,
                    'selectedColor': TTkColor.bg("#888800")+TTkColor.BOLD,
                    'separatorColor': TTkColor.fg("#555555")+TTkColor.bg("#444444")},
                'disabled':    {
                    'color': TTkColor.fg("#888888"),
                    'lineColor': TTkColor.fg("#888888"),
                    'headerColor': TTkColor.fg("#888888"),
                    'selectedColor': TTkColor.fg("#888888"),
                    'separatorColor': TTkColor.fg("#888888")},
            }

    __slots__ = ( '_tableModel',
                  '_vHeaderSize',
                  '_showVSeparators', '_showHSeparators',
                  '_colsPos', '_rowsPos',
                  '_selectedId', '_selected', '_hSeparatorSelected', '_vSeparatorSelected',
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
        self._selected = None
        self._selectedId = None
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

    def _refreshLayout(self):
        rows = self._tableModel.rowCount()
        cols = self._tableModel.columnCount()
        self._vHeaderSize = 1+max(len(self._tableModel.headerData(_p, TTkK.VERTICAL)) for _p in range(rows) )
        if self._showVSeparators:
            self._colsPos  = [(1+x)*11 for x in range(cols)]
        else:
            self._colsPos  = [(1+x)*10 for x in range(cols)]
        if self._showHSeparators:
            self._rowsPos     = [(1+x)*2  for x in range(rows)]
        else:
            self._rowsPos     = [(1+x)    for x in range(rows)]
        self._selected = [[False]*cols for _ in range(rows)]

    # Overridden function
    def viewFullAreaSize(self) -> tuple[int, int]:
        w = self._vHeaderSize+self._colsPos[-1]
        h = 1+self._rowsPos[-1]
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

    def mousePressEvent(self, evt) -> bool:
        x,y = evt.x, evt.y
        ox, oy = self.getViewOffsets()
        vx = self._vHeaderSize
        self._hSeparatorSelected = None
        self._vSeparatorSelected = None

        # Handle Header Events
        if y == 0:
            x += ox-vx
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
        elif x<vx:
            y += oy
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
        vx = self._vHeaderSize
        if self._hSeparatorSelected is not None:
            x += ox-vx
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
            y += oy
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

    def paintEvent(self, canvas) -> None:
        style = self.currentStyle()

        color:TTkColor= style['color']
        lineColor:TTkColor= style['lineColor']
        headerColor:TTkColor= style['headerColor']
        selectedColor:TTkColor= style['selectedColor']
        separatorColor:TTkColor= style['separatorColor']

        ox,oy = self.getViewOffsets()
        w,h = self.size()

        rows = self._tableModel.rowCount()
        cols = self._tableModel.columnCount()
        rp = self._rowsPos
        cp = self._colsPos
        vx = self._vHeaderSize

        # Draw Cells
        sliceCol=list(zip([-1]+cp,cp))
        sliceRow=list(zip([0]+rp,rp))
        for row in range(rows):
            ya,yb = sliceRow[row]
            if ya>h+oy: break
            if yb<oy: continue
            for col in range(cols):
                xa,xb = sliceCol[col]
                if xa>w+ox: break
                if xb<ox: continue
                txt = self._tableModel.data(row, col)
                cellColor = selectedColor if self._selected[row][col] else color.mod(col,row)
                if isinstance(txt,TTkString): pass
                elif type(txt) == str: txt = TTkString(txt, cellColor)
                else:                  txt = TTkString(f"{txt}", cellColor)
                for i,line in enumerate(txt.split('\n')):
                    y = 1+i+ya-oy
                    if y == 1+yb-oy: break
                    canvas.drawTTkString(pos=(vx+1+xa-ox,y), text=line, width=xb-xa-1, color=cellColor)
                canvas.fill(pos=(vx+1+xa-ox,2+i+ya-oy),size=(xb-xa-1,yb-ya-i-1),color=cellColor)
                # Draw the VSeparator of the cell
                lineColorMix = color.mod(0,row) + lineColor
                if cellColor==TTkColor.RST or col<cols-1:
                    canvas.fill(pos=(vx-ox+xb,1+ya-oy), size=(1,yb-ya), char='│', color=lineColorMix)
                else:
                    canvas.fill(pos=(vx-ox+xb,1+ya-oy), size=(1,yb-ya), char=' ', color=lineColorMix)

        # Draw H-Header first:
        for col in range(cols):
            txt = self._tableModel.headerData(col,TTkK.HORIZONTAL)
            if isinstance(txt,TTkString): pass
            elif type(txt) == str: txt = TTkString(txt)
            else:                  txt = TTkString(f"{txt}")
            hx  = 0 if col==0 else cp[col-1]+1
            hx1 = cp[col]
            canvas.drawText(pos=(vx+hx-ox,0), text=txt, width=hx1-hx, color=headerColor)
            if col == self._sortColumn:
                s = '▼' if self._sortOrder == TTkK.AscendingOrder else '▲'
                canvas.drawText(pos=(vx+hx1-ox-1,0), text=s, color=headerColor)

        vHSeparator = TTkString('▐', separatorColor)
        # Draw V-Header :
        for row in range(rows):
            ya,yb = sliceRow[row]
            if ya>h+oy: break
            if yb<oy: continue
            if (1+yb-oy)<1: continue
            txt = self._tableModel.headerData(row,TTkK.VERTICAL)
            if isinstance(txt,TTkString): pass
            elif type(txt) == str: txt = TTkString(txt)
            else:                  txt = TTkString(f"{txt}")
            canvas.drawTTkString(pos=(0,1+ya-oy), text=txt, width=vx, color=headerColor)
            canvas.drawTTkString(pos=(vx-1,1+ya-oy), text=vHSeparator)
            for i in range(1,yb-ya):
                # canvas.drawTTkString(pos=(0,i+1+ya-oy), text=' ', width=vx, color=headerColor)
                canvas.drawTTkString(pos=(0,i+1+ya-oy), text=vHSeparator, width=vx, alignment=TTkK.RIGHT_ALIGN, color=headerColor)
            # canvas.drawText(pos=(0,1+ya-oy), text='lkjslkj', color=headerColor)

        hline = TTkString('╾'+'╌'*(vx-2), color=headerColor) + vHSeparator
        lineC  = TTkString()
        lineB  = TTkString()
        # Draw header separators, cols
        for sx in cp:
            if sx<ox: continue
            lineC += TTkString('─'*(sx-len(lineC))+'┼')
            lineB += TTkString('─'*(sx-len(lineB))+'┴')
            canvas.drawChar(pos=(vx+sx-ox,0), char='╿', color=headerColor)

        # Draw rows separators
        for row in range(rows):
            y = rp[row]-oy
            if y > h : break
            if y < 1: continue
            bgA:TTkColor = c if (c:=color.mod(0,row).background()) else TTkColor.RST
            bgB:TTkColor = c if (c:=color.mod(0,row+1).background()) else TTkColor.RST
            lineColorMix:TTkColor = bgA + lineColor
            if bgA == bgB == TTkColor.RST:
                if row<rows-1:
                    canvas.drawTTkString(pos=(vx-ox,y), text=lineC, color=lineColorMix)
                    canvas.drawChar(pos=(vx-ox+cp[-1],y), char="┤", color=lineColorMix)
                else:
                    canvas.drawTTkString(pos=(vx-ox,y), text=lineB, color=lineColorMix)
                    canvas.drawChar(pos=(vx-ox+cp[-1],y), char="┘", color=lineColorMix)
            elif bgA == bgB:
                canvas.drawTTkString(pos=(vx-ox,y), text=lineC, color=lineColorMix)
                canvas.drawChar(pos=(vx-ox+cp[-1],y), char="─", color=lineColorMix)
            else:
                if row>=rows-1 or bgB==TTkColor.RST:
                    canvas.fill(char='▀', pos=(vx,y), size=(1-ox+cp[-1],1), color=bgA.invertFgBg())
                else:
                    canvas.fill(char='▄', pos=(vx,y), size=(1-ox+cp[-1],1), color=bgA+bgB.invertFgBg())

            canvas.drawTTkString(pos=(  0,y), text=hline)

        # Draw Top/Left Corner
        canvas.drawText(pos=(0,0), text=' ', width=vx, color=separatorColor.invertFgBg() )

        selectedColorInv = selectedColor.background().invertFgBg()
        # Draw Select H-Edges
        for row in range(rows):
            y = rp[row]-oy
            if y > h : break
            if y < 1: continue
            # Draw Top Line
            # selMixA:TTkColor = c.background()+selectedColorInv if (row < rows-1 and (c:=color.mod(0,row  ).background())) else selectedColorInv
            # selMixB:TTkColor = c.background()+selectedColorInv if (row < rows-1 and (c:=color.mod(0,row+1).background())) else selectedColorInv
            selMixA:TTkColor = selectedColorInv
            selMixB:TTkColor = selectedColorInv
            for col in range(cols):
                xa,xb = sliceCol[col]
                xa = max(vx,vx+xa-ox)
                xb = max(vx,vx+xb-ox)
                if xa>w: break
                if xb<vx: continue
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
            ya = max(1,1+ya-oy)
            yb = max(1,1+yb-oy)
            if ya>h: break
            if yb<1: continue
            # Draw Top Line
            # selMix:TTkColor = c.background()+selectedColorInv if (c:=color.mod(0,row).background()) else selectedColorInv
            selMix:TTkColor = selectedColorInv
            for col in range(cols):
                x = cp[col]-ox+vx
                if x>w: break
                if x<vx: continue
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
            y = rp[row]-oy
            if y > h : break
            if y < 1: continue
            for col in range(cols):
                x = cp[col]-ox+vx
                if x>w: break
                if x<vx: continue
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





