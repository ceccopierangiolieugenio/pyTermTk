#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2026 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

import os
import sys
import timeit
from typing import List, Tuple

sys.path.append(os.path.join(sys.path[0], '../..'))
import TermTk as ttk


def _build_lines(lines_count: int = 2500, words_per_line: int = 90) -> list[str]:
    token = 'abcdefghij'
    lines: list[str] = []
    for line_idx in range(lines_count):
        parts: list[str] = []
        for word_idx in range(words_per_line):
            parts.append(token)
            if word_idx % 11 == 0:
                parts.append('\t')
            else:
                parts.append(' ')
        parts.append(f'line{line_idx}')
        lines.append(''.join(parts))
    return lines


def _mk_wrapper(doc: ttk.TTkTextDocument, mode: ttk.TTkK.WrapMode, width: int = 36) -> ttk.TTkTextWrap:
    tw = ttk.TTkTextWrap()
    tw.setDocument(doc)
    tw.enable()
    tw.setWrapWidth(width)
    tw.setWordWrapMode(mode)
    return tw


RAW_LINES = _build_lines()
DOC_TEXT = '\n'.join(RAW_LINES)
DOC = ttk.TTkTextDocument(text=DOC_TEXT)
TTK_LINES: list[ttk.TTkString] = DOC._dataLines
WRAP_WIDTH = 36
VIEWPORT_ROWS = 60

TW_ANY = _mk_wrapper(DOC, ttk.TTkK.WrapAnywhere, WRAP_WIDTH)


class _EagerWrapLegacy:
    def __init__(self, lines: List[ttk.TTkString], mode: ttk.TTkK.WrapMode, width: int, tab_spaces: int = 4) -> None:
        self._lines_src = lines
        self._mode = mode
        self._width = width
        self._tab_spaces = tab_spaces

    def _wrap_line(self, dt: int, line: ttk.TTkString) -> List[Tuple[int, Tuple[int, int]]]:
        out: List[Tuple[int, Tuple[int, int]]] = []
        fr = 0
        cur = line
        if not len(cur):
            out.append((dt, (0, 0)))
            return out
        while len(cur):
            fl = cur.tab2spaces(self._tab_spaces)
            if fl.termWidth() <= self._width:
                out.append((dt, (fr, fr + len(cur) + 1)))
                break
            to = max(1, cur.tabCharPos(self._width, self._tab_spaces))
            if self._mode == ttk.TTkK.WordWrap:
                s = str(cur)
                new_to = to
                while new_to and (s[new_to] != ' ' and s[new_to] != '\t'):
                    new_to -= 1
                if new_to:
                    to = new_to
            out.append((dt, (fr, fr + to)))
            cur = cur.substring(to)
            fr += to
        return out

    def rewrap(self) -> int:
        rows = 0
        for dt, line in enumerate(self._lines_src):
            rows += len(self._wrap_line(dt, line))
        return rows


LEGACY_ANY = _EagerWrapLegacy(TTK_LINES, ttk.TTkK.WrapAnywhere, WRAP_WIDTH)


def test_ti_01_legacy_eager_full_rewrap() -> int:
    return LEGACY_ANY.rewrap()


def test_ti_02_fastwrap_first_viewport() -> int:
    TW_ANY.rewrap()
    rows = TW_ANY.screenRows(0, VIEWPORT_ROWS)
    return len(rows)


def test_ti_03_fastwrap_mid_viewport() -> int:
    TW_ANY.rewrap()
    rows = TW_ANY.screenRows(2000, VIEWPORT_ROWS)
    return len(rows)


def test_ti_04_fastwrap_full_materialize() -> int:
    TW_ANY.rewrap()
    TW_ANY.ensureScreenRows(10**9, 1)
    return TW_ANY.size()


def test_ti_05_wraplinecount_only() -> int:
    return sum(TW_ANY._wrapLineCount(line) for line in TTK_LINES)


def test_ti_06_len_wrapline_each() -> int:
    return sum(len(TW_ANY._wrapLine(i, line)) for i, line in enumerate(TTK_LINES))


def _run(loop: int = 8) -> None:
    results: dict[str, float] = {}

    print(f'lines={len(TTK_LINES)} chars_per_line~{len(str(TTK_LINES[0]))} width={WRAP_WIDTH} loop={loop}')
    for test_name in sorted([tn for tn in globals() if tn.startswith('test_ti_')]):
        result = timeit.timeit(f'{test_name}()', globals=globals(), number=loop)
        sec = result / loop
        fps = loop / result
        retval = globals()[test_name]()
        results[test_name] = sec
        print(f'{test_name} | {sec:.10f} sec. | {fps:12.3f} Fps | rows={retval}')

    print('')
    eager = results['test_ti_01_legacy_eager_full_rewrap']
    first_view = results['test_ti_02_fastwrap_first_viewport']
    mid_view = results['test_ti_03_fastwrap_mid_viewport']
    full_fast = results['test_ti_04_fastwrap_full_materialize']
    count_only = results['test_ti_05_wraplinecount_only']
    len_wrapline = results['test_ti_06_len_wrapline_each']

    print('Legacy eager vs incremental wrapping:')
    print(f'  eager vs first viewport: {eager / first_view:.2f}x slower')
    print(f'  eager vs mid viewport:   {eager / mid_view:.2f}x slower')
    print(f'  eager vs full scan:      {eager / full_fast:.2f}x slower')
    print('')
    print('_wrapLineCount vs len(_wrapLine) overhead:')
    print(f'  len(_wrapLine) / _wrapLineCount: {len_wrapline / count_only:.3f}x')


if __name__ == '__main__':
    _run()
