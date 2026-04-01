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

sys.path.append(os.path.join(sys.path[0], '../../libs/pyTermTk'))

import TermTk as ttk


def _mk_wrap(text: str, width: int = 4, word_wrap: bool = False):
    doc = ttk.TTkTextDocument(text=text)
    tw = ttk.TTkTextWrap(document=doc)
    tw.enable()
    tw.setWrapWidth(width)
    if word_wrap:
        tw.setWordWrapMode(ttk.TTkK.WordWrap)
    else:
        tw.setWordWrapMode(ttk.TTkK.WrapAnywhere)
    return doc, tw


def test_screen_rows_wrap_anywhere_visible_window():
    _, tw = _mk_wrap('abcdefghij\nxyz', width=4)

    rows = tw.screenRows(0, 4)

    assert len(rows) == 4
    assert rows[0] == (0, (0, 4))
    assert rows[1] == (0, (4, 8))
    assert rows[2] == (0, (8, 11))
    assert rows[3] == (1, (0, 4))


def test_data_to_screen_and_back_roundtrip():
    _, tw = _mk_wrap('abcdefghij\nxyz', width=4)

    for pos in (0, 3, 4, 7, 9, 10):
        x, y = tw.dataToScreenPosition(0, pos)
        line, dpos = tw.screenToDataPosition(x, y)
        assert line == 0
        assert dpos == pos


def test_invalidate_from_data_line_drops_tail_prefix_cache():
    _, tw = _mk_wrap('line0-abcdefghij\nline1-abcdefghij\nline2-abcdefghij', width=6)

    tw.ensureScreenRows(0, 30)
    assert tw._processedLines == 3
    before_rows = tw._lineStartY[-1]

    tw.invalidateFromDataLine(1)

    assert tw._processedLines == 1
    assert len(tw._lineStartY) == 2
    assert tw._lineStartY[-1] < before_rows
    assert tw._checkpoints[-1][0] == 1
    assert tw._checkpoints[-1][1] == tw._lineStartY[-1]


def test_size_estimate_grows_with_partial_materialization():
    _, tw = _mk_wrap(('abcdefghij\n' * 50).rstrip('\n'), width=4)

    initial = tw.size()
    tw.ensureScreenRows(0, 6)
    after_first = tw.size()
    tw.ensureScreenRows(40, 6)
    after_more = tw.size()

    assert initial >= 50
    assert after_first >= 50
    assert after_more >= after_first
