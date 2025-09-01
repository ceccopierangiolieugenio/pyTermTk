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

import sys, os
import pytest
from typing import Union, Optional, List, Tuple

sys.path.append(os.path.join(sys.path[0],'../../libs/pyTermTk'))

import TermTk as ttk

def _gen_childs(num:int,prefix:str,nesting=2) -> List[ttk.TTkTreeWidgetItem]:
    ret = []
    for i in range(num):
        _c = ttk.TTkTreeWidgetItem([f"{prefix} A {i}{'\nabc'*i}", f"{prefix} B {i}", f"{prefix} C {i}"])
        ret.append(_c)
        if i%2:
            _c.setExpanded(True)
        if nesting:
            _c.addChildren(_gen_childs(num,f"{prefix}_X",nesting-1))
    return ret

def _add_children(item:ttk.TTkTreeWidgetItem):
    item.addChildren(_gen_childs(4,'l2',2))

def _create_tree() -> Tuple[ttk.TTkTreeWidgetItem,ttk.TTkTreeWidgetItem,ttk.TTkTreeWidgetItem]:
    l0   = ttk.TTkTreeWidgetItem(["XX0","XX0","XX0"])
    l1   = ttk.TTkTreeWidgetItem(["String A", "String B", "String C"])
    l2   = ttk.TTkTreeWidgetItem(["String AA", "String BB", "String CC"])
    l3   = ttk.TTkTreeWidgetItem(["String AAA", "String BBB", "String CCC"])
    l4   = ttk.TTkTreeWidgetItem(["String AAAA", "String BBBB", "String CCCC"])
    l5   = ttk.TTkTreeWidgetItem(["String AAAAA", "String BBBBB", "String CCCCC"])

    l2.addChild(l5)

    l1.addChildren(_gen_childs(2,'l1',1))
    l2.addChildren(_gen_childs(4,'l2',2))
    l3.addChildren(_gen_childs(3,'l3',1))
    l4.addChildren(_gen_childs(2,'l4',1))
    l5.addChildren(_gen_childs(2,'l5',1))

    l0.addChild(l1)
    l0.addChild(l2)
    l0.addChild(l3)
    l0.addChild(l4)

    l0.setExpanded(True)
    l2.setExpanded(True)
    l5.setExpanded(True)
    l4.setExpanded(True)

    return l0, l2, l5

def _format_item(item:ttk.TTkTreeWidgetItem) -> str:
    return f"{item.data(0)} h:{item.height()}         {item.data(1)} {item.data(2)}".replace('\n','_\\n_')

def _print_tree(child:ttk.TTkTreeWidgetItem, level:int=0):
    if child.isExpanded() and child.children():
        print('  '*level, ' v ', _format_item(child))
        for i,c in enumerate(child.children()):
            _print_tree(c,level+1)
    elif child.children():
        print('  '*level, ' > ', _format_item(child))
    else:
        print('  '*level, ' - ', _format_item(child))

# def test_tree_item_iterate_skip():
#     tree,_,_ = _create_tree()

#     print('\nTree:')
#     _print_tree(tree)

#     # for i,(a,b) in enumerate(tree.iterate()):
#     #     print(f"{i:03} - ", b, '  '*b, _format_item(a))

#     # print('\nSkip 3')
#     # for i,(a,b) in enumerate(tree.iterate(skip=3),3):
#     #     print(f"{i:03} - ", b, '  '*b, _format_item(a))

#     # print('\nSkip 7')
#     # for i,(a,b) in enumerate(tree.iterate(skip=7),7):
#     #     print(f"{i:03} - ", b, '  '*b, _format_item(a))

#     full = [(a,b) for a,b in tree._iterate()]

#     assert full      == [(a,b) for a,b in tree._iterate()]
#     assert full      == [(a,b) for a,b in tree._iterate(skip= 0)]
#     assert full[ 3:] == [(a,b) for a,b in tree._iterate(skip= 3)]
#     assert full[ 5:] == [(a,b) for a,b in tree._iterate(skip= 5)]
#     assert full[ 6:] == [(a,b) for a,b in tree._iterate(skip= 6)]
#     assert full[10:] == [(a,b) for a,b in tree._iterate(skip=10)]
#     assert full[15:] == [(a,b) for a,b in tree._iterate(skip=15)]
#     assert full[20:] == [(a,b) for a,b in tree._iterate(skip=20)]
#     assert full[30:] == [(a,b) for a,b in tree._iterate(skip=30)]
#     assert full[80:] == [(a,b) for a,b in tree._iterate(skip=80)]
#     assert []        == [(a,b) for a,b in tree._iterate(skip=80)]



