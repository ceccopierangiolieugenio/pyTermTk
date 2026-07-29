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

import pytest

sys.path.append(os.path.join(sys.path[0], '../../libs/pyTermTk'))

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.TTkTerm.inputkey import TTkKeyEvent
from TermTk.TTkCore.TTkTerm.inputkey import TTkKeyEvent_Character
from TermTk.TTkCore.TTkTerm.inputkey import TTkKeyEvent_SpecialKey
from TermTk.TTkCore.TTkTerm.inputkey import key2str
from TermTk.TTkCore.TTkTerm.inputkey import mod2str


def test_parse_printable_character_returns_character_event():
    evt = TTkKeyEvent.parse('A')

    assert isinstance(evt, TTkKeyEvent_Character)
    assert evt.type == TTkK.Character
    assert evt.key == 'A'
    assert evt.code == 'A'
    assert evt.mod == TTkK.NoModifier


def test_parse_space_returns_character_event():
    evt = TTkKeyEvent.parse(' ')

    assert isinstance(evt, TTkKeyEvent_Character)
    assert evt.key == ' '
    assert evt.mod == TTkK.NoModifier


def test_parse_del_returns_special_backspace_event():
    evt = TTkKeyEvent.parse('\177')

    assert isinstance(evt, TTkKeyEvent_SpecialKey)
    assert evt.type == TTkK.SpecialKey
    assert evt.key == TTkK.Key_Backspace
    assert evt.mod == TTkK.NoModifier


@pytest.mark.parametrize(
    'code,key,mod',
    [
        ('\033[A', TTkK.Key_Up, TTkK.NoModifier),
        ('\033OA', TTkK.Key_Up, TTkK.NoModifier),
        ('\033[1;6D', TTkK.Key_Left, TTkK.ControlModifier | TTkK.ShiftModifier),
        ('\033[24;5~', TTkK.Key_F12, TTkK.ControlModifier),
        ('\x03', TTkK.Key_C, TTkK.ControlModifier),
        ('\033\x61', TTkK.Key_A, TTkK.AltModifier),
        ('\033\x41', TTkK.Key_A, TTkK.AltModifier | TTkK.ShiftModifier),
        ('\n', TTkK.Key_J, TTkK.ControlModifier),
        ('\r', TTkK.Key_Enter, TTkK.NoModifier),
    ],
)
def test_parse_known_special_inputs(code, key, mod):
    evt = TTkKeyEvent.parse(code)

    assert isinstance(evt, TTkKeyEvent_SpecialKey)
    assert evt.key == key
    assert evt.mod == mod


def test_parse_unknown_escape_sequence_returns_none():
    assert TTkKeyEvent.parse('\033[999~') is None


def test_character_equality_ignores_code_but_checks_key_and_modifier():
    lhs = TTkKeyEvent_Character('x', 'x', TTkK.NoModifier)
    rhs = TTkKeyEvent_Character('x', 'different-code', TTkK.NoModifier)
    different_mod = TTkKeyEvent_Character('x', 'x', TTkK.ShiftModifier)

    assert lhs == rhs
    assert lhs != different_mod
    assert lhs != None


def test_special_key_equality_and_hash_depend_on_key_and_modifier():
    lhs = TTkKeyEvent_SpecialKey(TTkK.Key_Tab, '\t', TTkK.ShiftModifier)
    rhs = TTkKeyEvent_SpecialKey(TTkK.Key_Tab, 'different-code', TTkK.ShiftModifier)
    different_key = TTkKeyEvent_SpecialKey(TTkK.Key_Enter, '\n', TTkK.ShiftModifier)

    assert lhs == rhs
    assert hash(lhs) == hash(rhs)
    assert lhs != different_key
    assert lhs != None


def test_event_str_replaces_escape_and_includes_human_readable_parts():
    evt = TTkKeyEvent_SpecialKey(TTkK.Key_Up, '\033[A', TTkK.ControlModifier | TTkK.ShiftModifier)

    rendered = str(evt)

    assert 'Key_Up' in rendered
    assert 'Control,Shift' not in rendered
    assert 'Shift,Control' in rendered
    assert '<ESC>[A' in rendered


def test_mod2str_handles_none_known_combo_and_unknown_bitmask():
    assert mod2str(TTkK.NoModifier) == ''
    assert mod2str(TTkK.ShiftModifier | TTkK.AltModifier) == 'Shift,Alt'
    assert mod2str(0x00000001) == 'NONE!!!'


def test_key2str_for_known_and_unknown_key_values():
    assert key2str(TTkK.Key_Left) == 'Key_Left'
    assert key2str(-12345) == 'NONE!!!'