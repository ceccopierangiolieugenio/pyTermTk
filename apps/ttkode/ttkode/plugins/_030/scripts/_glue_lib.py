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

import sys
import json
import pytest

from dataclasses import asdict
from typing import Dict, Any

from _030.pytest_data import PTP_TestResult, PTP_ScanResult

class _Highlighter():
    _highlight = None

class _Dummy():
    _tw = _Highlighter()

class ResultCollector_Logreport:
    def pytest_configure(self, config:pytest.Config):
        config.pluginmanager.register(_Dummy(), "terminalreporter")
        # config.option.verbose = 2


    def pytest_runtest_logreport(self, report:pytest.TestReport) -> None:
        if report.when == "call":
            result = PTP_TestResult(
                nodeId = report.nodeid,
                outcome = report.outcome,
                duration = report.duration,
                sections = list(report.sections),
                longrepr = str(report.longrepr) if report.failed else None,
                location = report.location
            )

            # Print detailed output for failed tests (like terminal plugin does)
            # if report.failed and report.longrepr:
            #     print(f"\n{'='*70}")
            #     print(f"FAILED: {report.nodeid}")
            #     print(f"{'='*70}")
            #     print(report.longrepr)
            #     print()

            # # Print captured output sections
            # if report.sections:
            #     for section_name, section_content in report.sections:
            #         print(f"\n{'-'*70} {section_name} {'-'*70}")
            #         print(section_content)

            # print('REPORT: -------')
            # print(report)
            # print('SECTIONS: -------')
            # for s in report.sections:
            #     print('sec',s[0])
            #     print('cont',s[1])
            # print('LONGREPR: -------')
            # print(report.longrepr)
            # print('LOCATION: -------')
            # print(1,report.location[0])
            # print(2,report.location[1])
            # print(3,report.location[2])
            # # Print result immediately for real-time streaming
            # print('RET: -------')

            print(json.dumps(asdict(result)), flush=True)


class ResultCollector_ItemCollected:
    def __init__(self):
        self.results:Dict[str,Any] = []

    def pytest_itemcollected(self, item:pytest.Item) -> None:
        # Called during --collect-only
        relfspath, lineno, testname = item.location
        result = PTP_ScanResult(
            nodeId=item.nodeid,
            path=relfspath,
            lineno=lineno,
            testname=testname
        )
        print(json.dumps(asdict(result)), flush=True)