def test_tree_item_iterate_skip_2():
    def my_gen():
        for i in range(10):
            yield i

    # Save progress
    gen = my_gen()

    # Resume from saved_index
    for i,item in enumerate(gen):
        print(i, item)
        if i==5:
            break

    for i,item in enumerate(gen):
        print(i, item)

# def test_tree_item_listify():
#     tree,c1,c2 = _create_tree()

#     print('\nTree:')
#     _print_tree(tree)

#     for i,(a,b,c) in enumerate(tree.listify()):
#         print(f"{i:03} - ", b, c, '  '*b, _format_item(a))

#     full = [(a,b) for a,b in tree._iterate()]

#     print('expand')
#     c1.setExpanded(False)
#     for i,(a,b,c) in enumerate(tree.listify()):
#         print(f"{i:03} - ", b, c, '  '*b, _format_item(a))

#     print('expand')
#     c1.setExpanded(True)
#     for i,(a,b,c) in enumerate(tree.listify()):
#         print(f"{i:03} - ", b, c, '  '*b, _format_item(a))

#     print('expand')
#     c2.setExpanded(False)
#     for i,(a,b,c) in enumerate(tree.listify()):
#         print(f"{i:03} - ", b, c, '  '*b, _format_item(a))

#     print('expand')
#     c2.setExpanded(True)
#     for i,(a,b,c) in enumerate(tree.listify()):
#         print(f"{i:03} - ", b, c, '  '*b, _format_item(a))

#     print('expand c1 False')
#     c1.setExpanded(False)
#     for i,(a,b,c) in enumerate(tree.listify()):
#         print(f"{i:03} - ", b, c, '  '*b, _format_item(a))

#     print('expand c2 False')
#     c2.setExpanded(False)
#     for i,(a,b,c) in enumerate(tree.listify()):
#         print(f"{i:03} - ", b, c, '  '*b, _format_item(a))

#     print('expand c2 True')
#     c2.setExpanded(True)
#     for i,(a,b,c) in enumerate(tree.listify()):
#         print(f"{i:03} - ", b, c, '  '*b, _format_item(a))

#     print('expand c1 True')
#     c1.setExpanded(True)
#     for i,(a,b,c) in enumerate(tree.listify()):
#         print(f"{i:03} - ", b, c, '  '*b, _format_item(a))

def _get_node_size(item:ttk.TTkTreeWidgetItem):
    size = item.height()
    if item.isExpanded():
        for _ch in item.children():
            size += _get_node_size(_ch)
    return size

def _test_size_ch(ch:ttk.TTkTreeWidgetItem):
    print(_format_item(ch))
    assert _get_node_size(ch) == ch.size() , _format_item(ch)

# Test first the children and the parent
def _loop_1(item:ttk.TTkTreeWidgetItem):
    if item.isExpanded():
        for _ch in item.children():
            _loop_1(_ch)
    _test_size_ch(item)

# Test first the parent and the children
def _loop_2(item:ttk.TTkTreeWidgetItem):
    _test_size_ch(item)
    if item.isExpanded():
        for _ch in item.children():
            _loop_2(_ch)

def test_tree_sizes_simple_1():
    l0   = ttk.TTkTreeWidgetItem(["l0 XX0","XX0","XX0"], expanded=True)
    l1   = ttk.TTkTreeWidgetItem(["l1 String A", "String B", "String C"], expanded=True)
    l2   = ttk.TTkTreeWidgetItem(["l2 String AA", "String BB", "String CC"], expanded=True)
    l3   = ttk.TTkTreeWidgetItem(["l3 String AAA\nAAA\nAAA", "String BBB", "String CCC"], expanded=False)
    l4   = ttk.TTkTreeWidgetItem(["l4 String AAAA", "String BBBB", "String CCCC"], expanded=True)
    l5   = ttk.TTkTreeWidgetItem(["l5 String AAAAA", "String BBBBB\nB\nB", "String CCCCC"], expanded=True)

    l0.addChildren([l1,l2,l4])
    l1.addChild(l3)
    l3.addChild(l5)

    _loop_1(l0)

