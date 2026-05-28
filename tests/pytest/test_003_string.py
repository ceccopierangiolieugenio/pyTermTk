#!/usr/bin/env python3
# MIT License
#
# Copyright (c) 2022 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

sys.path.append(os.path.join(sys.path[0],'../../libs/pyTermTk'))

import TermTk

def test_stringAlign1():
    test1 = TermTk.TTkString('Yes\u231b\u231b\u231b') # 'Yes⌛⌛⌛'
    print(f"Testcase: |{str(test1)}|")

    for width in range(0, 15):
        aligned = test1.align(width=width, alignment=TermTk.TTkK.CENTER_ALIGN)
        print(f"width={width:2}: |{aligned}|")

    # width= 0: |Yes⌛⌛⌛|
    assert 'Yes⌛⌛⌛'    == str(test1.align(width= 0, alignment=TermTk.TTkK.CENTER_ALIGN))
    # width= 1: |Y|
    assert 'Y'            == str(test1.align(width= 1, alignment=TermTk.TTkK.CENTER_ALIGN))
    # width= 2: |Ye|
    assert 'Ye'           == str(test1.align(width= 2, alignment=TermTk.TTkK.CENTER_ALIGN))
    # width= 3: |Yes|
    assert 'Yes'          == str(test1.align(width= 3, alignment=TermTk.TTkK.CENTER_ALIGN))
    # width= 4: |Yes≽|
    assert 'Yes≽'         == str(test1.align(width= 4, alignment=TermTk.TTkK.CENTER_ALIGN))
    # width= 5: |Yes⌛|
    assert 'Yes⌛'        == str(test1.align(width= 5, alignment=TermTk.TTkK.CENTER_ALIGN))
    # width= 6: |Yes⌛≽|
    assert 'Yes⌛≽'       == str(test1.align(width= 6, alignment=TermTk.TTkK.CENTER_ALIGN))
    # width= 7: |Yes⌛⌛|
    assert 'Yes⌛⌛'      == str(test1.align(width= 7, alignment=TermTk.TTkK.CENTER_ALIGN))
    # width= 8: |Yes⌛⌛≽|
    assert 'Yes⌛⌛≽'     == str(test1.align(width= 8, alignment=TermTk.TTkK.CENTER_ALIGN))
    # width= 9: |Yes⌛⌛⌛|
    assert 'Yes⌛⌛⌛'    == str(test1.align(width= 9, alignment=TermTk.TTkK.CENTER_ALIGN))
    # width=10: |Yes⌛⌛⌛ |
    assert 'Yes⌛⌛⌛ '   == str(test1.align(width=10, alignment=TermTk.TTkK.CENTER_ALIGN))
    # width=11: | Yes⌛⌛⌛ |
    assert ' Yes⌛⌛⌛ '  == str(test1.align(width=11, alignment=TermTk.TTkK.CENTER_ALIGN))
    # width=12: | Yes⌛⌛⌛  |
    assert ' Yes⌛⌛⌛  ' == str(test1.align(width=12, alignment=TermTk.TTkK.CENTER_ALIGN))
    # width=13: |  Yes⌛⌛⌛  |
    assert '  Yes⌛⌛⌛  '== str(test1.align(width=13, alignment=TermTk.TTkK.CENTER_ALIGN))
    # width=14: |  Yes⌛⌛⌛   |
    assert '  Yes⌛⌛⌛   '==str(test1.align(width=14, alignment=TermTk.TTkK.CENTER_ALIGN))


def test_ttkstring_copy_constructor_is_independent():
    original = TermTk.TTkString('abc', TermTk.TTkColor.fg('#00ff00'))
    copied = TermTk.TTkString(original)
    original_ansi = original.toAnsi(strip=True)

    updated = copied.setColorAt(0, TermTk.TTkColor.fg('#ff0000'))

    assert updated is not copied
    assert original.toAnsi(strip=True) == original_ansi
    assert updated.toAnsi(strip=True) != original_ansi


