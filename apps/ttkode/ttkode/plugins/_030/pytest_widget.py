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

__all__ = ['PTP_PyTestWidget']

from typing import Dict, List, Any, Optional

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalTrueColorFormatter

import TermTk as ttk

from ttkode.proxy import ttkodeProxy
from ttkode.app.ttkode import TTKodeFileWidgetItem

from .pytest_tree import (
    _testStatus,
    PTP_TreeItem, PTP_TreeItemPath, PTP_TreeItemMethod,
    PTP_Tree, PTP_Action)
from .pytest_engine import PTP_Engine, PTP_TestResult, PTP_ScanResult
from .pytest_data import PTP_Node

def _strip_result(result: str) -> str:
    lines = result.splitlines()
    indent = min(len(line) - len(line.lstrip()) for line in lines if line.strip())
    result = "\n".join(line[indent:] for line in lines)
    return result.lstrip('\n')

_out_map = {
    'passed': ttk.TTkString('PASS', ttk.TTkColor.GREEN)+ttk.TTkColor.RST,
    'failed': ttk.TTkString('FAIL', ttk.TTkColor.RED)+ttk.TTkColor.RST
}
_error_color = ttk.TTkColor.fgbg('#FFFF00',"#FF0000")

class PTP_PyTestWidget(ttk.TTkContainer):
    __slots__ = (
        '_test_engine',
        '_res_tree','_test_results')
    _res_tree:PTP_Tree
    _test_results:ttk.TTkTextEdit

    def __init__(self, testResults=ttk.TTkTextEdit, **kwargs):
        self._test_results = testResults
        self._test_engine = PTP_Engine()
        super().__init__(**kwargs)
        self.setLayout(layout:=ttk.TTkGridLayout())

        layout.addWidget(btn_scan:=ttk.TTkButton(text="Scan", border=False), 0,0)
        layout.addWidget(btn_run:=ttk.TTkButton(text="Run", border=False), 0,1)
        layout.addWidget(res_tree:=PTP_Tree(dragDropMode=ttk.TTkK.DragDropMode.AllowDrag), 1,0,1,2)
        res_tree.setHeaderLabels(["Tests"])

        testResults.setText('Info Tests')

        self._res_tree = res_tree

        btn_scan.clicked.connect(self._scan)
        btn_run.clicked.connect(self._run_tests)
        self._test_engine.testResultReady.connect(self._test_updated)

        res_tree.actionPressed.connect(self._tree_action_pressed)
        res_tree.itemActivated.connect(self._tree_item_activated)

    @ttk.pyTTkSlot(PTP_Action)
    def _tree_action_pressed(self, action:PTP_Action) -> None:
        item = action.item
        if isinstance(item, PTP_TreeItem):
            self._mark_node(item.test_id(), outcome='undefined')
            self._test_results.clear()
            self._test_engine.run_tests(item.test_id())

    @ttk.pyTTkSlot(PTP_TreeItem, int)
    def _tree_item_activated(self, item:PTP_TreeItem, _):
        ttk.TTkLog.debug(item)
        if isinstance(item, PTP_TreeItemMethod):
            file = item.node().filename
            line = item.node().lineNumber
            ttkodeProxy.openFile(file, line)

    def _get_node_from_path(self, _n:ttk.TTkTreeWidgetItem, _p:str) -> Optional[PTP_TreeItem]:
        for _c in _n.children():
            if isinstance(_c, PTP_TreeItem) and _c.test_id() == _p:
                return _c
            if _cc:= self._get_node_from_path(_n=_c, _p=_p):
                return _cc
        return None

    @ttk.pyTTkSlot()
    def _scan(self):
        self._res_tree.clear()
        self._test_results.clear()

        def _get_or_add_path_in_node(_n:ttk.TTkTreeWidgetItem, _p:str, _name:str, _node:PTP_ScanResult) -> PTP_TreeItem:
            for _c in _n.children():
                if isinstance(_c, PTP_TreeItem) and _c.test_id() == _p:
                    return _c
            _ptp_node = _node.get_node()
            if _node.nodeId==_p: # This is the leaf test
                _n.addChild(_c:=PTP_TreeItemMethod(test_id=_p, name=_name, node=_ptp_node, expanded=True))
            else:
                _n.addChild(_c:=PTP_TreeItemPath(test_id=_p, name=_name, node=_ptp_node, expanded=True))
            return _c

        @ttk.pyTTkSlot(PTP_ScanResult)
        def _add_node(_node:PTP_ScanResult)->None:
            ttk.TTkLog.debug(_node)
            self._test_results.append(_node.nodeId)
            _node_id_split = _node.nodeId.split('::')
            _full_test_path = _node_id_split[0]
            _leaves = _node_id_split[1:]
            _tree_node: ttk.TTkTreeWidgetItem = self._res_tree.invisibleRootItem()
            _full_composite_test_path = ''
            ttk.TTkLog.debug(_node_id_split)
            ttk.TTkLog.debug(_full_test_path)
            for _test_path in _full_test_path.split('/'):
                if _full_composite_test_path:
                    _full_composite_test_path = '/'.join([_full_composite_test_path,_test_path])
                else:
                    _full_composite_test_path = _test_path
                ttk.TTkLog.debug(_full_composite_test_path)
                _tree_node = _get_or_add_path_in_node(_n=_tree_node, _p=_full_composite_test_path, _name=_test_path, _node=_node)
            for _leaf in _leaves:
                _full_composite_test_path = '::'.join([_full_composite_test_path,_leaf])
                _tree_node = _get_or_add_path_in_node(_n=_tree_node, _p=_full_composite_test_path, _name=_leaf, _node=_node)
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

    def _mark_node(self, _nodeid:str, outcome:str) -> None:
        status = {
            'passed' : _testStatus.Pass,
            'failed' : _testStatus.Fail,
        }.get(outcome, _testStatus.Undefined)
        def _recurse_node(_n:ttk.TTkTreeWidgetItem):
            for _c in _n.children():
                # ttk.TTkLog.debug(_c.data(0))
                if isinstance(_c, PTP_TreeItemPath):
                    if _nodeid.startswith(_c.test_id()):
                        if not ( _c.testStatus() == _testStatus.Fail and status == _testStatus.Pass ):
                            _c.setTestStatus(status)
                    elif _c.test_id().startswith(_nodeid):
                        _c.setTestStatus(status)
                elif isinstance(_c, PTP_TreeItemMethod) and _nodeid.startswith(_c.test_id()):
                    _c.setTestStatus(status)
                _recurse_node(_c)
        _recurse_node(self._res_tree.invisibleRootItem())

    def _clear_nodes(self, node:Optional[PTP_TreeItem] = None) -> None:
        status = _testStatus.Undefined
        def _recurse_node(_n:ttk.TTkTreeWidgetItem):
            for _c in _n.children():
                if isinstance(_c, PTP_TreeItem):
                    _c.setTestStatus(status)
                _recurse_node(_c)
        _recurse_node(node if node else self._res_tree.invisibleRootItem())

    @ttk.pyTTkSlot(PTP_TestResult)
    def _test_updated(self, test:PTP_TestResult) -> None:
        self._mark_node(_nodeid=test.nodeId, outcome=test.outcome)

        _outcome = _out_map.get(test.outcome, test.outcome)
        self._test_results.append(f"{test.nodeId}: " + _outcome + f" ({test.duration:.2f}s)")

        for (_s_name,_s_content) in test.sections:
            self._test_results.append(ttk.TTkString(_s_name, ttk.TTkColor.GREEN))
            self._test_results.append(_s_content)

        if test.outcome == 'failed':
            self._test_results.append(ttk.TTkString("◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤ ↳ Error: ◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤", ttk.TTkColor.RED))
            _code = test.longrepr
            _code_str = ttk.TTkString(highlight(_code, PythonLexer(), TerminalTrueColorFormatter(style='material')))
            _code_h_err = [
                _l.setColor(_error_color) if _l._text.startswith('E') else _l
                for _l in _code_str.split('\n')]
            self._test_results.append(ttk.TTkString('\n').join(_code_h_err))
            self._test_results.append(ttk.TTkString("◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤", ttk.TTkColor.RED))


    @ttk.pyTTkSlot()
    def _run_tests(self) -> None:
        self._clear_nodes()
        self._test_results.clear()
        self._test_engine.run_all_tests()