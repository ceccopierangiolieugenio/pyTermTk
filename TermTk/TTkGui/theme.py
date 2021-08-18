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
    ''' from: https://en.wikipedia.org/wiki/Box-drawing_character

    ::

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

    hline = ('╞','═','╡')
    vline = ('╥','║','╨')

    box = ( '═','║',
            '╔','╗',
            '╚','╝')


    grid = (
      ( # Grid 0
        '┌','─','┬','┐',
        '│',' ','│','│',
        '├','─','┼','┤',
        '└','─','┴','┘'),
      ( # Grid 1
        '╔','═','╦','╗',
        '║',' ','║','║',
        '╠','═','╬','╣',
        '╚','═','╩','╝'),
      ( # Grid 2
        '╔','═','╤','╗',
        '║',' ','│','║',
        '╟','─','┼','╢',
        '╚','═','╧','╝'),
      ( # Grid 3
        '┌','─','╥','┐',
        '│',' ','║','│',
        '╞','═','╬','╡',
        '└','─','╨','┘'),
      (), # TODO: Grid 4
      (), # TODO: Grid 5
      ( # Grid 6
        '╓','─','┬','┐',
        '║',' ','│','│',
        '╟','─','┼','┤',
        '╚','═','╧','╛'),
      (), # TODO: Grid 7
      (), # TODO: Grid 8
      ( # Grid 9 ╒═╤╕
        '╒','═','╤','╕',
        '│',' ','│','│',
        '├','─','┼','┤',
        '└','─','┴','┘'),
      (), # TODO: Grid 10
        )
    ''' Grid Types

    ::

        grid0  grid1  grid2  grid3
        ┌─┬┐   ╔═╦╗   ╔═╤╗   ┌─╥┐
        │ ││   ║ ║║   ║ │║   │ ║│
        ├─┼┤   ╠═╬╣   ╟─┼╢   ╞═╬╡
        └─┴┘   ╚═╩╝   ╚═╧╝   └─╨┘
        grid4  grid5  grid6  grid7  grid8  grid9
        ╓─╥╖   ╒═╤╕   ╓─┬┐   ┌─┬╖   ┌─┬┐   ╒═╤╕
        ║ ║║   │ ││   ║ ││   │ │║   │ ││   │ ││
        ╟─╫╢   ╞═╪╡   ╟─┼┤   ├─┼╢   ├─┼┤   ├─┼┤
        ╙─╨╜   ╘═╧╛   ╚═╧╛   ╘═╧╝   ╘═╧╛   └─┴┘

        ids (hex):
        0  1  2  3
        ┌  ─  ┬  ┐
        4  5  6  7
        │     │  │
        8  9  A  B
        ├  ─  ┼  ┤
        C  D  E  F
        └  ─  ┴  ┘
    '''



    buttonBox = (
      ('┌','─','┐',
       '│',' ','│',
       '└','─','┘'),
      ('┌','─','┐',
       '│',' ','│',
       '╘','═','╛'))
    '''
    ::

        box0   box1
        ┌─┐    ┌─┐
        │ │    │ │
        └─┘    ╘═╛
    '''

    hscroll = ('◀','┄','▓','▶')
    vscroll = ('▲','┊','▓','▼')

            #   0   1   2   3   4   5
    menuBar = ('├','─','┤','┄','┄','▶')


    tab = (
      #0   1   2   3   4   5   6   7   8
      '┌','─','┬','┐','╔','═','╗','╭','╮',
      #9   10
      '│','║',
      #11  12  13  14  15  16  17  18  19  20
      '╞','═','╧','╩','╡','╘','╛','└','─','┘',
      #21  22  23  24  25  26  27  28  29  30
      '╚','╝','╰','╯','⣿','⣿','╒','╕','┴','X',
      #31  32  33  34  35  36  37  38  39  40
      '◀','▶'
    )
    ''' Tab Examples

    ::

          ┌──────╔══════╗──────┬──────┐           ┌─┌──────╔══════╗──────┬──────┐─┐
          │Label1║Label2║Label3│Label4│           │◀│Label1║Label2║Label3│Label4│▶│
        ╞═╧══════╩══════╩══════╧══════╧════╡      ╞═╧══════╩══════╩══════╧══════╧═╡
          ┌──────╔══════╗──────┬──────┐           ╭─┌──────╔══════╗──────┬──────┐─╮
          │Label1║Label2║Label3│Label4│           │◀│Label1║Label2║Label3│Label4│▶│
        ╞════════╩══════╩══════════════════╡      ╞════════╩══════╩═══════════════╡
        # Menu Prototype:
        ╭──┌──────╔══════╗──────┬──────┐          ╭──┬─┌──────╔══════╗──────┬──────┐─╮
        │XX│Label1║Label2║Label3│Label4│          │XX│◀│Label1║Label2║Label3│Label4│▶│
        ╞═════════╩══════╩═══════════════╡        ╞══╧════════╩══════╩═══════════════╡
              ┌──────╔══════╗──────┬──────┐             ╭─┌──────╔══════╗──────┬──────┐─╮
         XX YY│Label1║Label2║Label3│Label4│JJ KK   XX YY│◀│Label1║Label2║Label3│Label4│▶│JJ KK
        ╞════════════╩══════╩═══════════════════╡ ╞═════╧════════╩══════╩═══════════════╧═════╡
          ┌──────┲━━━━━━┱──────┬──────┐
          │Label1┃Label2┃Label3│Label4│
        ┝━┷━━━━━━┻━━━━━━┻━━━━━━┷━━━━━━┷━━━━┥
    '''

    # ''' bpytop style graph:
    # ::
    #         ⢠⢠              ⡇      ⣆⡇  ⢠  ⣰  ⢠
    #     ⢸⣀⣀⣠⣸⣸⡄     ⡄⣼  ⣀⡀ ⢠⣷⡀  ⣀⣰⣀⣿⣇⡀⢀⣸⡀⣆⣿⣆⣄⣼⣀⣀⣸
    #     ⣾⣿⣿⣿⣿⣿⣧⣧⣧⣤⣦⣦⣿⣿⣤⣿⣧⣧⣿⣿⣿⣷⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧
    #     ⢿⣿⣿⣿⣿⣿⡟⠟⠟⠋⠟⠏⡿⣿⠋⣿⡟⡟⢿⣿⡿⠿⡿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⡏
    #     ⢸⠉⠉⠉⢸⢹⠁     ⠃⠹ ⠁  ⠈⡿⠁  ⠈⠸⠉⣿⡏ ⠈⢹⠁⠏⣿⠏⠃⢻⠉ ⠸⠈⠁
    #         ⠈⠈             ⠇      ⠋⠇  ⠈  ⠘  ⠈
    # '''
    # graph_up = (
    #     (' ','⢀','⢠','⢰','⢸'),
    #     ('⡀','⣀','⣠','⣰','⣸'),
    #     ('⡄','⣄','⣤','⣴','⣼'),
    #     ('⡆','⣆','⣦','⣶','⣾'),
    #     ('⡇','⣇','⣧','⣷','⣿'))
    # graph_down=(
    #     (' ','⠈','⠘','⠸','⢸'),
    #     ('⠁','⠉','⠙','⠹','⢹'),
    #     ('⠃','⠋','⠛','⠻','⢻'),
    #     ('⠇','⠏','⠟','⠿','⢿'),
    #     ('⡇','⡏','⡟','⡿','⣿'))

    # Generated by:
    # tests/utf-8/test.braille.py
    braille=(
      '⠀','⠈','⠐','⠘','⠠','⠨','⠰','⠸','⢀','⢈','⢐','⢘','⢠','⢨','⢰','⢸',
      '⠁','⠉','⠑','⠙','⠡','⠩','⠱','⠹','⢁','⢉','⢑','⢙','⢡','⢩','⢱','⢹',
      '⠂','⠊','⠒','⠚','⠢','⠪','⠲','⠺','⢂','⢊','⢒','⢚','⢢','⢪','⢲','⢺',
      '⠃','⠋','⠓','⠛','⠣','⠫','⠳','⠻','⢃','⢋','⢓','⢛','⢣','⢫','⢳','⢻',
      '⠄','⠌','⠔','⠜','⠤','⠬','⠴','⠼','⢄','⢌','⢔','⢜','⢤','⢬','⢴','⢼',
      '⠅','⠍','⠕','⠝','⠥','⠭','⠵','⠽','⢅','⢍','⢕','⢝','⢥','⢭','⢵','⢽',
      '⠆','⠎','⠖','⠞','⠦','⠮','⠶','⠾','⢆','⢎','⢖','⢞','⢦','⢮','⢶','⢾',
      '⠇','⠏','⠗','⠟','⠧','⠯','⠷','⠿','⢇','⢏','⢗','⢟','⢧','⢯','⢷','⢿',
      '⡀','⡈','⡐','⡘','⡠','⡨','⡰','⡸','⣀','⣈','⣐','⣘','⣠','⣨','⣰','⣸',
      '⡁','⡉','⡑','⡙','⡡','⡩','⡱','⡹','⣁','⣉','⣑','⣙','⣡','⣩','⣱','⣹',
      '⡂','⡊','⡒','⡚','⡢','⡪','⡲','⡺','⣂','⣊','⣒','⣚','⣢','⣪','⣲','⣺',
      '⡃','⡋','⡓','⡛','⡣','⡫','⡳','⡻','⣃','⣋','⣓','⣛','⣣','⣫','⣳','⣻',
      '⡄','⡌','⡔','⡜','⡤','⡬','⡴','⡼','⣄','⣌','⣔','⣜','⣤','⣬','⣴','⣼',
      '⡅','⡍','⡕','⡝','⡥','⡭','⡵','⡽','⣅','⣍','⣕','⣝','⣥','⣭','⣵','⣽',
      '⡆','⡎','⡖','⡞','⡦','⡮','⡶','⡾','⣆','⣎','⣖','⣞','⣦','⣮','⣶','⣾',
      '⡇','⡏','⡗','⡟','⡧','⡯','⡷','⡿','⣇','⣏','⣗','⣟','⣧','⣯','⣷','⣿')

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
