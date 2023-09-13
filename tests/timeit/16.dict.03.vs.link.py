#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2023 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

sys.path.append(os.path.join(sys.path[0],'../..'))
from TermTk import TTkTermColor

testInput = "abcdefghil£££ABCDEFG<£££>!#$()0123459zZ£££"

testDict1 = {
    '!' : lambda x: x*2,
    '#' : lambda x: x*2,
    '$' : lambda x: x*2,

    '0' : lambda x: x*2,
    '1' : lambda x: x*2,
    '2' : lambda x: x*2,
    '3' : lambda x: x*2,
    '4' : lambda x: x*2,
    '9' : lambda x: x*2,

    'A' : lambda x: x*2,
    'B' : lambda x: x*2,
    'C' : lambda x: x*2,
    'D' : lambda x: x*2,
    'E' : lambda x: x*2,
    'F' : lambda x: x*2,
    'G' : lambda x: x*2,
    'H' : lambda x: x*2,
    'I' : lambda x: x*2,
    'Z' : lambda x: x*2,

    'a' : lambda x: x*2,
    'b' : lambda x: x*2,
    'c' : lambda x: x*2,
    'd' : lambda x: x*2,
    'e' : lambda x: x*2,
    'f' : lambda x: x*2,
    'g' : lambda x: x*2,
    'h' : lambda x: x*2,
    'i' : lambda x: x*2,
    'z' : lambda x: x*2,
}

testArray1 = [       # Oct   Dec   Kex   Char
    lambda x : x*2 , # 041   33    21    !
    None           , # 042   34    22    "
    lambda x : x*2 , # 043   35    23    #
    lambda x : x*2 , # 044   36    24    $
    None           , # 045   37    25    %
    None           , # 046   38    26    &
    None           , # 047   39    27    '
    None           , # 050   40    28    (
    None           , # 051   41    29    )
    None           , # 052   42    2A    *
    None           , # 053   43    2B    +
    None           , # 054   44    2C    ,
    None           , # 055   45    2D    -
    None           , # 056   46    2E    .
    None           , # 057   47    2F    /
    lambda x : x*2 , # 060   48    30    0
    lambda x : x*2 , # 061   49    31    1
    lambda x : x*2 , # 062   50    32    2
    lambda x : x*2 , # 063   51    33    3
    lambda x : x*2 , # 064   52    34    4
    None           , # 065   53    35    5
    None           , # 066   54    36    6
    None           , # 067   55    37    7
    None           , # 070   56    38    8
    lambda x : x*2 , # 071   57    39    9
    None           , # 072   58    3A    :
    None           , # 073   59    3B    ;
    None           , # 074   60    3C    <
    None           , # 075   61    3D    =
    None           , # 076   62    3E    >
    None           , # 077   63    3F    ?
    None           , # 100   64    40    @
    lambda x : x*2 , # 101   65    41    A
    lambda x : x*2 , # 102   66    42    B
    lambda x : x*2 , # 103   67    43    C
    lambda x : x*2 , # 104   68    44    D
    lambda x : x*2 , # 105   69    45    E
    lambda x : x*2 , # 106   70    46    F
    lambda x : x*2 , # 107   71    47    G
    lambda x : x*2 , # 110   72    48    H
    lambda x : x*2 , # 111   73    49    I
    None           , # 112   74    4A    J
    None           , # 113   75    4B    K
    None           , # 114   76    4C    L
    None           , # 115   77    4D    M
    None           , # 116   78    4E    N
    None           , # 117   79    4F    O
    None           , # 120   80    50    P
    None           , # 121   81    51    Q
    None           , # 122   82    52    R
    None           , # 123   83    53    S
    None           , # 124   84    54    T
    None           , # 125   85    55    U
    None           , # 126   86    56    V
    None           , # 127   87    57    W
    None           , # 130   88    58    X
    None           , # 131   89    59    Y
    lambda x : x*2 , # 132   90    5A    Z
    None           , # 133   91    5B    [
    None           , # 134   92    5C    \  '\\'
    None           , # 135   93    5D    ]
    None           , # 136   94    5E    ^
    None           , # 137   95    5F    _
    None           , # 140   96    60    `
    lambda x : x*2 , # 141   97    61    a
    lambda x : x*2 , # 142   98    62    b
    lambda x : x*2 , # 143   99    63    c
    lambda x : x*2 , # 144   100   64    d
    lambda x : x*2 , # 145   101   65    e
    lambda x : x*2 , # 146   102   66    f
    lambda x : x*2 , # 147   103   67    g
    lambda x : x*2 , # 150   104   68    h
    lambda x : x*2 , # 151   105   69    i
    None           , # 152   106   6A    j
    None           , # 153   107   6B    k
    None           , # 154   108   6C    l
    None           , # 155   109   6D    m
    None           , # 156   110   6E    n
    None           , # 157   111   6F    o
    None           , # 160   112   70    p
    None           , # 161   113   71    q
    None           , # 162   114   72    r
    None           , # 163   115   73    s
    None           , # 164   116   74    t
    None           , # 165   117   75    u
    None           , # 166   118   76    v
    None           , # 167   119   77    w
    None           , # 170   120   78    x
    None           , # 171   121   79    y
    lambda x : x*2 , # 172   122   7A    z
    lambda x : x*2 , # 173   123   7B    {
    lambda x : x*2 , # 174   124   7C    |
    lambda x : x*2 , # 175   125   7D    }
    lambda x : x*2 , # 176   126   7E    ~
    lambda x : x*2 , # 177   127   7F    DEL
]


def test1(ttt=testInput):
    ret = 0
    for ch in ttt:
        op = testDict1.get(ch,None)
        if op:
            ret += op(10)
    return ret

def test2(ttt=testInput):
    ret = 0
    for ch in ttt:
        if 33 <= (o:=ord(ch)) <= 127:
            op = testArray1[o-33]
            if op:
                ret += op(10)
    return ret

loop = 150000

a={}

iii = 1
while (testName := f'test{iii}') and (testName in globals()):
    result = timeit.timeit(f'{testName}(*a)', globals=globals(), number=loop)
    # print(f"test{iii}) fps {loop / result :.3f} - s {result / loop:.10f} - {result / loop} {globals()[testName](*a)}")
    print(f"test{iii:02}) | {result / loop:.10f} sec. | {loop / result : 15.3f} Fps ╞╡-> {globals()[testName](*a)}")
    iii+=1

