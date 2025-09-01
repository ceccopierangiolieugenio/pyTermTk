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

import sys, os

sys.path.append(os.path.join(sys.path[0],'../../libs/pyTermTk'))

import TermTk

def test_stringAlign1():
    test1 = TermTk.TTkString('Yes\u231b\u231b\u231b') # 'Yes⌛⌛⌛'
    print(f"Testcase: |{str(test1)}|")

    for width in range(0, 15):
        aligned = test1.align(width=width, alignment=TermTk.TTkK.CENTER_ALIGN)
        print(f"width={width:2}: |{aligned}|")

    # width= 0: |Yes⌛⌛⌛|
    assert 'Yes⌛⌛⌛'    == str(test1.align(width= 0, alignment=TermTk.TTkK.CENTER_ALIGN))
    # width= 1: |Y|
    assert 'Y'            == str(test1.align(width= 1, alignment=TermTk.TTkK.CENTER_ALIGN))
    # width= 2: |Ye|
    assert 'Ye'           == str(test1.align(width= 2, alignment=TermTk.TTkK.CENTER_ALIGN))
    # width= 3: |Yes|
    assert 'Yes'          == str(test1.align(width= 3, alignment=TermTk.TTkK.CENTER_ALIGN))
    # width= 4: |Yes≽|
    assert 'Yes≽'         == str(test1.align(width= 4, alignment=TermTk.TTkK.CENTER_ALIGN))
    # width= 5: |Yes⌛|
    assert 'Yes⌛'        == str(test1.align(width= 5, alignment=TermTk.TTkK.CENTER_ALIGN))
    # width= 6: |Yes⌛≽|
    assert 'Yes⌛≽'       == str(test1.align(width= 6, alignment=TermTk.TTkK.CENTER_ALIGN))
    # width= 7: |Yes⌛⌛|
    assert 'Yes⌛⌛'      == str(test1.align(width= 7, alignment=TermTk.TTkK.CENTER_ALIGN))
    # width= 8: |Yes⌛⌛≽|
    assert 'Yes⌛⌛≽'     == str(test1.align(width= 8, alignment=TermTk.TTkK.CENTER_ALIGN))
    # width= 9: |Yes⌛⌛⌛|
    assert 'Yes⌛⌛⌛'    == str(test1.align(width= 9, alignment=TermTk.TTkK.CENTER_ALIGN))
    # width=10: |Yes⌛⌛⌛ |
    assert 'Yes⌛⌛⌛ '   == str(test1.align(width=10, alignment=TermTk.TTkK.CENTER_ALIGN))
    # width=11: | Yes⌛⌛⌛ |
    assert ' Yes⌛⌛⌛ '  == str(test1.align(width=11, alignment=TermTk.TTkK.CENTER_ALIGN))
    # width=12: | Yes⌛⌛⌛  |
    assert ' Yes⌛⌛⌛  ' == str(test1.align(width=12, alignment=TermTk.TTkK.CENTER_ALIGN))
    # width=13: |  Yes⌛⌛⌛  |
    assert '  Yes⌛⌛⌛  '== str(test1.align(width=13, alignment=TermTk.TTkK.CENTER_ALIGN))
    # width=14: |  Yes⌛⌛⌛   |
    assert '  Yes⌛⌛⌛   '==str(test1.align(width=14, alignment=TermTk.TTkK.CENTER_ALIGN))
