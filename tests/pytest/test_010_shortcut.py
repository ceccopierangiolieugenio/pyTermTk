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

import pytest

import TermTk as ttk
from TermTk.TTkCore.shortcut import TTkShortcut
from TermTk.TTkCore.shortcut import _TTkKeySequence


@pytest.fixture(autouse=True)
def _reset_shortcuts_registry():
    TTkShortcut._shortcuts = {}


def test_key_sequence_without_modifier_creates_character_event():
    seq = _TTkKeySequence(ord('x'))

    assert isinstance(seq._key, ttk.TTkKeyEvent_Character)
    assert seq._key.key == 'x'
    assert seq._key.mod == ttk.TTkK.NoModifier


def test_key_sequence_with_modifier_creates_special_event():
    seq = _TTkKeySequence(ttk.TTkK.CTRL | ttk.TTkK.Key_A)

    assert isinstance(seq._key, ttk.TTkKeyEvent_SpecialKey)
    assert seq._key.key == ttk.TTkK.Key_A
    assert seq._key.mod == ttk.TTkK.ControlModifier


def test_shortcut_constructor_rejects_non_int_and_non_key_event():
    with pytest.raises(TypeError):
        TTkShortcut(key='bad')


def test_process_key_ignores_character_events():
    root = ttk.TTkWidget()
    _ = TTkShortcut(key=ttk.TTkK.CTRL | ttk.TTkK.Key_A, parent=root)

    handled = TTkShortcut.processKey(
        ttk.TTkKeyEvent_Character('a', 'a', ttk.TTkK.NoModifier),
        focusWidget=root,
    )

    assert handled is False


def test_process_key_emits_when_window_shortcut_matches():
    root = ttk.TTkWidget()
    key_event = ttk.TTkKeyEvent_SpecialKey(ttk.TTkK.Key_A, '', ttk.TTkK.ControlModifier)
    sc = TTkShortcut(key=ttk.TTkK.CTRL | ttk.TTkK.Key_A, parent=root, shortcutContext=ttk.TTkK.WindowShortcut)
    fired = []
    sc.activated.connect(lambda: fired.append('ok'))

    handled = TTkShortcut.processKey(key_event, focusWidget=root)

    assert handled is True
    assert fired == ['ok']


def test_process_key_requires_connection_before_emitting():
    root = ttk.TTkWidget()
    key_event = ttk.TTkKeyEvent_SpecialKey(ttk.TTkK.Key_B, '', ttk.TTkK.ControlModifier)
    _ = TTkShortcut(key=ttk.TTkK.CTRL | ttk.TTkK.Key_B, parent=root, shortcutContext=ttk.TTkK.WindowShortcut)

    handled = TTkShortcut.processKey(key_event, focusWidget=root)

    assert handled is False


def test_process_key_widget_context_requires_exact_focus_widget():
    class _FocusWidget:
        def __init__(self, parent=None):
            self._p = parent

        def parentWidget(self):
            return self._p

    parent = _FocusWidget()
    child = _FocusWidget(parent=parent)
    key_event = ttk.TTkKeyEvent_SpecialKey(ttk.TTkK.Key_C, '', ttk.TTkK.ControlModifier)
    sc = TTkShortcut(key=ttk.TTkK.CTRL | ttk.TTkK.Key_C, parent=parent, shortcutContext=ttk.TTkK.WidgetShortcut)
    fired = []
    sc.activated.connect(lambda: fired.append('ok'))

    handled_child = TTkShortcut.processKey(key_event, focusWidget=child)
    handled_parent = TTkShortcut.processKey(key_event, focusWidget=parent)

    assert handled_child is False
    assert handled_parent is True
    assert fired == ['ok']


def test_process_key_widget_with_children_context_matches_parent_chain_direction():
    class _FocusWidget:
        def __init__(self, parent=None):
            self._p = parent

        def parentWidget(self):
            return self._p

    ancestor = _FocusWidget()
    parent = _FocusWidget(parent=ancestor)
    child = _FocusWidget(parent=parent)
    key_event = ttk.TTkKeyEvent_SpecialKey(ttk.TTkK.Key_D, '', ttk.TTkK.ControlModifier)
    sc = TTkShortcut(
        key=ttk.TTkK.CTRL | ttk.TTkK.Key_D,
        parent=parent,
        shortcutContext=ttk.TTkK.WidgetWithChildrenShortcut,
    )
    fired = []
    sc.activated.connect(lambda: fired.append('ok'))

    handled_child = TTkShortcut.processKey(key_event, focusWidget=child)
    handled_ancestor = TTkShortcut.processKey(key_event, focusWidget=ancestor)

    assert handled_child is False
    assert handled_ancestor is True
    assert fired == ['ok']


def test_process_key_widget_with_children_without_parent_does_not_emit():
    focus = ttk.TTkWidget()
    key_event = ttk.TTkKeyEvent_SpecialKey(ttk.TTkK.Key_E, '', ttk.TTkK.ControlModifier)
    sc = TTkShortcut(
        key=ttk.TTkK.CTRL | ttk.TTkK.Key_E,
        parent=None,
        shortcutContext=ttk.TTkK.WidgetWithChildrenShortcut,
    )
    fired = []
    sc.activated.connect(lambda: fired.append('ok'))

    handled = TTkShortcut.processKey(key_event, focusWidget=focus)

    assert handled is False
    assert fired == []


def test_process_key_application_shortcut_emits_independent_of_focus_widget():
    focus = ttk.TTkWidget()
    key_event = ttk.TTkKeyEvent_SpecialKey(ttk.TTkK.Key_F, '', ttk.TTkK.ControlModifier)
    sc = TTkShortcut(
        key=ttk.TTkK.CTRL | ttk.TTkK.Key_F,
        parent=None,
        shortcutContext=ttk.TTkK.ApplicationShortcut,
    )
    fired = []
    sc.activated.connect(lambda: fired.append('ok'))

    handled = TTkShortcut.processKey(key_event, focusWidget=focus)

    assert handled is True
    assert fired == ['ok']


def test_process_key_stops_after_first_matching_connected_shortcut():
    focus = ttk.TTkWidget()
    key_event = ttk.TTkKeyEvent_SpecialKey(ttk.TTkK.Key_G, '', ttk.TTkK.ControlModifier)

    first = TTkShortcut(key=ttk.TTkK.CTRL | ttk.TTkK.Key_G, parent=focus, shortcutContext=ttk.TTkK.WindowShortcut)
    second = TTkShortcut(key=ttk.TTkK.CTRL | ttk.TTkK.Key_G, parent=focus, shortcutContext=ttk.TTkK.WindowShortcut)

    fired = []
    first.activated.connect(lambda: fired.append('first'))
    second.activated.connect(lambda: fired.append('second'))

    handled = TTkShortcut.processKey(key_event, focusWidget=focus)

    assert handled is True
    assert fired == ['first']


def test_process_key_returns_false_for_unregistered_special_key():
    focus = ttk.TTkWidget()
    key_event = ttk.TTkKeyEvent_SpecialKey(ttk.TTkK.Key_Z, '', ttk.TTkK.ControlModifier)

    handled = TTkShortcut.processKey(key_event, focusWidget=focus)

    assert handled is False
