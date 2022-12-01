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

import wcwidth
from functools import lru_cache

sys.path.append(os.path.join(sys.path[0],'../..'))
sys.path.append(os.path.join(sys.path[0],'.'))
import TermTk as ttk


_unicode_version = "13.0.0"
zw = wcwidth.ZERO_WIDTH[_unicode_version]
# zwcf = wcwidth.ZERO_WIDTH_CF
we = wcwidth.WIDE_EASTASIAN[_unicode_version]
zwcf = [
    0,       # Null (Cc)
    0x034F,  # Combining grapheme joiner (Mn)
    0x200B,  # Zero width space
    0x200C,  # Zero width non-joiner
    0x200D,  # Zero width joiner
    0x200E,  # Left-to-right mark
    0x200F,  # Right-to-left mark
    0x2028,  # Line separator (Zl)
    0x2029,  # Paragraph separator (Zp)
    0x202A,  # Left-to-right embedding
    0x202B,  # Right-to-left embedding
    0x202C,  # Pop directional formatting
    0x202D,  # Left-to-right override
    0x202E,  # Right-to-left override
    0x2060,  # Word joiner
    0x2061,  # Function application
    0x2062,  # Invisible times
    0x2063,  # Invisible separator
]


def set2binmask(s):
    ret = []
    for v in s:
        id = v >> 5
        mask = v & 0x1F
        bit = 1 << mask
        if id >= len(ret):
            ret += [0]*(id-len(ret)+2)
        ret[id] |= bit
    return ret


print(f"Create Set...")
zset = []
for a,b in zw:
    for v in range(a,b+1):
        zset.append(v)
for v in zwcf:
    zset.append(v)
zset = set(zset)

wset = []
for a,b in we:
    for v in range(a,b+1):
        wset.append(v)
wset = set(wset)

print(f"Create Set DONE!!!")

print(f"Create CharSetStringTest...")
cstr = ""
for _ in range(0x4000):
    cstr += chr(random.randint(0x100,0x20000))
print(f"Create CharSetStringTest DONE!!!")

# print(f"{set2binmask(zset)}")

bzset = set2binmask(zset)
bwset = set2binmask(wset)

print(f"len zset 0x{len(zset):04x}")
print(f"len zset 0x{len(bzset):04x}")
print(f"len wset 0x{len(wset):04x}")
print(f"len wset 0x{len(bwset):04x}")
print(f"len cstr 0x{len(cstr):04x}")

print([f"'{ch}':{unicodedata.east_asian_width(ch)}:{unicodedata.category(ch)}" for ch in cstr])

# @lru_cache(maxsize=3)
# def ttt(val):
#     return random.randint(10,100)
#
# print(f"{ttt(1)=}")
# print(f"{ttt(2)=}")
# print(f"{ttt(3)=}")
# print(f"{ttt(1)=}")unicodedata.category
# print(f"{ttt(1)=}")
# print(f"{ttt(3)=}")
# print(f"{ttt(2)=}")

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
        cw += _bisearch(ord(ch), zw)
    return cw

def test2():
    cw = 0
    for ch in cstr:
        cw += _bicache(ord(ch), zw)
    return cw

def test3():
    return  wcwidth.wcswidth(cstr)

def test4():
    cw = 0
    for ch in cstr:
        cw += 1 if ord(ch) in wset else 0
    return cw

def test5():
    cw = sum([1 if ord(ch) in wset else 0 for ch in cstr])
    return cw

def test6():
    return len(cstr) + sum([ord(ch) in wset for ch in cstr]) - sum([ord(ch) in zset for ch in cstr])

def test7():
    return len(cstr) + sum([bwset[ord(ch)>>5]>>(ord(ch)&0x1F)&1 for ch in cstr]) - sum([bzset[ord(ch)>>5]>>(ord(ch)&0x1F)&1 for ch in cstr])

def test8():
    return len(cstr) + sum([bwset[ord(ch)>>5]>>(ord(ch)&0x1F)&1 for ch in cstr]) - sum([ord(ch) in zset for ch in cstr])

def test9():
    return len(cstr) + sum([0!=(bwset[ord(ch)>>5]&(1<<(ord(ch)&0x1F))) for ch in cstr]) - sum([ord(ch) in zset for ch in cstr])

def test10():
    return ( len(cstr) +
             sum(['W'==unicodedata.east_asian_width(ch) for ch in cstr]) -
             sum(['Me'==(c:=unicodedata.category(ch)) or 'Mn'==c for ch in cstr]) )
def test11():
    return ( len(cstr) +
             sum([unicodedata.east_asian_width(ch) == 'W' for ch in cstr]) -
             sum([unicodedata.category(ch) in ('Me','Mn') for ch in cstr]) )


loop = 100

result = timeit.timeit('test4()', globals=globals(), number=loop)
print(f"4  {result / loop:.10f} - {result / loop} {test4()}")
result = timeit.timeit('test5()', globals=globals(), number=loop)
print(f"5  {result / loop:.10f} - {result / loop} {test5()}")
result = timeit.timeit('test6()', globals=globals(), number=loop)
print(f"6  {result / loop:.10f} - {result / loop} {test6()}")
result = timeit.timeit('test10()', globals=globals(), number=loop)
print(f"10 {result / loop:.10f} - {result / loop} {test10()}")
result = timeit.timeit('test11()', globals=globals(), number=loop)
print(f"11 {result / loop:.10f} - {result / loop} {test11()}")
result = timeit.timeit('test7()', globals=globals(), number=loop)
print(f"7  {result / loop:.10f} - {result / loop} {test7()}")
result = timeit.timeit('test8()', globals=globals(), number=loop)
print(f"8  {result / loop:.10f} - {result / loop} {test8()}")
result = timeit.timeit('test9()', globals=globals(), number=loop)
print(f"9  {result / loop:.10f} - {result / loop} {test9()}")

result = timeit.timeit('test3()', globals=globals(), number=loop)
print(f"3w {result / loop:.10f} - {result / loop} {test3()}")
result = timeit.timeit('test1()', globals=globals(), number=loop)
print(f"1w {result / loop:.10f} - {result / loop} {test1()}")
result = timeit.timeit('test2()', globals=globals(), number=loop)
print(f"2w {result / loop:.10f} - {result / loop} {test2()}")
