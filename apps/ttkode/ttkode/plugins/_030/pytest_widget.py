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

__all__ = ['PyTestWidget']

import io
import os
import sys
import json
import pytest
import subprocess

from typing import Dict, List, Any, Optional

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalTrueColorFormatter

import TermTk as ttk

from ttkode import ttkodeProxy
from ttkode.app.ttkode import TTKodeFileWidgetItem

from .pytest_tree import _testStatus, TestTreeItemPath, TestTreeItemMethod
from .pytest_engine import PytestEngine, ScanItem

def _strip_result(result: str) -> str:
    lines = result.splitlines()
    indent = min(len(line) - len(line.lstrip()) for line in lines if line.strip())
    result = "\n".join(line[indent:] for line in lines)
    return result.lstrip('\n')

class PyTestWidget(ttk.TTkContainer):
    __slots__ = (
        '_test_engine',
        '_res_tree','_test_results')
    _res_tree:ttk.TTkTree
    _test_results:ttk.TTkTextEdit

    def __init__(self, testResults=ttk.TTkTextEdit, **kwargs):
        self._test_results = testResults
        self._test_engine = PytestEngine()
        super().__init__(**kwargs)
        self.setLayout(layout:=ttk.TTkGridLayout())

        layout.addWidget(btn_scan:=ttk.TTkButton(text="Scan", border=False), 0,0)
        layout.addWidget(btn_run:=ttk.TTkButton(text="Run", border=False), 0,1)
        layout.addWidget(res_tree:=ttk.TTkTree(), 1,0,1,2)
        res_tree.setHeaderLabels(["Tests"])


        testResults.setText('Ciaoooo Testsssss\nPippo')

        self._res_tree = res_tree

        btn_scan.clicked.connect(self._scan)
        btn_run.clicked.connect(self._run_tests)

    @ttk.pyTTkSlot()
    def _scan(self):
        self._res_tree.clear()
        self._test_results.clear()

        # _tree = {}
        # def _add_node(_node:str)->None:
        #     _full_path,_leaf = _node.split('::')
        #     _loop_tree = _tree
        #     for _path in _full_path.split('/'):
        #         if _path not in _loop_tree:
        #             _loop_tree[_path] = {}
        #         _loop_tree = _loop_tree[_path]
        #     _loop_tree[_leaf] = '_node'

        # for _r in results:
        #     self._test_results.append(f"{_r['nodeid']}")
        #     _add_node(_r['nodeid'])

        # def _iter_tree(_node:Dict,_path:str) -> List[ttk.TTkTreeWidgetItem]:
        #     _ret  = []
        #     for _n,_content in _node.items():
        #         if isinstance(_content, str):
        #             _test_call = f"{_path}::{_n}"
        #             _ret_node = TestTreeItemMethod([ttk.TTkString(_n)],test_call=_test_call)
        #         elif isinstance(_content, dict):
        #             _node_path = f"{_path}/{_n}" if _path else _n
        #             _ret_node = TestTreeItemPath([ttk.TTkString(_n)], path=_node_path, expanded=True)
        #             _ret_node.addChildren(_iter_tree(_content,_node_path))
        #         _ret.append(_ret_node)
        #     return _ret

        # self._test_results.append(f"{_tree}")
        # self._res_tree.addTopLevelItems(_iter_tree(_tree,''))
        # self._res_tree.resizeColumnToContents(0)

        def _get_or_add_path_in_node(_n:TestTreeItemPath, _p:str, _name:str) -> TestTreeItemPath:
            for _c in _n.children():
                if isinstance(_c, TestTreeItemPath) and _c.path() == _p:
                    return _c
            _n.addChild(_c:=TestTreeItemPath([ttk.TTkString(_name)], path=_p, expanded=True))
            return _c

        @ttk.pyTTkSlot(ScanItem)
        def _add_node(_node:ScanItem)->None:
            self._test_results.append(_node.nodeId)
            _node_id_split = _node.nodeId.split('::')
            _full_path = _node_id_split[0]
            _leaves = _node_id_split[1:]
            _tree_node = self._res_tree.invisibleRootItem()
            _full_composite_path = ''
            for _path in _full_path.split('/'):
                if _full_composite_path:
                    _full_composite_path = '/'.join([_full_composite_path,_path])
                else:
                    _full_composite_path = _path
                _tree_node = _get_or_add_path_in_node(_tree_node, _full_composite_path, _path)
            for _leaf in _leaves:
                _full_composite_path = '::'.join([_full_composite_path,_leaf])
                _tree_node = _get_or_add_path_in_node(_tree_node, _full_composite_path, _leaf)
                # _tree_node = _tree_node.addChild(TestTreeItemMethod([ttk.TTkString(_leaf)],test_call=_node.nodeId))

        @ttk.pyTTkSlot(str)
        def _add_error(error:str) -> None:
            self._test_results.append(ttk.TTkString(error, ttk.TTkColor.RED))

        @ttk.pyTTkSlot()
        def _end_scan() -> None:
            self._res_tree.resizeColumnToContents(0)
            self._test_engine.itemScanned.disconnect(_add_node)

        self._test_engine.errorReported.connect(_add_error)
        self._test_engine.endScan.connect(_end_scan)
        self._test_engine.itemScanned.connect(_add_node)

        self._test_engine.scan()


    @ttk.pyTTkSlot()
    def _run_tests(self):
        self._test_results.clear()

        def _mark_node(_nodeid:str, outcome:str):
            status = {
                'passed' : _testStatus.Pass,
                'failed' : _testStatus.Fail,
            }.get(outcome, _testStatus.Undefined)
            def _recurse_node(_n:ttk.TTkTreeWidgetItem):
                for _c in _n.children():
                    # ttk.TTkLog.debug(_c.data(0))
                    if isinstance(_c, TestTreeItemPath) and _nodeid.startswith(_c.path()):
                        _c.setTestStatus(status)
                    elif isinstance(_c, TestTreeItemMethod) and _nodeid.startswith(_c.test_call()):
                        _c.setTestStatus(status)
                    _recurse_node(_c)
            _recurse_node(self._res_tree.invisibleRootItem())

        results = PytestEngine.run_tests()
        _out_map = {
            'passed': ttk.TTkString('PASS', ttk.TTkColor.GREEN)+ttk.TTkColor.RST,
            'failed': ttk.TTkString('FAIL', ttk.TTkColor.RED)+ttk.TTkColor.RST
        }
        _error_color = ttk.TTkColor.fgbg('#FFFF00',"#FF0000")
        for _r in results:
            _outcome = _out_map.get(_r['outcome'], _r['outcome'])
            self._test_results.append(f"{_r['nodeid']}: " + _outcome + f" ({_r['duration']:.2f}s)")
            _mark_node(_r['nodeid'], _r['outcome'])
            if _r['outcome'] == 'failed':
                self._test_results.append(ttk.TTkString("◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤ ↳ Error: ◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤", ttk.TTkColor.RED))
                _code = _r['longrepr']
                _code_str = ttk.TTkString(highlight(_code, PythonLexer(), TerminalTrueColorFormatter(style='material')))
                _code_h_err = [
                    _l.setColor(_error_color) if _l._text.startswith('E') else _l
                    for _l in _code_str.split('\n')]
                self._test_results.append(ttk.TTkString('\n').join(_code_h_err))
                self._test_results.append(ttk.TTkString("◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤", ttk.TTkColor.RED))

