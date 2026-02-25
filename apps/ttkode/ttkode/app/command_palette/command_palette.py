# MIT License
#
# Copyright (c) 2026 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

__all__ = ['TTKode_CommandPalette']

from pathlib import Path
from enum import Enum,auto
from typing import List, Tuple, Optional

import TermTk as ttk

from ttkode.app.command_palette.search_file_threading import TTKode_CP_SearchFileThreading, TTKode_CP_SearchFileItem
from ttkode.app.command_palette.command_palette_items import TTKodeCommandPaletteListItem, TTKodeCommandPaletteListItemFile

class _ListAction(Enum):
    UP=auto()
    DOWN=auto()
    SELECT=auto()


class _TTKodeCommandPaletteListWidget(ttk.TTkAbstractScrollView):
    _color_hovered = ttk.TTkColor.bg('#444444')
    _color_hilghlight = ttk.TTkColor.bg("#173C70")

    __slots__ = ('_items', '_highlight', '_hovered', 'selected')

    _items:List[TTKodeCommandPaletteListItem]
    _highlight:Optional[TTKodeCommandPaletteListItem]
    _hovered:Optional[TTKodeCommandPaletteListItem]
    selected:ttk.pyTTkSignal

    def __init__(self, **kwargs):
        self._items = []
        self._highlight = None
        self._hovered = None
        self.selected = ttk.pyTTkSignal(TTKodeCommandPaletteListItem)
        super().__init__(**kwargs)

    def viewFullAreaSize(self) -> Tuple[int,int]:
        w = self.width()
        h = len(self._items)
        return w, h

    def clean(self) -> None:
        self._highlight = None
        self._hovered = None
        self._items = []
        self.viewMoveTo(0,0)

    def extend(self, items:List[TTKodeCommandPaletteListItem]):
        self._items.extend(items)
        self._items = sorted(self._items, key=lambda x: x.sorted_key())
        self.viewChanged.emit()
        self.update()

    def _pushAction(self, action:_ListAction) -> None:
        if not self._items:
            return
        _highlight = self._highlight
        if _highlight is None:
            _highlight = self._items[0]
            self._highlight = _highlight

        _items = self._items
        ox,oy = self.getViewOffsets()
        h = self.height()

        index = _items.index(_highlight) if _highlight in _items else None
        if action is _ListAction.UP:
            index = -1 if index is None else index-1
        elif action is _ListAction.DOWN:
            index = 0 if index is None or index>=len(_items)-1 else index+1
        elif action is _ListAction.SELECT:
            if self._highlight:
                self.selected.emit(self._highlight)
            return
        else:
            index = 0
        self._highlight = _items[index]
        index = _items.index(self._highlight)
        if index < oy:
            oy = index
        elif oy+h <= index:
            oy = index-h+1
        self.viewMoveTo(ox,oy)
        self.update()

    def mouseReleaseEvent(self, evt):
        ox,oy = self.getViewOffsets()
        x,y = evt.x,evt.y
        y+=oy
        _items = self._items
        if 0 <= y < len(_items):
            self.selected.emit(_items[y])
        self.update()
        return True

    def mouseMoveEvent(self, evt):
        ox,oy = self.getViewOffsets()
        x,y = evt.x,evt.y
        y+=oy
        _items = self._items
        if 0 <= y < len(_items):
            self._hovered = _items[y]
        else:
            self._hovered = None
        self.update()
        return True

    def leaveEvent(self, evt):
        self._hovered = None
        self.update()
        return True

    def paintEvent(self, canvas):
        w,h = self.size()
        ox,oy = self.getViewOffsets()
        for i,item in enumerate(self._items[oy:oy+h]):
            color = ttk.TTkColor.RST
            if item is self._hovered:
                color = self._color_hovered
            elif item is self._highlight:
                color = self._color_hilghlight
            elif self._highlight is None and i == 0:
                color = self._color_hilghlight

            text = item.toTTkString(width=w).completeColor(color)
            canvas.fill(pos=(0,i),size=(w,1),color=color)
            canvas.drawTTkString(text=text, pos=(0,i))

class _TTKodeCommandPaletteList(ttk.TTkAbstractScrollArea):
    __slots__ = ('_list_widget', 'selected')
    selected:ttk.pyTTkSignal
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._list_widget = _TTKodeCommandPaletteListWidget()
        self.selected = self._list_widget.selected
        self.setViewport(self._list_widget)

    def clean(self) -> None:
        return self._list_widget.clean()

    def extend(self, items:List[TTKodeCommandPaletteListItem]):
        return self._list_widget.extend(items=items)

    def _pushAction(self, action:_ListAction) -> None:
        return self._list_widget._pushAction(action=action)


class TTKode_CommandPalette(ttk.TTkResizableFrame):
    __slots__ = ('_line_edit', '_cpl', '_sft')
    def __init__(self, **kwargs):
        layout = ttk.TTkGridLayout()
        self._line_edit = le = ttk.TTkLineEdit(hint='Search files by name')
        self._cpl = cpl = _TTKodeCommandPaletteList()
        self._sft = TTKode_CP_SearchFileThreading()
        layout.addWidget(le,0,0)
        layout.addWidget(cpl,1,0)
        super().__init__(layout=layout, **kwargs)
        le.textEdited.connect(self._search)
        self._sft.search_results.connect(self._process_search_results)
        self._cpl.selected.connect(self._selected_item)

    @ttk.pyTTkSlot(TTKodeCommandPaletteListItem)
    def _selected_item(self, item:TTKodeCommandPaletteListItem) -> None:
        if isinstance(item, TTKodeCommandPaletteListItemFile):
            from ttkode.proxy import ttkodeProxy
            ttkodeProxy.openFile(item._file)
            self.close()

    @ttk.pyTTkSlot(str)
    def _search(self, pattern:ttk.TTkString) -> None:
        self._cpl.clean()
        self._sft.search(pattern=pattern.toAscii())

    @ttk.pyTTkSlot(List[TTKode_CP_SearchFileItem])
    def _process_search_results(self, items:List[TTKode_CP_SearchFileItem]):
        items_path = [
            TTKodeCommandPaletteListItemFile(
                file=_f.file,
                pattern=_f.match_pattern
            ) for _f in items
        ]
        ttk.TTkLog.debug('\n'.join([str(f) for f in items]))
        self._cpl.extend(items_path)

    # def setFocus(self):
    #     return self._line_edit.setFocus()

    def keyEvent(self, evt:ttk.TTkKeyEvent) -> bool:
        if evt.type == ttk.TTkK.SpecialKey:
            # Don't Handle the special focus switch key
            if evt.key is ttk.TTkK.Key_Up:
                self._cpl._pushAction(_ListAction.UP)
                self.update()
                return True
            if evt.key is ttk.TTkK.Key_Down:
                self._cpl._pushAction(_ListAction.DOWN)
                self.update()
                return True
            if evt.key is ttk.TTkK.Key_Enter:
                self._cpl._pushAction(_ListAction.SELECT)
                self.update()
                return True
            if evt.key is ttk.TTkK.Key_Escape:
                self.pippo='Esc'
                self.close()
                return True
        if self._line_edit.keyEvent(evt=evt):
            self._line_edit.setFocus()
            return True
        return False

    def paintEvent(self, canvas:ttk.TTkCanvas) -> None:
        super().paintEvent(canvas)
        w,h = self.size()
        canvas.drawChar(pos=(  0,  0), char='╭')
        canvas.drawChar(pos=(w-1,  0), char='╮')
        canvas.drawChar(pos=(  0,h-1), char='╰')
        canvas.drawChar(pos=(w-1,h-1), char='╯')
