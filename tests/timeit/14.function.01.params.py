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
import random


sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk

class Pippo():
    __slots__ = ('_pa')
    def __init__(self, pa=1234):
        self._pa=pa
    def getPa(self):
        return self._pa

    def fa(self):
        return self._pa*self._pa

    def faa(self):
        return self.getPa()*self.getPa()

    def fb(self, a):
        return a*a

    def fc(self, a, b):
        pass

pippo = Pippo(4321)

def fa():
    pass

def fb(a):
    pass

def fc(a, b):
    pass

def test1():
    return pippo.fa()
def test2():
    return pippo.faa()
def test3():
    return pippo.fb(pippo.getPa())
def test4():
    return pippo.fb(pippo._pa)
def test5(): return 5
def test6(): return 6
def test7(): return 7
def test8(): return 8
def test9(): return 9

loop = 100000

a={}

iii = 1
while (testName := f'test{iii}') and (testName in globals()):
    result = timeit.timeit(f'{testName}(*a)', globals=globals(), number=loop)
    # print(f"test{iii}) fps {loop / result :.3f} - s {result / loop:.10f} - {result / loop} {globals()[testName](*a)}")
    print(f"test{iii:02}) | {result / loop:.10f} sec. | {loop / result : 15.3f} Fps ╞╡-> {globals()[testName](*a)}")
    iii+=1

