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

__all__ = ['TTkTheme']

from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.helper import TTkHelper
# from TermTk.TTkCore.string import TTkString
import TermTk.TTkTheme.fileicon_nerd  as fi_nerd
import TermTk.TTkTheme.fileicon_utf8  as fi_utf8
import TermTk.TTkTheme.fileicon_ascii as fi_ascii
import TermTk.TTkTheme.draw_utf8      as draw_utf8
import TermTk.TTkTheme.draw_ascii     as draw_ascii

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
    unicodeWideOverflowCh = draw_utf8.TTkTheme.unicodeWideOverflowCh
    progressbarBlocks = draw_utf8.TTkTheme.progressbarBlocks

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
        TTkTheme.unicodeWideOverflowCh = theme['draw'].TTkTheme.unicodeWideOverflowCh
        TTkTheme.progressbarBlocks = theme['draw'].TTkTheme.progressbarBlocks

        TTkTheme.fileIcon    = theme['file'].FileIcon
        TTkHelper.updateAll()

