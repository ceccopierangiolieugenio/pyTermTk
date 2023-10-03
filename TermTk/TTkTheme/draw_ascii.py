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

class TTkTheme():
    hline = ('=','=','=')
    vline = ('|','|','|')

    box = ( 'X','X',
            'X','X',
            'X','X')

    grid = (
      ( # Grid 0
        'X','X','X','X',
        'X',' ','X','X',
        'X','X','X','X',
        'X','X','X','X'),
      ( # Grid 1
        'X','X','X','X',
        'X',' ','X','X',
        'X','X','X','X',
        'X','X','X','X'),
      ( # Grid 2
        'X','X','X','X',
        'X',' ','X','X',
        'X','X','X','X',
        'X','X','X','X'),
      ( # Grid 3
        'X','X','X','X',
        'X',' ','X','X',
        'X','X','X','X',
        'X','X','X','X'),
      (), # TODO: Grid 4
      (), # TODO: Grid 5
      ( # Grid 6
        'X','X','X','X',
        'X',' ','X','X',
        'X','X','X','X',
        'X','X','X','X'),
      (), # TODO: Grid 7
      (), # TODO: Grid 8
      ( # Grid 9 ╒═╤╕
        'X','X','X','X',
        'X',' ','X','X',
        'X','X','X','X',
        'X','X','X','X'),
      (), # TODO: Grid 10
        )

    buttonBox = (
      ('X','X','X',
       'X',' ','X',
       'X','X','X'),
      ('X','X','X',
       'X',' ','X',
       'X','X','X'),
      ('X','X','X',
       'X',' ','X',
       'X','X','X'),
      ('X','X','X',
       'X',' ','X',
       'X','X','X'))

    combobox = {'( )','(x)'}
    checkbox = {'[ ]','[x]','[/]'}

    hscroll = ('<','-','X','>')
    vscroll = ('^','|','X','v')

    tree = (' ','+','-',' ',
            '|','|','v','^',)


            #   0   1   2   3   4   5
    menuBar = ('|','-','|','-','-','>')


    tab = (
      #0   1   2   3   4   5   6   7   8
      '/','-','-','\\','=','=','=','/','\\',
      #9   10
      '|','|',
      #11  12  13  14  15  16  17  18  19  20
      '=','=','=','=','=','=','=','\\','-','/',
      #21  22  23  24  25  26  27  28  29  30
      '=','=','\\','/','X','X','=','=','-','X',
      #31  32  33  34  35  36  37  38  39  40
      '<','>','|','|','-','-','X'
    )

    braille=(
      'X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X',
      'X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X',
      'X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X',
      'X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X',
      'X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X',
      'X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X',
      'X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X',
      'X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X',
      'X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X',
      'X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X',
      'X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X',
      'X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X',
      'X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X',
      'X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X',
      'X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X',
      'X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X')

    unicodeWideOverflowCh = ('<','>')

    #                          012345678
    progressbarBlocks = tuple('     ||||')