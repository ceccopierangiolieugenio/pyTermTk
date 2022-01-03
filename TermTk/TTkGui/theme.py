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

from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.helper import TTkHelper
import TermTk.TTkGui.fileicon_nerd  as fi_nerd
import TermTk.TTkGui.fileicon_utf8  as fi_utf8
import TermTk.TTkGui.fileicon_ascii as fi_ascii
import TermTk.TTkGui.draw_utf8      as draw_utf8
import TermTk.TTkGui.draw_ascii     as draw_ascii


class TTkTheme():
    NERD  = {'file':fi_nerd,  'draw':draw_utf8}
    UTF8  = {'file':fi_utf8,  'draw':draw_utf8}
    ASCII = {'file':fi_ascii, 'draw':draw_ascii}

    hline     = draw_utf8.TTkTheme.hline
    vline     = draw_utf8.TTkTheme.vline
    box       = draw_utf8.TTkTheme.box
    grid      = draw_utf8.TTkTheme.grid
    buttonBox = draw_utf8.TTkTheme.buttonBox
    hscroll   = draw_utf8.TTkTheme.hscroll
    vscroll   = draw_utf8.TTkTheme.vscroll
    tree      = draw_utf8.TTkTheme.tree
    menuBar   = draw_utf8.TTkTheme.menuBar
    tab       = draw_utf8.TTkTheme.tab
    braille   = draw_utf8.TTkTheme.braille

    getFileIcon     = fi_utf8.FileIcon.getIcon
    folderIconClose = fi_utf8.FileIcon.folder_close
    folderIconOpen  = fi_utf8.FileIcon.folder_open

    def loadTheme(theme):
        TTkTheme.hline     = theme['draw'].TTkTheme.hline
        TTkTheme.vline     = theme['draw'].TTkTheme.vline
        TTkTheme.box       = theme['draw'].TTkTheme.box
        TTkTheme.grid      = theme['draw'].TTkTheme.grid
        TTkTheme.buttonBox = theme['draw'].TTkTheme.buttonBox
        TTkTheme.hscroll   = theme['draw'].TTkTheme.hscroll
        TTkTheme.vscroll   = theme['draw'].TTkTheme.vscroll
        TTkTheme.tree      = theme['draw'].TTkTheme.tree
        TTkTheme.menuBar   = theme['draw'].TTkTheme.menuBar
        TTkTheme.tab       = theme['draw'].TTkTheme.tab
        TTkTheme.braille   = theme['draw'].TTkTheme.braille

        TTkTheme.getFileIcon     = theme['file'].FileIcon.getIcon
        TTkTheme.folderIconClose = theme['file'].FileIcon.folder_close
        TTkTheme.folderIconOpen  = theme['file'].FileIcon.folder_open

        TTkHelper.updateAll()



    frameBorderColor = TTkColor.RST
    frameTitleColor  = TTkColor.fg("#dddddd")+TTkColor.bg("#222222")

    windowBorderColor = TTkColor.RST
    windowBorderColorFocus = TTkColor.fg("#ffff55")

    buttonBoxGrid = 1
    buttonBoxGridClicked = 0
    buttonTextColor   = TTkColor.fg("#dddd88")+TTkColor.bg("#000044")
    buttonBorderColor = TTkColor.RST
    buttonTextColorClicked   = TTkColor.fg("#ffffdd")+TTkColor.BOLD
    buttonBorderColorClicked = TTkColor.fg("#dddddd")+TTkColor.BOLD
    buttonTextColorFocus     = buttonTextColor   + TTkColor.BOLD
    buttonBorderColorFocus   = TTkColor.fg("#ffff00") + TTkColor.BOLD


    menuButtonShortcutColor = TTkColor.fg("#dddddd") + TTkColor.UNDERLINE
    menuButtonColor = TTkColor.BOLD
    menuButtonBorderColor = frameBorderColor
    menuButtonColorClicked =  TTkColor.fg("#ffff88")
    menuButtonBorderColorClicked = frameBorderColor

    listColor            = TTkColor.RST
    listColorSelected    = TTkColor.fg("#ffffdd")+TTkColor.bg("#000044") + TTkColor.BOLD
    listColorHighlighted = TTkColor.bg("#000088") + TTkColor.BOLD

    lineEditTextColor       = TTkColor.fg("#dddddd")+TTkColor.bg("#222222")
    lineEditTextColorFocus  = TTkColor.fg("#dddddd")+TTkColor.bg("#000044")

    comboboxContentColor      = TTkColor.fg("#dddd88")+TTkColor.bg("#111111")
    comboboxBorderColor       = buttonBorderColor
    comboboxContentColorFocus      = TTkColor.fg("#ffff88")+TTkColor.bg("#111111")
    comboboxBorderColorFocus       = buttonBorderColorFocus

    checkboxContentColor      = buttonTextColor
    checkboxBorderColor       = buttonBorderColor
    checkboxContentColorFocus = buttonTextColorFocus
    checkboxBorderColorFocus  = buttonBorderColorFocus

    radioButtonContentColor      = buttonTextColor
    radioButtonBorderColor       = buttonBorderColor
    radioButtonContentColorFocus = buttonTextColorFocus
    radioButtonBorderColorFocus  = buttonBorderColorFocus

    tabColor       = TTkColor.fg("#aaaaaa")
    tabOffsetColor = TTkColor.RST
    tabBorderColor = frameBorderColor
    tabSelectColor = TTkColor.fg("#ffff88")+TTkColor.bg("#000066")+TTkColor.BOLD
    tabColorFocus       = TTkColor.fg("#aaaaaa")
    tabOffsetColorFocus = tabOffsetColor
    tabBorderColorFocus = TTkColor.fg("#ffff88")
    tabSelectColorFocus = TTkColor.fg("#ffff88")+TTkColor.bg("#000066")+TTkColor.BOLD

    treeHeaderColor = TTkColor.fg("#ffffff")+TTkColor.bg("#444444")+TTkColor.BOLD
    treeSelectedColor = TTkColor.fg("#ffff88")+TTkColor.bg("#000066")+TTkColor.BOLD