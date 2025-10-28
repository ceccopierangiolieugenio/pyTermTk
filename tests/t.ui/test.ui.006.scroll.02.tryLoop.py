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

import sys, os

sys.path.append(os.path.join(sys.path[0],'../../libs/pyTermTk'))
import TermTk as ttk

root = ttk.TTk()

sb1 = ttk.TTkScrollBar(parent=root, pos=(10,6), size=(1,10))
sb2 = ttk.TTkScrollBar(parent=root, pos=(12,6), size=(1,12))
sb3 = ttk.TTkScrollBar(parent=root, pos=(14,6), size=(1,14))
sb4 = ttk.TTkScrollBar(parent=root, pos=(16,6), size=(1,16))
sb5 = ttk.TTkScrollBar(parent=root, pos=( 5,0), size=(30,1), orientation=ttk.TTkK.HORIZONTAL)

slh6 = ttk.TTkSlider(parent=root, pos=( 5,1), size=(30,1), orientation=ttk.TTkK.HORIZONTAL)
slh7 = ttk.TTkSlider(parent=root, pos=( 5,2), size=(40,1), orientation=ttk.TTkK.HORIZONTAL)
slh8 = ttk.TTkSlider(parent=root, pos=( 5,3), size=(50,1), orientation=ttk.TTkK.HORIZONTAL)

slv6 = ttk.TTkSlider(parent=root, pos=(18,14), size=(1,10), orientation=ttk.TTkK.VERTICAL)
slv7 = ttk.TTkSlider(parent=root, pos=(20,10), size=(1,14), orientation=ttk.TTkK.VERTICAL)
slv8 = ttk.TTkSlider(parent=root, pos=(22, 6), size=(1,18), orientation=ttk.TTkK.VERTICAL)

sb9 = ttk.TTkSpinBox(parent=root, pos=(10,5), size=(10,1))

sb1.valueChanged.connect(sb2.setValue)
sb2.valueChanged.connect(sb3.setValue)
sb3.valueChanged.connect(sb4.setValue)
sb4.valueChanged.connect(sb5.setValue)
sb5.valueChanged.connect(sb1.setValue)
sb5.valueChanged.connect(slh6.setValue)

slh6.valueChanged.connect(slh7.setValue)
slh7.valueChanged.connect(slh8.setValue)
slh8.valueChanged.connect(slh6.setValue)
slh8.valueChanged.connect(sb2.setValue)
slh8.valueChanged.connect(sb2.setValue)

sb9.valueChanged.connect(sb1.setValue)
sb1.valueChanged.connect(sb9.setValue)

slv6.valueChanged.connect(slh7.setValue)
slv7.valueChanged.connect(slh8.setValue)
slv8.valueChanged.connect(slh6.setValue)
slh6.valueChanged.connect(slv7.setValue)
slh7.valueChanged.connect(slv8.setValue)
slh8.valueChanged.connect(slv6.setValue)


root.mainloop()