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

class TTkTheme():
    '''  from: https://en.wikipedia.org/wiki/Box-drawing_character
        ┌─┬┐  ╔═╦╗  ╓─╥╖  ╒═╤╕
        │ ││  ║ ║║  ║ ║║  │ ││
        ├─┼┤  ╠═╬╣  ╟─╫╢  ╞═╪╡
        └─┴┘  ╚═╩╝  ╙─╨╜  ╘═╧╛
        ┌───────────────────┐
        │  ╔═══╗ Some Text  │▒
        │  ╚═╦═╝ in the box │▒
        ╞═╤══╩══╤═══════════╡▒
        │ ├──┬──┤           │▒
        │ └──┴──┘           │▒
        └───────────────────┘▒
         ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
    '''
    box = ( '═','║',
            '╔','╗',
            '╚','╝')
    '''
        grid0  grid1  grid2  grid3
        ┌─┬┐   ╔═╦╗   ╔═╤╗   ┌─╥┐
        │ ││   ║ ║║   ║ │║   │ ║│
        ├─┼┤   ╠═╬╣   ╟─┼╢   ╞═╬╡
        └─┴┘   ╚═╩╝   ╚═╧╝   └─╨┘
        grid4  grid5  grid6  grid7  grid8
        ╓─╥╖   ╒═╤╕   ╓─┬┐   ┌─┬╖   ┌─┬┐
        ║ ║║   │ ││   ║ ││   │ │║   │ ││
        ╟─╫╢   ╞═╪╡   ╟─┼┤   ├─┼╢   ├─┼┤
        ╙─╨╜   ╘═╧╛   ╚═╧╛   ╘═╧╝   ╘═╧╛
    '''
    grid = (
      ( '─','│', # Grid 0
        '┌','┐','└','┘',
        '├','┤','┬','┴',
        '─','│','┼',),
      ( '═','║', # Grid 1
        '╔','╗','╚','╝',
        '╠','╣','╦','╩',
        '═','║','╬',),
      ( '═','║', # Grid 2
        '╔','╗','╚','╝',
        '╟','╢','╤','╧',
        '─','│','┼',),
      ( '─','│', # Grid 3
        '┌','┐','└','┘',
        '╞','╡','╥','╨',
        '═','║','╬',))

    '''
        box0   box1
        ┌─┐    ┌─┐
        │ │    │ │
        └─┘    ╘═╛
    '''
    buttonBox = (
      ('┌','─','┐',
       '│',' ','│',
       '└','─','┘'),
      ('┌','─','┐',
       '│',' ','│',
       '╘','═','╛'))

    hscroll = ('◀','┄','▓','▶')
    vscroll = ('▲','┊','▓','▼')

    frameBorderColor = TTkColor.RST
    frameTitleColor  = TTkColor.fg("#dddddd")+TTkColor.bg("#222222")

    buttonBoxGrid = 1
    buttonBoxGridClicked = 0
    buttonTextColor   = TTkColor.fg("#dddd88")+TTkColor.bg("#000044")
    buttonBorderColor = TTkColor.fg("#dddd88")
    buttonTextColorClicked   = TTkColor.fg("#ffffdd")+TTkColor.BOLD
    buttonBorderColorClicked = TTkColor.fg("#dddddd")+TTkColor.BOLD
    buttonTextColorFocus     = buttonTextColor   + TTkColor.BOLD
    buttonBorderColorFocus   = buttonBorderColor + TTkColor.BOLD


    lineEditTextColor       = TTkColor.fg("#dddddd")+TTkColor.bg("#222222")
    lineEditTextColorFocus  = TTkColor.fg("#dddddd")+TTkColor.bg("#000044")

    comboboxContentColor      = TTkColor.fg("#dddd88")+TTkColor.bg("#111111")
    comboboxBorderColor       = buttonBorderColor

    checkboxContentColor      = buttonTextColor
    checkboxBorderColor       = buttonBorderColor
    checkboxContentColorFocus = buttonTextColorFocus
    checkboxBorderColorFocus  = buttonBorderColorFocus

    radioButtonContentColor      = buttonTextColor
    radioButtonBorderColor       = buttonBorderColor
    radioButtonContentColorFocus = buttonTextColorFocus
    radioButtonBorderColorFocus  = buttonBorderColorFocus