def test_tree_sizes_simple_2():
    l0   = ttk.TTkTreeWidgetItem(["XX0","XX0","XX0"], expanded=False)
    l1   = ttk.TTkTreeWidgetItem(["String A", "String B", "String C"], expanded=False)
    l2   = ttk.TTkTreeWidgetItem(["String AA", "String BB", "String CC"], expanded=False)

    l0.addChild(l1)

    l0.setExpanded(True)
    l1.setExpanded(True)
    l2.setExpanded(True)

    l1.addChild(l2)

    assert _get_node_size(l0) == l0.size() , _format_item(l0)

def test_tree_sizes_simple_3():
    l0   = ttk.TTkTreeWidgetItem(["XX0","XX0","XX0"], expanded=True)
    l1   = ttk.TTkTreeWidgetItem(["String A", "String B", "String C"], expanded=True)
    l3   = ttk.TTkTreeWidgetItem(["String AAA\nAAA\nAAA", "String BBB", "String CCC"], expanded=False)
    l5   = ttk.TTkTreeWidgetItem(["String AAAAA", "String BBBBB\nB\nB", "String CCCCC"], expanded=True)

    l0.addChild(l1)
    l1.addChild(l3)
    l3.addChild(l5)

    _loop_1(l0)

def test_tree_sizes_simple_4_expanding():
    l0   = ttk.TTkTreeWidgetItem(["XX0","XX0","XX0"], expanded=True)
    l1   = ttk.TTkTreeWidgetItem(["String A", "String B", "String C"], expanded=True)
    l2   = ttk.TTkTreeWidgetItem(["String AA", "String BB", "String CC"], expanded=True)
    l3   = ttk.TTkTreeWidgetItem(["String AAA\nAAA\nAAA", "String BBB", "String CCC"], expanded=False)
    l4   = ttk.TTkTreeWidgetItem(["String AAAA", "String BBBB", "String CCCC"], expanded=True)
    l5   = ttk.TTkTreeWidgetItem(["String AAAAA", "String BBBBB\nB\nB", "String CCCCC"], expanded=True)

    l0.addChildren([l1,l2,l4])
    l1.addChild(l3)
    l3.addChild(l5)

    def _expand_test(item:ttk.TTkTreeWidgetItem):
        item.setExpanded(True)
        _loop_1(item)
        item.setExpanded(False)
        _loop_1(item)
        item.setExpanded(True)
        _loop_1(item)
        for ch in item.children():
            ch.setExpanded(True)
            _loop_1(item)
            ch.setExpanded(False)
            _loop_1(item)
            ch.setExpanded(True)
            _loop_1(item)
            ch.collapseAll()
            _loop_1(item)
            ch.expandAll()
            _loop_1(item)
        item.collapseAll()
        _loop_1(item)
        item.expandAll()
        _loop_1(item)

    _expand_test(l0)
    _expand_test(l1)
    _expand_test(l2)
    _expand_test(l3)
    _expand_test(l4)
    _expand_test(l5)

def test_tree_sizes_widgets_1():

    btn_1 = ttk.TTkButton(text='Test B 1', border=True, height=5)
    btn_2 = ttk.TTkButton(text='Test B 2', border=True, height=5)
    btn_3 = ttk.TTkButton(text='Test B 3', border=True, height=5)

    l0   = ttk.TTkTreeWidgetItem(["l0 XX0","XX0","XX0"], expanded=True)
    l1   = ttk.TTkTreeWidgetItem(["l1 String A", "String B", "String C"], expanded=True)
    l2   = ttk.TTkTreeWidgetItem(["l2 String AA", "String BB", "String CC"], expanded=True)
    l3   = ttk.TTkTreeWidgetItem([btn_1, "l3 String BBB", "String CCC"], expanded=False)
    l4   = ttk.TTkTreeWidgetItem(["l4 String AAAA", "String BBBB", btn_3], expanded=True)
    l5   = ttk.TTkTreeWidgetItem(["l5 String AAAAA", btn_2, "String CCCCC"], expanded=True)

    l0.addChildren([l1,l2,l4])
    l1.addChild(l3)
    l3.addChild(l5)

    print('\nTree:')
    _print_tree(l0)

    _loop_1(l0)

    assert l0.size() == 13
    btn_1.resize(10,10)
    assert l0.size() == 18
    btn_2.resize(10,10)
    assert l0.size() == 18
    btn_3.resize(10,10)
    assert l0.size() == 23

def test_tree_sizes_complex():
    tree,c1,c2 = _create_tree()

    _loop_1(tree)

    tree,c1,c2 = _create_tree()

    _loop_2(tree)

