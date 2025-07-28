# MIT License
#
# Copyright (c) 2025 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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
import pytest
from typing import Union, Optional

sys.path.append(os.path.join(sys.path[0],'../../libs/pyTermTk'))

import TermTk as ttk

def test_slots_stringType():
    signal1 = ttk.pyTTkSignal(str)
    signal2 = ttk.pyTTkSignal(ttk.TTkString)
    signal3 = ttk.pyTTkSignal(ttk.TTkStringType)

    @ttk.pyTTkSlot(str)
    def _test_slot1(txt:str):
        print("slot 1", txt)

    @ttk.pyTTkSlot(ttk.TTkString)
    def _test_slot2(txt:ttk.TTkString):
        print("slot 2", txt)

    @ttk.pyTTkSlot(ttk.TTkStringType)
    def _test_slot3(txt:ttk.TTkStringType):
        print("slot 3", txt)

    signal1.connect(_test_slot1)
    signal2.connect(_test_slot2)
    signal3.connect(_test_slot3)

    signal1.connect(_test_slot3)
    signal2.connect(_test_slot3)

    with pytest.raises(TypeError):
        signal1.connect(_test_slot2)
    with pytest.raises(TypeError):
        signal2.connect(_test_slot1)
    with pytest.raises(TypeError):
        signal3.connect(_test_slot1)
    with pytest.raises(TypeError):
        signal3.connect(_test_slot2)

    print('OKKK')

    signal1.emit('Eugenio1')
    signal2.emit('Eugenio2')
    signal3.emit('Eugenio3')

def test_slots_unionType():
    t1 = ttk.TTkWidget
    t2 = ttk.TTkContainer
    t3 = ttk.TTkFrame
    # TTkContainer extends TTkWidget
    # TTkWindow extends TTkFrame
    # TTkFileButtonPicker extends TTkButton
    t4 = Union[ttk.TTkFrame, ttk.TTkButton]
    t5 = Union[ttk.TTkWindow, ttk.TTkFileButtonPicker]

    signal1 = ttk.pyTTkSignal(t1)
    signal2 = ttk.pyTTkSignal(t2)
    signal3 = ttk.pyTTkSignal(t3)
    signal4 = ttk.pyTTkSignal(t4)
    signal5 = ttk.pyTTkSignal(t5)

    @ttk.pyTTkSlot(t1)
    def _test_slot1(_): pass
    @ttk.pyTTkSlot(t2)
    def _test_slot2(_): pass
    @ttk.pyTTkSlot(t3)
    def _test_slot3(_): pass
    @ttk.pyTTkSlot(t4)
    def _test_slot4(_): pass
    @ttk.pyTTkSlot(t5)
    def _test_slot5(_): pass

    signal1.connect(_test_slot1)
    signal1.connect(_test_slot2)
    signal1.connect(_test_slot3)
    signal1.connect(_test_slot4)
    signal1.connect(_test_slot5)

    signal2.connect(_test_slot2)
    signal2.connect(_test_slot3)
    signal2.connect(_test_slot4)
    signal2.connect(_test_slot5)

    signal3.connect(_test_slot3)
    signal3.connect(_test_slot4)
    signal3.connect(_test_slot5)

    signal4.connect(_test_slot4)
    signal4.connect(_test_slot5)

    signal5.connect(_test_slot5)

    with pytest.raises(TypeError):
        signal5.connect(_test_slot4)
    with pytest.raises(TypeError):
        signal5.connect(_test_slot1)

    with pytest.raises(TypeError):
        @ttk.pyTTkSlot(float)
        def _slot(_): pass
        ttk.pyTTkSignal(int).connect(_slot)
    with pytest.raises(TypeError):
        @ttk.pyTTkSlot(int)
        def _slot(_): pass
        ttk.pyTTkSignal(Union[int,float]).connect(_slot)
    with pytest.raises(TypeError):
        @ttk.pyTTkSlot(Union[int,str])
        def _slot(_): pass
        ttk.pyTTkSignal(Union[int,float]).connect(_slot)