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

import timeit
import random
import unicodedata

sys.path.append(os.path.join(sys.path[0],'../..'))
sys.path.append(os.path.join(sys.path[0],'.'))
import TermTk as ttk

# first Zero size char 0x00300
# first Full size char 0x01100


print(f"Create CharSetStringTest...")
cstr  = ""
cstrw = ""
for _ in range(0x4000):
    cstr  += chr(random.randint(0x100,0x300))
    cstrw += chr(random.randint(0x100,0x20000))
print(f"Create CharSetStringTest DONE!!!")

print(f"len cstr  0x{len(cstr):04x}")
print(f"len cstrw 0x{len(cstrw):04x}")

# print([f"'{ch}':{unicodedata.east_asian_width(ch)}:{unicodedata.category(ch)}" for ch in cstr])
# print([f"'{ch}':{unicodedata.east_asian_width(ch)}:{unicodedata.category(ch)}" for ch in cstrw])

a=10

def test1(x):
    text = cstr
    return ( len(text) +
             sum(unicodedata.east_asian_width(ch) == 'W' for ch in text) -
             sum(unicodedata.category(ch) in ('Me','Mn') for ch in text) )

def test2(x):
    text = cstrw
    return ( len(text) +
             sum(unicodedata.east_asian_width(ch) == 'W' for ch in text) -
             sum(unicodedata.category(ch) in ('Me','Mn') for ch in text) )

def test3(x):
    text = cstr
    return ( any(unicodedata.east_asian_width(ch) == 'W' for ch in text) or
             any(unicodedata.category(ch) in ('Me','Mn') for ch in text) )

def test4(x):
    text = cstrw
    return ( any(unicodedata.east_asian_width(ch) == 'W' for ch in text) or
             any(unicodedata.category(ch) in ('Me','Mn') for ch in text) )

def test5(x):
    text = cstr
    return  any(ord(ch)>=0x300 for ch in text)

def test6(x):
    text = cstrw
    return  any(ord(ch)>=0x300 for ch in text)



loop = 100

result = timeit.timeit('test1(a)', globals=globals(), number=loop)
print(f"1a  {result / loop:.10f} - {result / loop} {test1(a)}")
result = timeit.timeit('test2(a)', globals=globals(), number=loop)
print(f"2a  {result / loop:.10f} - {result / loop} {test2(a)}")
result = timeit.timeit('test3(a)', globals=globals(), number=loop)
print(f"3a  {result / loop:.10f} - {result / loop} {test3(a)}")
result = timeit.timeit('test4(a)', globals=globals(), number=loop)
print(f"4a  {result / loop:.10f} - {result / loop} {test4(a)}")
result = timeit.timeit('test5(a)', globals=globals(), number=loop)
print(f"5a  {result / loop:.10f} - {result / loop} {test5(a)}")
result = timeit.timeit('test6(a)', globals=globals(), number=loop)
print(f"6a  {result / loop:.10f} - {result / loop} {test6(a)}")
