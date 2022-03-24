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
from TermTk.TTkCore.string import TTkString
import TermTk.TTkGui.fileicon_nerd  as fi_nerd
import TermTk.TTkGui.fileicon_utf8  as fi_utf8
import TermTk.TTkGui.fileicon_ascii as fi_ascii
import TermTk.TTkGui.draw_utf8      as draw_utf8
import TermTk.TTkGui.draw_ascii     as draw_ascii


class TTkTheme():
    '''Default Theme Class
    This class can be reimplemented/extended to include new themes and default colors
    '''
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

    fileNameColor   = TTkColor.RST # Simil NerdTree purple
    '''Default to **TTkColor.RST # Simil NerdTree purple**'''
    executableColor = TTkColor.fg("#AAFFAA") # Greenish
    '''Default to **TTkColor.fg("#AAFFAA") # Greenish**'''
    linkNameColor   = TTkColor.fg("#00FFFF") # Cyanish
    '''Default to **TTkColor.fg("#00FFFF") # Cyanish**'''
    folderNameColor = TTkColor.fg("#AAFFFF") # Yellowish
    '''Default to **TTkColor.fg("#AAFFFF") # Yellowish**'''
    failNameColor   = TTkColor.fg("#FF0000") # Yellowish
    '''Default to **TTkColor.fg("#FF0000") # Yellowish**'''
    fileIconColor   = TTkColor.fg("#FFAAFF") # Simil NerdTree purple
    '''Default to **TTkColor.fg("#FFAAFF") # Simil NerdTree purple**'''
    folderIconColor = TTkColor.fg("#FFFFAA") # Yellowish
    '''Default to **TTkColor.fg("#FFFFAA") # Yellowish**'''

    fileIcon        = fi_utf8.FileIcon

    @staticmethod
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

        TTkTheme.fileIcon    = theme['file'].FileIcon
        TTkHelper.updateAll()



    frameBorderColor = TTkColor.RST
    '''Default to :class:`~TermTk.TTkCore.color.TTkColor.RST`'''
    frameTitleColor  = TTkColor.fg("#dddddd")+TTkColor.bg("#222222")
    '''Default to **TTkColor.fg("#dddddd")+TTkColor.bg("#222222")**'''

    windowBorderColor = TTkColor.RST
    '''Default to :class:`~TermTk.TTkCore.color.TTkColor.RST`'''
    windowBorderColorFocus = TTkColor.fg("#ffff55")
    '''Default to **TTkColor.fg("#ffff55")**'''

    buttonBoxGrid = 1
    '''Default to **1**'''
    buttonBoxGridClicked = 0
    '''Default to **0**'''
    buttonBoxGridDisabled = 0
    '''Default to **0**'''
    buttonTextColor   = TTkColor.fg("#dddd88")+TTkColor.bg("#000044")
    '''Default to **TTkColor.fg("#dddd88")+TTkColor.bg("#000044")**'''
    buttonBorderColor = TTkColor.RST
    '''Default to :class:`~TermTk.TTkCore.color.TTkColor.RST`'''
    buttonTextColorClicked   = TTkColor.fg("#ffffdd")+TTkColor.BOLD
    '''Default to **TTkColor.fg("#ffffdd")+**:class:`~TermTk.TTkCore.color.TTkColor.BOLD`'''
    buttonBorderColorClicked = TTkColor.fg("#dddddd")+TTkColor.BOLD
    '''Default to **TTkColor.fg("#dddddd")+**:class:`~TermTk.TTkCore.color.TTkColor.BOLD`'''
    buttonTextColorFocus     = buttonTextColor + TTkColor.BOLD
    '''Default to :class:`buttonTextColor` **+** :class:`~TermTk.TTkCore.color.TTkColor.BOLD`'''
    buttonBorderColorFocus   = TTkColor.fg("#ffff00") + TTkColor.BOLD
    '''Default to **TTkColor.fg("#ffff00") + **:class:`~TermTk.TTkCore.color.TTkColor.BOLD`'''
    buttonTextColorDisabled  = TTkColor.fg("#888888")
    '''Default to **TTkColor.fg("#888888")**'''
    buttonBorderColorDisabled= TTkColor.fg("#888888")
    '''Default to **TTkColor.fg("#888888")**'''


    menuButtonShortcutColor = TTkColor.fg("#dddddd") + TTkColor.UNDERLINE
    '''Default to **TTkColor.fg("#dddddd") + TTkColor.UNDERLINE**'''
    menuButtonColor = TTkColor.BOLD
    '''Default to :class:`~TermTk.TTkCore.color.TTkColor.BOLD`'''
    menuButtonBorderColor = frameBorderColor
    '''Default to :class:`frameBorderColor`'''
    menuButtonColorClicked = TTkColor.fg("#ffff88")
    '''Default to **TTkColor.fg("#ffff88")**'''
    menuButtonBorderColorClicked = frameBorderColor
    '''Default to :class:`frameBorderColor`'''

    listColor            = TTkColor.RST
    '''Default to :class:`~TermTk.TTkCore.color.TTkColor.RST`'''
    listColorSelected    = TTkColor.fg("#ffffdd")+TTkColor.bg("#000044") + TTkColor.BOLD
    '''Default to **TTkColor.fg("#ffffdd")+TTkColor.bg("#000044") + **:class:`~TermTk.TTkCore.color.TTkColor.BOLD`'''
    listColorHighlighted = TTkColor.bg("#000088") + TTkColor.BOLD
    '''Default to **TTkColor.bg("#000088") + **:class:`~TermTk.TTkCore.color.TTkColor.BOLD`'''

    lineEditTextColor       = TTkColor.fg("#dddddd")+TTkColor.bg("#222222")
    '''Default to **TTkColor.fg("#dddddd")+TTkColor.bg("#222222")**'''
    lineEditTextColorFocus  = TTkColor.fg("#dddddd")+TTkColor.bg("#000044")
    '''Default to **TTkColor.fg("#dddddd")+TTkColor.bg("#000044")**'''
    lineEditTextColorSelected  = TTkColor.fg("#ffffff")+TTkColor.bg("#008844")
    '''Default to **TTkColor.fg("#ffffff")+TTkColor.bg("#008844")**'''

    comboboxContentColor      = TTkColor.fg("#dddd88")+TTkColor.bg("#111111")
    '''Default to **TTkColor.fg("#dddd88")+TTkColor.bg("#111111")**'''
    comboboxBorderColor       = buttonBorderColor
    '''Default to :class:`buttonBorderColor`'''
    comboboxContentColorFocus      = TTkColor.fg("#ffff88")+TTkColor.bg("#111111")
    '''Default to **TTkColor.fg("#ffff88")+TTkColor.bg("#111111")**'''
    comboboxBorderColorFocus       = buttonBorderColorFocus
    '''Default to :class:`buttonBorderColorFocus`'''
    comboboxContentColorDisabled  = TTkColor.fg("#888888")
    '''Default to **TTkColor.fg("#888888")**'''
    comboboxBorderColorDisabled= TTkColor.fg("#888888")
    '''Default to **TTkColor.fg("#888888")**'''

    checkboxContentColor      = buttonTextColor
    '''Default to :class:`buttonTextColor`'''
    checkboxBorderColor       = buttonBorderColor
    '''Default to :class:`buttonBorderColor`'''
    checkboxTextColor         = TTkColor.RST
    '''Default to :class:`~TermTk.TTkCore.color.TTkColor.RST`'''
    checkboxContentColorFocus = buttonTextColorFocus
    '''Default to :class:`buttonTextColorFocus`'''
    checkboxBorderColorFocus  = buttonBorderColorFocus
    '''Default to :class:`buttonBorderColorFocus`'''
    checkboxTextColorFocus    = TTkColor.fg("#ffff88")+TTkColor.bg("#111111")
    '''Default to **TTkColor.fg("#ffff88")+TTkColor.bg("#111111")**'''

    radioButtonContentColor      = checkboxContentColor
    '''Default to :class:`checkboxContentColor`'''
    radioButtonBorderColor       = checkboxBorderColor
    '''Default to :class:`checkboxBorderColor`'''
    radioButtonTextColor       = checkboxTextColor
    '''Default to :class:`checkboxTextColor`'''
    radioButtonContentColorFocus = checkboxContentColorFocus
    '''Default to :class:`checkboxContentColorFocus`'''
    radioButtonBorderColorFocus  = checkboxBorderColorFocus
    '''Default to :class:`checkboxBorderColorFocus`'''
    radioButtonTextColorFocus  = checkboxTextColorFocus
    '''Default to :class:`checkboxTextColorFocus`'''

    tabColor       = TTkColor.fg("#aaaaaa")
    '''Default to **TTkColor.fg("#aaaaaa")**'''
    tabOffsetColor = TTkColor.RST
    '''Default to **TTkColor.RST**'''
    tabBorderColor = frameBorderColor
    '''Default to :class:`frameBorderColor`'''
    tabSelectColor = TTkColor.fg("#ffff88")+TTkColor.bg("#000066")+TTkColor.BOLD
    '''Default to **TTkColor.fg("#ffff88")+TTkColor.bg("#000066")+**:class:`~TermTk.TTkCore.color.TTkColor.BOLD`'''
    tabColorFocus       = TTkColor.fg("#aaaaaa")
    '''Default to **TTkColor.fg("#aaaaaa")**'''
    tabOffsetColorFocus = tabOffsetColor
    '''Default to :class:`tabOffsetColor`'''
    tabBorderColorFocus = TTkColor.fg("#ffff88")
    '''Default to **TTkColor.fg("#ffff88")**'''
    tabSelectColorFocus = TTkColor.fg("#ffff88")+TTkColor.bg("#000066")+TTkColor.BOLD
    '''Default to **TTkColor.fg("#ffff88")+TTkColor.bg("#000066")+**:class:`~TermTk.TTkCore.color.TTkColor.BOLD`'''

    treeHeaderColor = TTkColor.fg("#ffffff")+TTkColor.bg("#444444")+TTkColor.BOLD
    '''Default to **TTkColor.fg("#ffffff")+TTkColor.bg("#444444")+**:class:`~TermTk.TTkCore.color.TTkColor.BOLD`'''
    treeSelectedColor = TTkColor.fg("#ffff88")+TTkColor.bg("#000066")+TTkColor.BOLD
    '''Default to **TTkColor.fg("#ffff88")+TTkColor.bg("#000066")+**:class:`~TermTk.TTkCore.color.TTkColor.BOLD`'''
    treeLineColor     = TTkColor.fg("#444444")
    '''Default to **TTkColor.fg("#444444")**'''