def test_ttkstring_add_color_returns_independent_instance():
    original = TermTk.TTkString('abc', TermTk.TTkColor.fg('#00ff00'))
    recolored = original + TermTk.TTkColor.fg('#0000ff')
    original_ansi = original.toAnsi(strip=True)

    updated = recolored.setColorAt(1, TermTk.TTkColor.fg('#ffffff'))

    assert updated is not recolored
    assert original.toAnsi(strip=True) == original_ansi
    assert updated.toAnsi(strip=True) != original_ansi


def test_replace_expanding_match_keeps_full_output_text():
    txt = TermTk.TTkString('abc')

    replaced = txt.replace('a', 'ZZ')

    assert str(replaced) == 'ZZbc'
    assert replaced.toAnsi(strip=True) == 'ZZbc'


def test_complete_color_applies_match_at_start_of_text():
    txt = TermTk.TTkString('abc')
    txt_ansi = txt.toAnsi(strip=True)

    colorized = txt.completeColor(TermTk.TTkColor.BOLD, match='a')

    assert txt.toAnsi(strip=True) == txt_ansi
    assert colorized.toAnsi(strip=True) != txt_ansi


def test_extract_shortcuts_trailing_ampersand_does_not_crash():
    txt = TermTk.TTkString('Save &')

    extracted, shortcuts = txt.extractShortcuts()

    assert str(extracted) == 'Save '
    assert shortcuts == []


def test_lstrip_preserves_combining_char_display_width():
    txt = TermTk.TTkString('a\u0301')

    stripped = txt.lstrip(' ')

    assert stripped.termWidth() == 1


def test_set_color_at_out_of_range_raises_index_error():
    txt = TermTk.TTkString('abc')

    with pytest.raises(IndexError):
        txt.setColorAt(100, TermTk.TTkColor.BOLD)


def test_basic_dunder_conversions_and_comparisons():
    txt = TermTk.TTkString('12')

    assert len(txt) == 2
    assert bool(txt) is True
    assert int(txt) == 12
    assert float(txt) == 12.0
    assert complex(txt) == complex(12)
    assert txt == '12'
    assert txt < '99'
    assert txt >= TermTk.TTkString('12')


def test_sameas_distinguishes_text_and_color():
    a = TermTk.TTkString('abc', TermTk.TTkColor.fg('#101010'))
    b = TermTk.TTkString('abc', TermTk.TTkColor.fg('#101010'))
    c = TermTk.TTkString('abc', TermTk.TTkColor.fg('#202020'))
    d = TermTk.TTkString('abd', TermTk.TTkColor.fg('#101010'))

    assert a.sameAs(b)
    assert not a.sameAs(c)
    assert not a.sameAs(d)


def test_char_and_color_accessors():
    txt = TermTk.TTkString('abc', TermTk.TTkColor.fg('#00ff00'))

    assert txt.charAt(1) == 'b'
    assert txt.colorAt(0) == TermTk.TTkColor.fg('#00ff00')
    assert txt.colorAt(99) == TermTk.TTkColor()


def test_tab2spaces_and_tab_char_pos_mapping():
    txt = TermTk.TTkString('a\tb')
    expanded = txt.tab2spaces(4)

    assert str(expanded) == 'a   b'
    assert txt.tabCharPos(0, 4) == 0
    assert txt.tabCharPos(1, 4) == 1
    assert txt.tabCharPos(2, 4) == 1
    assert txt.tabCharPos(4, 4) == 2


def test_tab_char_pos_with_wide_chars():
    txt = TermTk.TTkString('界a\tb')

    assert txt.termWidth() == 5
    assert txt.tabCharPos(0, 4) == 0
    assert txt.tabCharPos(1, 4) == 0
    assert txt.tabCharPos(2, 4) == 1
    assert txt.tabCharPos(5, 4) == 4


def test_plain_text_ascii_and_ansi_roundtrip_plain():
    txt = TermTk.TTkString('plain text')

    assert txt.isPlainText()
    assert txt.toAscii() == 'plain text'
    assert txt.toAnsi(strip=True) == 'plain text'


