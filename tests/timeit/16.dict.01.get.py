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

D1 = {
    'a' : lambda x, _ : 2*x,
    'b' : lambda x, _ : 2*x,
    'c' : lambda x, _ : 2*x,
    'd' : lambda x, _ : 2*x,
    'e' : lambda x, _ : 2*x,
    'f' : lambda x, _ : 2*x,
    'g' : lambda x, _ : 2*x,
    'h' : lambda x, _ : 2*x,
    'i' : lambda x, _ : 2*x,
    'j' : lambda x, _ : 2*x,
    'k' : lambda x, _ : 2*x,
    'l' : lambda x, y : 2*x+y,
    'm' : lambda x, _ : 2*x,
    'n' : lambda x, _ : 2*x,
    'o' : lambda x, _ : 2*x,
    'p' : lambda x, y : 2*x+y,
    'q' : lambda x, _ : 2*x,
    'r' : lambda x, _ : 2*x,
    's' : lambda x, y : 2*x+y,
    't' : lambda x, _ : 2*x,
    'u' : lambda x, y : 2*x+y,
    'v' : lambda x, _ : 2*x,
    'w' : lambda x, _ : 2*x,
    'x' : lambda x, _ : 2*x,
    'y' : lambda x, _ : 2*x,
    'z' : lambda x, _ : 2*x,
}

D2_1 = {
    'a' : lambda x: 2*x,
    'b' : lambda x: 2*x,
    'c' : lambda x: 2*x,
    'd' : lambda x: 2*x,
    'e' : lambda x: 2*x,
    'f' : lambda x: 2*x,
    'g' : lambda x: 2*x,
    'h' : lambda x: 2*x,
    'i' : lambda x: 2*x,
    'j' : lambda x: 2*x,
    'k' : lambda x: 2*x,
    'm' : lambda x: 2*x,
    'n' : lambda x: 2*x,
    'o' : lambda x: 2*x,
    'q' : lambda x: 2*x,
    'r' : lambda x: 2*x,
    't' : lambda x: 2*x,
    'v' : lambda x: 2*x,
    'w' : lambda x: 2*x,
    'x' : lambda x: 2*x,
    'y' : lambda x: 2*x,
    'z' : lambda x: 2*x,
}

D2_2 = {
    'l' : lambda x, y : 2*x+y,
    'p' : lambda x, y : 2*x+y,
    's' : lambda x, y : 2*x+y,
    'u' : lambda x, y : 2*x+y,
}

test_input_1 = {
    'a' : (2,None),
    'b' : (2,None),
    'c' : (2,None),
    'd' : (2,None),
    'e' : (2,None),
    'l' : (2,2),
    'p' : (2,2),
    's' : (2,2),
    'n' : (2,None),
    'o' : (2,None),
    'z' : (2,None),
    'y' : (2,None),
    'u' : (2,2),
}

def process1(ttt):
    ret = 0
    for i in ttt:
        x,y = ttt[i]
        _v = D1.get(i,lambda x,y:None)
        ret += _v(x,y)
    return ret

def process2(ttt):
    ret = 0
    for i in ttt:
        x,y = ttt[i]
        if y:
            _v = D2_2.get(i,lambda x,y:None)
            ret += _v(x,y)
        else:
            _v = D2_1.get(i,lambda x:None)
            ret += _v(x)
    return ret

def process3(ttt):
    return 3

def test1(): return process1(test_input_1)
def test2(): return process1(test_input_1)
def test3(): return process1(test_input_1)
def test4(): return process2(test_input_1)
def test5(): return process2(test_input_1)
def test6(): return process2(test_input_1)
def test7(): return process3(test_input_1)
def test8(): return process3(test_input_1)
def test9(): return process3(test_input_1)

loop = 100000

a={}

iii = 1
while (testName := f'test{iii}') and (testName in globals()):
    result = timeit.timeit(f'{testName}(*a)', globals=globals(), number=loop)
    # print(f"test{iii}) fps {loop / result :.3f} - s {result / loop:.10f} - {result / loop} {globals()[testName](*a)}")
    print(f"test{iii:02}) | {result / loop:.10f} sec. | {loop / result : 15.3f} Fps ╞╡-> {globals()[testName](*a)}")
    iii+=1

