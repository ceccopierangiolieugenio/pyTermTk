#!/usr/bin/env python3

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

from __future__ import annotations

import sys, os

from dataclasses import dataclass
from enum import Enum,Flag,auto
import timeit

from typing import List, Tuple, Iterator

sys.path.append(os.path.join(sys.path[0],'../../libs/pyTermTk'))

import TermTk as ttk

def _create_tree() -> ttk.TTkTreeWidgetItem:
    l0   = ttk.TTkTreeWidgetItem(["XX0","XX0","XX0"])
    l1   = ttk.TTkTreeWidgetItem(["String A", "String B", "String C"])
    l2   = ttk.TTkTreeWidgetItem(["String AA", "String BB", "String CC"])
    l3   = ttk.TTkTreeWidgetItem(["String AAA", "String BBB", "String CCC"])
    l4   = ttk.TTkTreeWidgetItem(["String AAAA", "String BBBB", "String CCCC"])
    l5   = ttk.TTkTreeWidgetItem(["String AAAAA", "String BBBBB", "String CCCCC"])
    l51   = ttk.TTkTreeWidgetItem(["String AAAAA", "String BBBBB", "String CCCCC"])
    l511   = ttk.TTkTreeWidgetItem(["String AAAAA", "String BBBBB", "String CCCCC"])
    l5111   = ttk.TTkTreeWidgetItem(["String AAAAA", "String BBBBB", "String CCCCC"])
    l52   = ttk.TTkTreeWidgetItem(["String AAAAA", "String BBBBB", "String CCCCC"])
    l521   = ttk.TTkTreeWidgetItem(["String AAAAA", "String BBBBB", "String CCCCC"])

    l2.addChild(l5)
    l5.addChild(l51)
    l51.addChild(l511)
    l511.addChild(l5111)
    l5.addChild(l52)
    l52.addChild(l521)

    def _addChilds(p:ttk.TTkTreeWidgetItem,num:int,prefix:str,nesting=2):
        _children = []
        for i in range(num):
            _c = ttk.TTkTreeWidgetItem([f"{prefix} A {i}", f"{prefix} B {i}", f"{prefix} C {i}"])
            _c._height = i
            _children.append(_c)
            if i%2:
                _c.setExpanded(True)
            if nesting:
                _addChilds(_c,num,f"{prefix}_X",nesting-1)
        p.addChildren(_children)

    _addChilds(l1,10,'l1',3)
    _addChilds(l2,100,'l2',0)
    _addChilds(l2,20,'l2',2)
    _addChilds(l3,30,'l3',2)
    _addChilds(l4,10,'l4',2)
    _addChilds(l5,20,'l5',2)
    _addChilds(l51,30,'l51',2)
    _addChilds(l511,30,'l511',2)
    _addChilds(l5111,40,'l5111',2)
    _addChilds(l52,50,'l52',2)
    _addChilds(l521,10,'l521',2)

    l0.addChild(l1)
    l0.addChild(l2)
    l0.addChild(l3)
    l0.addChild(l4)

    l0.setExpanded(True)
    l2.setExpanded(True)
    l5.setExpanded(True)
    l51.setExpanded(True)
    l511.setExpanded(True)
    l5111.setExpanded(True)
    l52.setExpanded(True)
    l521.setExpanded(True)
    l4.setExpanded(True)

    return l0

def _format_item(item:ttk.TTkTreeWidgetItem) -> str:
    return f"{item.data(0)} {item.data(1)} {item.data(2)}"

def _full_iterate(p:ttk.TTkTreeWidgetItem, level:int=0) -> Iterator[ttk.TTkTreeWidgetItem]:
    for _c in p._children:
        for _y in range(_c._height):
            yield _c, level, _y
        if _c._expanded:
            yield from _full_iterate(_c,level+1)

def _full_full_iterate(p:ttk.TTkTreeWidgetItem, level:int=0) -> Iterator[ttk.TTkTreeWidgetItem]:
    for _c in p._children:
        yield _c, level
        yield from _c._iterate(level+1)

def _get_size_iterate_1(p:ttk.TTkTreeWidgetItem) -> int:
    return len(p._children) + sum(_get_size_iterate_1(_c) for _c in p._children if _c.isExpanded())

def _get_size_iterate_2(p:ttk.TTkTreeWidgetItem) -> int:
    _ret = len(p._children)
    for _c in p._children:
        if _c.isExpanded():
            _ret += _get_size_iterate_2(_c)
    return _ret

def _get_size_iterate_3(p:ttk.TTkTreeWidgetItem) -> int:
    # return p.height()
    _ret = 0
    for _c in p._children:
        _ret += _c._height
        if _c.isExpanded():
            _ret += _get_size_iterate_3(_c)
    return _ret

tree = _create_tree()

print('Total: ', len(list(_full_full_iterate(tree))))

def test_ti_0_00_0(): return len([x for x in _full_iterate(tree)])
def test_ti_0_00_1(): return len([x for x in _full_iterate(tree)])
def test_ti_0_01_0(): return len(tree.listify())
def test_ti_0_02_0(): return tree.size()

loop = 100

a:dict = {}

for testName in sorted([tn for tn in globals() if tn.startswith('test_ti_')]):
    result = timeit.timeit(f'{testName}(*a)', globals=globals(), number=loop)
    # print(f"test{iii}) fps {loop / result :.3f} - s {result / loop:.10f} - {result / loop} {globals()[testName](*a)}")
    print(f"{testName} | {result / loop:.10f} sec. | {loop / result : 15.3f} Fps ╞╡-> {globals()[testName](*a)}")
