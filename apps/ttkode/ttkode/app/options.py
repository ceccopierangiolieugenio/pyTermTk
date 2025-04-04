#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2022 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

__all__ = ['optionsLoadTheme', 'optionsFormLayout']

import copy

from . import TTKodeCfg, TloggGlbl

from TermTk import *

def optionsLoadTheme(theme):
    if theme == 'ASCII':
        TTkTheme.loadTheme(TTkTheme.ASCII)
    elif theme == 'UTF8':
        TTkTheme.loadTheme(TTkTheme.UTF8)
    elif theme == 'NERD':
        TTkTheme.loadTheme(TTkTheme.NERD)

def optionsFormLayout(win):
    options = copy.deepcopy(TTKodeCfg.options)

    retLayout    = TTkGridLayout()
    bottomLayout = TTkGridLayout()

    themesFrame = TTkFrame(title="Theme", border=True, layout=TTkVBoxLayout(), maxHeight=5, minHeight=5)
    # Themes
    themesFrame.layout().addWidget(r1 := TTkRadioButton(text="ASCII", name="theme", checked=options['theme'] == 'ASCII'))
    themesFrame.layout().addWidget(r2 := TTkRadioButton(text="UTF-8", name="theme", checked=options['theme'] == 'UTF8'))
    themesFrame.layout().addWidget(r3 := TTkRadioButton(text="Nerd",  name="theme", checked=options['theme'] == 'NERD'))

    retLayout.addWidget(themesFrame,0,0)
    retLayout.addWidget(TTkSpacer() ,1,0,1,2)

    retLayout.addItem(bottomLayout ,2,0,1,2)
    bottomLayout.addWidget(applyBtn  := TTkButton(text="Apply",  border=True, maxHeight=3),0,1)
    bottomLayout.addWidget(cancelBtn := TTkButton(text="Cancel", border=True, maxHeight=3),0,2)
    bottomLayout.addWidget(okBtn     := TTkButton(text="OK",     border=True, maxHeight=3),0,3)

    def _saveOptions():
        if r1.checkState() == TTkK.Checked: options['theme'] = 'ASCII'
        if r2.checkState() == TTkK.Checked: options['theme'] = 'UTF8'
        if r3.checkState() == TTkK.Checked: options['theme'] = 'NERD'
        TTKodeCfg.options = options
        TTKodeCfg.save(searches=False, filters=False, colors=False, options=True)
        optionsLoadTheme(options['theme'])
        TloggGlbl.refreshViews()
        TTkHelper.updateAll()

    applyBtn.clicked.connect(_saveOptions)
    okBtn.clicked.connect(_saveOptions)
    okBtn.clicked.connect(win.close)
    cancelBtn.clicked.connect(win.close)

    return retLayout
