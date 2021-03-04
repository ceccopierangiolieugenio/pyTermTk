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


'''
    bits          utf-8             diff with utf8 bits
    0 4  0,1,2 -> 0x00->0x07        ch012
    1 5  4,5,6 -> 0x00->0x07 << 3   ch456>>1
    2 6
    3 7
    | \---> 7  -> 0x80              ch7
    \-----> 3  -> 0x40              ch3<<3
'''
def ch2braille(ch):
    ch012 = ch & 0x07
    ch456 = ch & 0x70
    ch3   = ch & 0x08
    ch7   = ch & 0x80
    return 0x2800 | ch012 | (ch456>>1) | (ch3<<3) | ch7


codes = [ chr(ch2braille(ch)) for ch in range(0,0x100)]

print("braille=(")
for a in range(0x10):
    for b in range(0x10):
        val = a | (b<<4)
        print(f"'{codes[val]}',",end='')
    print()
print(")")

