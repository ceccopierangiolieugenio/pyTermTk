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

__all__ = ['PTP_Engine']

import os
import sys
import json
import threading
import subprocess
from pathlib import Path
from dataclasses import dataclass, asdict, fields
from typing import Dict, Any, Optional, List

import TermTk as ttk

from _030.pytest_data import PTP_TestResult, PTP_ScanResult

def _strip_result(result: str) -> str:
    lines = result.splitlines()
    indent = min(len(line) - len(line.lstrip()) for line in lines if line.strip())
    result = "\n".join(line[indent:] for line in lines)
    return result.lstrip('\n')

class PTP_Engine():
    __slots__ = (
        '_scan_lock', '_test_lock',
        'itemScanned','testResultReady',
        'errorReported',
        'endScan', 'endTest')

    def __init__(self):
        self.itemScanned = ttk.pyTTkSignal(PTP_ScanResult)
        self.testResultReady = ttk.pyTTkSignal(PTP_TestResult)
        self.errorReported = ttk.pyTTkSignal(str)
        self.endScan = ttk.pyTTkSignal()
        self.endTest = ttk.pyTTkSignal()
        self._scan_lock = threading.RLock()
        self._test_lock = threading.RLock()

    def scan(self) -> Dict:
        threading.Thread(target=self._scan_thread).start()

    def _scan_thread(self):
        with self._scan_lock:
            dirname = os.path.dirname(__file__)
            script_file = Path(dirname) / 'scripts' / '_main_scan.py'
            script = script_file.read_text()
            # Run the script in a subprocess and capture output
            process = subprocess.Popen(
                [sys.executable, "-c", script, dirname],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,  # Line buffered
                universal_newlines=True
            )

            def read_stdout():
                for line in iter(process.stdout.readline, ''):
                    line = line.strip()
                    if line:
                        try:
                            result_dict = json.loads(line)
                            result = PTP_ScanResult(**result_dict)
                            self.itemScanned.emit(result)
                        except (json.JSONDecodeError, KeyError) as e:
                            ttk.TTkLog.error(f"Error parsing test result: {line}")
                process.stdout.close()

            def read_stderr():
                for line in iter(process.stderr.readline, ''):
                    self.errorReported.emit(line)
                process.stderr.close()

            # Start threads to read stdout and stderr
            stdout_thread = threading.Thread(target=read_stdout)
            stderr_thread = threading.Thread(target=read_stderr)

            stdout_thread.start()
            stderr_thread.start()

            # Wait for process to complete
            process.wait()

            self.endScan.emit()


    def run_all_tests(self):
        self.run_tests('.')

    def run_tests(self, test_path:str):
        threading.Thread(target=self._run_tests_thread, args=(test_path,)).start()

    def _run_tests_thread(self, test_path:str):
        with self._test_lock:
            dirname = os.path.dirname(__file__)
            script_file = Path(dirname) / 'scripts' / '_main_tests.py'
            script = script_file.read_text()

            # Run the script in a subprocess with streaming output
            process = subprocess.Popen(
                [sys.executable, "-c", script, dirname, test_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,  # Line buffered
                universal_newlines=True
            )

            def read_stdout():
                for line in iter(process.stdout.readline, ''):
                    line = line.strip()
                    if line:
                        try:
                            result_dict = json.loads(line)
                            result = PTP_TestResult(**result_dict)
                            self.testResultReady.emit(result)
                        except (json.JSONDecodeError, KeyError) as e:
                            ttk.TTkLog.error(f"Error parsing test result: {line}")
                process.stdout.close()

            def read_stderr():
                for line in iter(process.stderr.readline, ''):
                    self.errorReported.emit(line)
                process.stderr.close()

            # Start threads to read stdout and stderr
            stdout_thread = threading.Thread(target=read_stdout)
            stderr_thread = threading.Thread(target=read_stderr)

            stdout_thread.start()
            stderr_thread.start()

            # Wait for process to complete
            process.wait()

            self.endTest.emit()
