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


sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk

words = ["Lorem", "ipsum", "dolor", "sit", "amet,", "consectetur", "adipiscing", "elit,", "sed", "do", "eiusmod", "tempor", "incididunt", "ut", "labore", "et", "dolore", "magna", "aliqua.", "Ut", "enim", "ad", "minim", "veniam,", "quis", "nostrud", "exercitation", "ullamco", "laboris", "nisi", "ut", "aliquip", "ex", "ea", "commodo", "consequat.", "Duis", "aute", "irure", "dolor", "in", "reprehenderit", "in", "voluptate", "velit", "esse", "cillum", "dolore", "eu", "fugiat", "nulla", "pariatur.", "Excepteur", "sint", "occaecat", "cupidatat", "non", "proident,", "sunt", "in", "culpa", "qui", "officia", "deserunt", "mollit", "anim", "id", "est", "laborum."]

def getWords(n):
    www = [random.choice(words) for _ in range(n)]
    return " ".join(www)
def getSentence(a,b,i):
    return " ".join([f"{i} "]+[getWords(random.randint(1,4)) for i in range(0,random.randint(a,b))])

doc1 = [ getSentence(3,10,i) for i in range(10000) ]

doc2 = doc1.copy()
doc2[5000:5050] = [ getSentence(3,10,i) for i in range(50) ]


nn = 1000

class I():
    def __init__(self, i):
        self.z = i

ii = [ I(random.randint(0,10000)) for _ in range(nn)]


def test():
    minz = 0
    for i in ii:
        minz=min(i.z-1,minz)
    return minz

def test1():
    return min([i.z-1 for i in ii])

def test2():
    return min([i.z for i in ii])-1

def test3(): # tbd
    return 0

def test4(): # tbd
    return 0

loop = 1000

result = timeit.timeit('test()', globals=globals(), number=loop)
print(f"{result / loop:.10f} - {result / loop} {test()}")
result = timeit.timeit('test1()', globals=globals(), number=loop)
print(f"{result / loop:.10f} - {result / loop} {test1()}")
result = timeit.timeit('test2()', globals=globals(), number=loop)
print(f"{result / loop:.10f} - {result / loop} {test2()}")
result = timeit.timeit('test3()', globals=globals(), number=loop)
print(f"{result / loop:.10f} - {result / loop} {test3()}")
result = timeit.timeit('test4()', globals=globals(), number=loop)
print(f"{result / loop:.10f} - {result / loop} {test4()}")