def test_tree_sizes_adding_nodes():
    tree,c1,c2 = _create_tree()

    _loop_1(tree)
    _add_children(c1)
    _loop_1(tree)
    _add_children(c2)
    _loop_1(tree)

    tree,c1,c2 = _create_tree()

    _loop_2(tree)
    _add_children(c1)
    _loop_1(tree)
    _add_children(c2)
    _loop_1(tree)

def _get_full_tree_page(item:ttk.TTkTreeWidgetItem) -> List[ttk.TTkTreeWidgetItem]:
    ret = [item]*item._height
    if item.isExpanded():
        for ch in item.children():
            ret.extend(_get_full_tree_page(ch))
    return ret

def test_tree_get_page():
    tree,c1,c2 = _create_tree()

    full_page = _get_full_tree_page(tree)

    print('\nTree:')
    _print_tree(tree)

    def _test_page(index,size):
        page = tree._get_page(0,index,size)
        # print(f"Testing: {index=} {size=} , page size={len(page)}")
        assert (
            [f"{c.isExpanded()} {c.data(0)}" for c in full_page[index:index+size]] ==
            [f"{c.isExpanded()} {c.data(0)}" for _,_,c in page] )

    # _test_page(0,1)
    # _test_page(0,2)
    # _test_page(0,3)
    # _test_page(0,4)
    # _test_page(0,5)
    # _test_page(0,5)
    # _test_page(0,6)
    # _test_page(0,7)
    # _test_page(0,10)
    # _test_page(0,100)

    for i in range(0,100,1):
        for j in range(0,100,1):
            _test_page(i,j)

    print("\n - 0,10")
    page = tree._get_page(0,0,10)
    for a,b,c in page:
        print(a, b, '  '*a, _format_item(c))

    print("\n - 2,5")
    page = tree._get_page(0,2,5)
    for a,b,c in page:
        print(a, b, '  '*a, _format_item(c))

def test_tree_sort():
    tree,c1,c2 = _create_tree()

    def _test():
        full_page = _get_full_tree_page(tree)
        page = tree._get_page(0,0,10000)
        assert (
            [f"{c.isExpanded()} {c.data(0)}" for c in full_page] ==
            [f"{c.isExpanded()} {c.data(0)}" for _,_,c in page] )

    _test()

    tree.sortChildren(0,ttk.TTkK.AscendingOrder)
    _test()

    tree.sortChildren(0,ttk.TTkK.DescendingOrder)
    _test()

    tree.sortChildren(1,ttk.TTkK.AscendingOrder)
    _test()

    tree.sortChildren(1,ttk.TTkK.DescendingOrder)
    _test()

    tree.sortChildren(2,ttk.TTkK.AscendingOrder)
    _test()

    tree.sortChildren(2,ttk.TTkK.DescendingOrder)
    _test()


def test_tree_take_child():
    tree,c1,c2 = _create_tree()

    print('\nTree:')
    _print_tree(tree)

    def _test_page():
        full_page = _get_full_tree_page(tree)
        page = tree._get_page(0,0,1000)
        assert len(full_page) == tree.size() == len(page)
        assert (
            [f"{c.isExpanded()} {c.data(0)}" for c in full_page] ==
            [f"{c.isExpanded()} {c.data(0)}" for _,_,c in page] )
        print(f"Testing: size={len(page)},{tree.size()}")

    _test_page()

    c2.takeChild(1)
    _test_page()

    c1.takeChildren()
    _test_page()

def test_tree_show_hide():
    l0   = ttk.TTkTreeWidgetItem(["l0", "l0", "l0", "l0", "l0"],expanded=True)
    l1   = ttk.TTkTreeWidgetItem(["l1", "l1", "l1", "l1", "l1"],expanded=True)
    l2   = ttk.TTkTreeWidgetItem(["l2", "l2", "l2", "l2", "l2"],expanded=True)
    l3   = ttk.TTkTreeWidgetItem(["l3", "l3", "l3", "l3", "l3"],expanded=True)
    l4   = ttk.TTkTreeWidgetItem(["l4", "l4", "l4", "l4", "l4"],expanded=True)
    l5   = ttk.TTkTreeWidgetItem(["l5", "l5", "l5", "l5", "l5"],expanded=True)

    l0.addChildren([l1,l2,l4])
    l1.addChild(l3)
    l3.addChild(l5)

    print(l0.size())
    l5.setHidden(True)
    print(l0.size())
    l4.setHidden(True)
    print(l0.size())
    l5.setHidden(False)
    print(l0.size())
    l4.setHidden(False)
    print(l0.size())
