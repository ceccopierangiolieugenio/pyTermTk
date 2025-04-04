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

__all__ = ['highlightersFormLayout']

import copy

from . import TloggCfg, TloggGlbl

from TermTk import *

def highlightersFormLayout(win):
    '''
    This form is inspired by glogg "Filters..." form
    '''

    colors = copy.deepcopy(TloggCfg.colors)

    leftRightLayout = TTkHBoxLayout()
    leftLayout        = TTkGridLayout()
    rightLayout       = TTkGridLayout()
    bottomRightLayout = TTkGridLayout()
    leftRightLayout.addItem(leftLayout)
    leftRightLayout.addItem(rightLayout)

    frameColors = TTkFrame(border=True, layout=TTkGridLayout())
    leftLayout.addWidget(frameColors,0,0,1,5)

    listColors = TTkList(parent=frameColors, dragDropMode=TTkK.DragDropMode.AllowDragDrop)

    addButton    = TTkButton(text="+",maxWidth=3)
    removeButton = TTkButton(text="-",maxWidth=3)
    upButton     = TTkButton(text="▲",maxWidth=3)
    downButton   = TTkButton(text="▼",maxWidth=3)

    leftLayout.addWidget(addButton       ,1,0)
    leftLayout.addWidget(removeButton    ,1,1)
    leftLayout.addWidget(TTkSpacer() ,1,2)
    leftLayout.addWidget(upButton        ,1,3)
    leftLayout.addWidget(downButton      ,1,4)

    rightLayout.addWidget(TTkLabel(text="Pattern:"),0,0)
    rightLayout.addWidget(pattern:=TTkLineEdit(text="-----"),0,1)
    rightLayout.addWidget(TTkLabel(text="Ignore Case:"),1,0)
    rightLayout.addWidget(ignoreCase:=TTkCheckbox(),1,1)
    rightLayout.addWidget(TTkLabel(text="FG Color:"),2,0)
    rightLayout.addWidget(fgColor := TTkColorButtonPicker(border=False, color=TTkColor.fg('#eeeeee') ),2,1)
    rightLayout.addWidget(TTkLabel(text="BG Color:"),3,0)
    rightLayout.addWidget(bgColor := TTkColorButtonPicker(border=False, color=TTkColor.bg('#333333') ),3,1)
    rightLayout.addWidget(TTkSpacer() ,4,0,1,2)

    rightLayout.addItem(bottomRightLayout ,5,0,1,2)
    bottomRightLayout.addWidget(applyBtn  := TTkButton(text="Apply",  border=True, maxHeight=3),0,1)
    bottomRightLayout.addWidget(cancelBtn := TTkButton(text="Cancel", border=True, maxHeight=3),0,2)
    bottomRightLayout.addWidget(okBtn     := TTkButton(text="OK",     border=True, maxHeight=3),0,3)

    def _move(offset):
        def _moveUpDown():
            if items := listColors.selectedItems():
                item = items[0]
                index = listColors.indexOf(item)
                listColors.moveItem(index,index+offset)
        return _moveUpDown
    upButton.clicked.connect(_move(-1))
    downButton.clicked.connect(_move(1))

    def _addCallback():
        color = {'pattern':"<PATTERN>", 'ignorecase':True, 'fg':"#FFFFFF", 'bg':"#000000" }
        colors.append(color)
        listColors.addItem(item=color['pattern'],data=color)
    addButton.clicked.connect(_addCallback)

    def _removeCallback():
        # Clear all the signals
        pattern.textEdited.clear()
        ignoreCase.clicked.clear()
        fgColor.colorSelected.clear()
        bgColor.colorSelected.clear()
        if items := listColors.selectedItems():
            colors.remove(items[0].data)
            listColors.removeItem(items[0])
    removeButton.clicked.connect(_removeCallback)

    def _saveColors():
        colors = []
        for item in listColors.items():
            colors.append(item.data())
        TloggCfg.colors = colors
        TloggCfg.save(searches=False, filters=False, colors=True, options=False)
        TloggGlbl.refreshViews()
        # TTkHelper.updateAll()

    applyBtn.clicked.connect(_saveColors)
    okBtn.clicked.connect(_saveColors)
    okBtn.clicked.connect(win.close)
    cancelBtn.clicked.connect(win.close)

    @ttk.pyTTkSlot(TTkAbstractListItem)
    def _listCallback(item):
        if color:=item.data():
            # Clear all the signals
            pattern.textEdited.clear()
            ignoreCase.clicked.clear()
            fgColor.colorSelected.clear()
            bgColor.colorSelected.clear()
            # Config the color widgets
            pattern.setText(color['pattern'])
            ignoreCase.setCheckState(TTkK.Checked if color['ignorecase'] else TTkK.Unchecked)
            fgColor.setColor(TTkColor.bg(color['fg']))
            bgColor.setColor(TTkColor.bg(color['bg']))
            # Connect the actions
            ## Pattern Line Edit
            @pyTTkSlot(str)
            def _setPattern(p:TTkString):
                item.setText(str(p))
                color['pattern'] = str(p)
            pattern.textEdited.connect(_setPattern)
            ## Case Sensitivity checkbox
            def _setCase(c):color['ignorecase'] = c
            ignoreCase.clicked.connect(_setCase)
            ## Color Button
            def _setFg(c):color['fg'] = c.getHex(TTkK.Background)
            def _setBg(c):color['bg'] = c.getHex(TTkK.Background)
            fgColor.colorSelected.connect(_setFg)
            bgColor.colorSelected.connect(_setBg)


    listColors.itemClicked.connect(_listCallback)

    for i,color in enumerate(colors):
        # ali = TTkAbstractListItem(text=color['pattern'],data=color)
        listColors.addItem(item=color['pattern'],data=color)

    return leftRightLayout

def highlightersForm(root=None):
    preferencesLayout = TTkGridLayout(columnMinWidth=1)
    frame = TTkFrame(parent=root, layout=preferencesLayout, border=0)

    frameColors = TTkFrame(border=True, title="Highlighters...", layout=highlightersFormLayout())
    preferencesLayout.addWidget(frameColors,0,0)

    return frame