#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2021 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

import os
import sys
import random
import argparse

sys.path.append(os.path.join(sys.path[0],'../../libs/pyTermTk'))
import TermTk as ttk

class TestUndoRedo(ttk.TTkWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._doc = kwargs.get('document', ttk.TTkTextDocument())
        self._doc.contentsChanged.connect(self.update)
        self._doc.undoAvailable.connect(lambda _: self.update())
        self._doc.redoAvailable.connect(lambda _: self.update())

    def mousePressEvent(self, evt) -> bool:
        self.update()
        return super().mousePressEvent(evt)

    def paintEvent(self, canvas):
        return
        def _getSelect(i,p):
            selSt = p.selectionStart()
            selEn = p.selectionEnd()
            if selSt.line == i: ss = selSt.pos
            if selEn.line == i: se = selEn.pos
            if selSt.line < i:  ss = 0
            if selEn.line > i:  se = len(s)
            if selSt.line > i:  ss = len(s)
            if selEn.line < i:  se = 0
            return ss, se

        self._canvas.drawText(pos=(2,0), text=f"Undo/Redo Status:")
        self._canvas.drawText(pos=(2,1), text=f"Id{self._doc._diffId} Fw:{self._doc._diffIdFw}")
        y = 3
        for i,d in enumerate(self._doc._diffs):
            i1 = d._i1
            i2 = d._i2
            c1 = d._cursor1
            c2 = d._cursor2
            self._canvas.drawText(pos=(4,y), text=f"i1={i1} i2={i2}")
            y +=1

            if i == self._doc._diffId:
                if self._doc._diffIdFw:
                    pre1 = f'{i} * '
                    pre2 = f'{i} *>'
                else:
                    pre1 = f'{i} *>'
                    pre2 = f'{i} * '
            else:
                pre1 = f'{i}   '
                pre2 = f'{i}   '
            if not d._slice1:
                self._canvas.drawText(pos=(2,y), text=f'{pre1}s1 (x)-><- [Empty]')
                y +=1
            for i,s in enumerate(d._slice1, i1):
                p = c1._properties[0]
                ss, se = _getSelect(i, p)
                # self._canvas.drawText(pos=(2,y), text=f'l1:{selSt.line} p1:{selSt.pos} l2:{selEn.line} p2:{selEn.pos} {ss=} {se=}')
                # y += 1
                s = s.setColor(color=ttk.TTkColor.bg("#004444"), posFrom=ss, posTo=se)
                self._canvas.drawText(pos=(2,y), text=f'{pre1}s1 ({i})->'+s+'<-')
                y +=1
            if not d._slice2:
                self._canvas.drawText(pos=(2,y), text=f'{pre2}s2 (x)-><- [Empty]')
                y +=1
            for i,s in enumerate(d._slice2, i1):
                p = c2._properties[0]
                ss, se = _getSelect(i, p)
                # self._canvas.drawText(pos=(2,y), text=f'l1:{selSt.line} p1:{selSt.pos} l2:{selEn.line} p2:{selEn.pos} {ss=} {se=}')
                # y += 1
                s = s.setColor(color=ttk.TTkColor.bg("#004444"), posFrom=ss, posTo=se)
                self._canvas.drawText(pos=(2,y), text=f'{pre2}s2 ({i})->'+s+'<-')
                y +=1

def demoTextEdit1(root=None, document=None):
    te = ttk.TTkTextEdit(parent=root, document=document)
    te.setReadOnly(False)

def demoTextEdit2(root=None, document=None):
    te = ttk.TTkTextEdit(parent=root, document=document)
    te.setLineWrapMode(ttk.TTkK.WidgetWidth)
    te.setWordWrapMode(ttk.TTkK.WordWrap)
    te.setReadOnly(False)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', help='Full Screen (default)', action='store_true')
    parser.add_argument('-w', help='Windowed',    action='store_true')
    args = parser.parse_args()
    windowed = args.w

    ttk.TTkLog.use_default_file_logging()

    root = ttk.TTk(sigmask=(
                    ttk.TTkTerm.Sigmask.CTRL_Q |
                    ttk.TTkTerm.Sigmask.CTRL_S |
                    ttk.TTkTerm.Sigmask.CTRL_Z |
                    # ttk.TTkTerm.Sigmask.CTRL_C ))
                    0 ))
    if windowed:
        rootTree = ttk.TTkWindow(parent=root,pos = (0,0), size=(70,40), title="Test Text Edit", layout=ttk.TTkGridLayout(), border=True)
    else:
        rootTree = root
        root.setLayout(ttk.TTkGridLayout())

    hsplit = ttk.TTkSplitter()
    vsplit = ttk.TTkSplitter(parent=hsplit, orientation=ttk.TTkK.VERTICAL)
    document = ttk.TTkTextDocument(text="Text Edit DEMO Eugenio Parodi\nabc def ghi jkf lmn\nLorem ipsomething.")

    TestUndoRedo(parent=hsplit, document=document)

    demoTextEdit1(vsplit, document)
    demoTextEdit2(vsplit, document)

    rootTree.layout().addWidget(hsplit,0,0,1,2)
    rootTree.layout().addWidget(quitbtn := ttk.TTkButton(border=True, text="Quit", maxWidth=6),1,0)
    rootTree.layout().addWidget(ttk.TTkKeyPressView(maxHeight=3),1,1)
    quitbtn.clicked.connect(root.quit)
    root.mainloop()

if __name__ == "__main__":
    main()