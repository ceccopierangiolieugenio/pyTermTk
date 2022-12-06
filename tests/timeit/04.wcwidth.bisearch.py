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

from wcwidth import *
from functools import lru_cache

sys.path.append(os.path.join(sys.path[0],'../..'))
sys.path.append(os.path.join(sys.path[0],'.'))
import TermTk as ttk

# Try to create a table with ~200 entries
print(f"Create Table...")
table = []
base = 0x1000
for _ in range(200):
    incr = random.randint(0x10,0x200)
    table.append((base,base+incr))
    base += incr + random.randint(0x10,0x100)
table =  tuple(table)
print(f"Create Done!!!")

for a,b in table:
    print(f"0x{a:06x}, 0x{b:06x}")

print(f"Create Set...")
tset = []
for a,b in table:
    for v in range(a,b+1):
        tset.append(v)
tset = set(tset)
print(f"Create Set DONE!!!")
print(f"len tset 0x{len(tset):04x}")

print(f"Create CharSetStringTest...")
cstr = ""
for _ in range(0x4000):
    cstr += chr(random.randint(0xA0,0x40000))
print(f"Create CharSetStringTest DONE!!!")

@lru_cache(maxsize=3)
def ttt(val):
    return random.randint(10,100)

print(f"{ttt(1)=}")
print(f"{ttt(2)=}")
print(f"{ttt(3)=}")
print(f"{ttt(1)=}")
print(f"{ttt(2)=}")
print(f"{ttt(3)=}")
print(f"{ttt(4)=}")
print(f"{ttt(1)=}")
print(f"{ttt(3)=}")
print(f"{ttt(2)=}")

def _bisearch(ucs, table):
    lbound = 0
    ubound = len(table) - 1

    if ucs < table[0][0] or ucs > table[ubound][1]:
        return 0
    while ubound >= lbound:
        mid = (lbound + ubound) // 2
        if ucs > table[mid][1]:
            lbound = mid + 1
        elif ucs < table[mid][0]:
            ubound = mid - 1
        else:
            return 1

    return 0

@lru_cache(maxsize=1000)
def _bicache(ucs, table):
    lbound = 0
    ubound = len(table) - 1

    if ucs < table[0][0] or ucs > table[ubound][1]:
        return 0
    while ubound >= lbound:
        mid = (lbound + ubound) // 2
        if ucs > table[mid][1]:
            lbound = mid + 1
        elif ucs < table[mid][0]:
            ubound = mid - 1
        else:
            return 1

    return 0

def test1():
    cw = 0
    for ch in cstr:
        cw += _bisearch(ord(ch), table)
    return cw

def test2():
    cw = 0
    for ch in cstr:
        cw += _bicache(ord(ch), table)
    return cw

def test3():
    return wcswidth(cstr)

def test4():
    cw = 0
    for ch in cstr:
        cw += 1 if ord(ch) in tset else 0
    return cw

def test5():
    cw = sum([1 if ord(ch) in tset else 0 for ch in cstr])
    return cw

def test6():
    return sum([ord(ch) in tset for ch in cstr])

loop = 100

result = timeit.timeit('test4()', globals=globals(), number=loop)
print(f"{result / loop:.10f} - {result / loop} {test4()}")
result = timeit.timeit('test5()', globals=globals(), number=loop)
print(f"{result / loop:.10f} - {result / loop} {test4()}")
result = timeit.timeit('test6()', globals=globals(), number=loop)
print(f"{result / loop:.10f} - {result / loop} {test4()}")

result = timeit.timeit('test3()', globals=globals(), number=loop)
print(f"{result / loop:.10f} - {result / loop} {test3()}")
result = timeit.timeit('test1()', globals=globals(), number=loop)
print(f"{result / loop:.10f} - {result / loop} {test1()}")
result = timeit.timeit('test2()', globals=globals(), number=loop)
print(f"{result / loop:.10f} - {result / loop} {test2()}")
