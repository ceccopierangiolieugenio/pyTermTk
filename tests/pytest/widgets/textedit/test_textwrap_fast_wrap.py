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


def _mk_fast_wrap(text: str, width: int = 200):
    doc = ttk.TTkTextDocument(text=text)
    tw = ttk.TTkTextWrap(document=doc)
    tw.setEngine(ttk.TTkK.WrapEngine.FastWrap)
    tw.setWrapWidth(width)
    tw.setWordWrapMode(ttk.TTkK.WrapAnywhere)
    return doc, tw


def test_fast_wrap_inserts_middle_chunk_without_invalidating_following_chunks():
    text = '\n'.join(['line'] * 1200)
    _, tw = _mk_fast_wrap(text=text, width=200)

    # Build an initial chunk and then a far-away estimated chunk.
    tw.screenRows(0, 1)
    tw.screenRows(1000, 1)

    chunks_before = tw._wrapEngine._chunks  # type: ignore[attr-defined]
    assert len(chunks_before) == 2
    assert chunks_before[0].id == 0
    assert chunks_before[1].id == 6
    assert chunks_before[1].y == 1000

    # Requesting in-between should add chunk id=1 and shift later chunks forward.
    tw.screenRows(130, 1)

    chunks_after = tw._wrapEngine._chunks  # type: ignore[attr-defined]
    assert len(chunks_after) == 3
    assert [c.id for c in chunks_after] == [0, 1, 6]
    assert chunks_after[1].y == 128
    # Existing gap is preserved; only non-overlap is enforced.
    assert chunks_after[2].y == 1000
    assert chunks_after[2].y >= chunks_after[1].y + chunks_after[1].size


def test_fast_wrap_shifted_following_chunk_keeps_cached_coordinate_mapping():
    text = '\n'.join(['line'] * 1200)
    _, tw = _mk_fast_wrap(text=text, width=200)

    tw.screenRows(0, 1)
    tw.screenRows(1000, 1)
    tw.screenRows(130, 1)

    # The far chunk keeps its mapped y because there is still a gap after insertion.
    line, pos = tw.screenToDataPosition(0, 1000)
    assert (line, pos) == (768, 0)