def test_align_left_right_center_and_justify():
    txt = TermTk.TTkString('ab')

    assert str(txt.align(width=5, alignment=TermTk.TTkK.LEFT_ALIGN)) == 'ab   '
    assert str(txt.align(width=5, alignment=TermTk.TTkK.RIGHT_ALIGN)) == '   ab'
    assert str(txt.align(width=5, alignment=TermTk.TTkK.CENTER_ALIGN)) == ' ab  '

    just = TermTk.TTkString('a b c').align(width=7, alignment=TermTk.TTkK.JUSTIFY)
    assert str(just) == 'a  b  c'


def test_extract_shortcuts_regular_case():
    txt = TermTk.TTkString('&File &Edit')

    extracted, shortcuts = txt.extractShortcuts()

    assert str(extracted) == 'File Edit'
    assert shortcuts == ['F', 'E']


def test_replace_equal_shorter_longer_and_count():
    txt = TermTk.TTkString('aabbcc')

    assert str(txt.replace('bb', 'XX')) == 'aaXXcc'
    assert str(txt.replace('aa', 'Q')) == 'Qbbcc'
    assert str(txt.replace('cc', 'YYY')) == 'aabbYYY'
    assert str(txt.replace('a', 'Z', 1)) == 'Zabbcc'


def test_complete_color_by_range_and_full():
    txt = TermTk.TTkString('abcdef')

    full = txt.completeColor(TermTk.TTkColor.BOLD)
    part = txt.completeColor(TermTk.TTkColor.ITALIC, posFrom=2, posTo=4)

    assert full.toAnsi(strip=True) != txt.toAnsi(strip=True)
    assert part.toAnsi(strip=True) != txt.toAnsi(strip=True)
    assert str(part) == 'abcdef'


def test_set_color_by_range_match_and_full():
    txt = TermTk.TTkString('abcabc')

    full = txt.setColor(TermTk.TTkColor.fg('#112233'))
    match = txt.setColor(TermTk.TTkColor.fg('#445566'), match='bc')
    part = txt.setColor(TermTk.TTkColor.fg('#778899'), posFrom=1, posTo=3)

    assert str(full) == 'abcabc'
    assert str(match) == 'abcabc'
    assert str(part) == 'abcabc'
    assert full.toAnsi(strip=True) != txt.toAnsi(strip=True)
    assert match.toAnsi(strip=True) != txt.toAnsi(strip=True)
    assert part.toAnsi(strip=True) != txt.toAnsi(strip=True)


def test_substring_split_join_and_indexes():
    txt = TermTk.TTkString('one,two,three')

    assert str(txt.substring(4, 7)) == 'two'
    parts = txt.split(',')
    assert [str(p) for p in parts] == ['one', 'two', 'three']
    assert txt.getIndexes('o') == [0, 6]

    joined = TermTk.TTkString('|').join(parts)
    assert str(joined) == 'one|two|three'


def test_split_multi_char_separator_not_supported():
    txt = TermTk.TTkString('a::b')

    with pytest.raises(NotImplementedError):
        txt.split('::')


def test_search_find_findall_variants():
    txt = TermTk.TTkString('Abc abc ABC')

    assert txt.search(r'abc') is not None
    assert txt.search(r'abc', ignoreCase=True) is not None
    assert txt.find('abc') == 4
    assert txt.findall(r'abc') == ['abc']
    assert txt.findall(r'abc', ignoreCase=True) == ['Abc', 'abc', 'ABC']


def test_get_data_zero_width_combining_and_wide_chars():
    combining = TermTk.TTkString('a\u0301')
    wide = TermTk.TTkString('界x')

    c_text, c_colors = combining.getData()
    w_text, w_colors = wide.getData()

    assert ''.join(c_text) == 'a\u0301'
    assert len(c_colors) == 1
    assert ''.join(w_text).startswith('界')
    assert len(w_colors) == 3


def test_next_and_prev_positions_skip_combining_chars():
    txt = TermTk.TTkString('a\u0301b')

    assert txt.nextPos(0) == 2
    assert txt.prevPos(2) == 0


def test_radd_with_plain_string_preserves_text():
    txt = TermTk.TTkString('world')

    out = 'hello ' + txt

    assert str(out) == 'hello world'
