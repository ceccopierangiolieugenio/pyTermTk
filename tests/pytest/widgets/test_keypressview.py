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

from typing import Any

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.propertyanimation import TTkEasingCurve
from TermTk.TTkCore.TTkTerm.inputkey import TTkKeyEvent_Character
from TermTk.TTkCore.TTkTerm.inputkey import TTkKeyEvent_SpecialKey
from TermTk.TTkCore.TTkTerm.inputmouse import TTkMouseEvent
from TermTk.TTkTestWidgets.keypressview import TTkKeyPressView


class _CanvasSpy:
    def __init__(self) -> None:
        self.calls = []

    def drawText(self, *, pos, text, color) -> None:
        self.calls.append({'pos': pos, 'text': text, 'color': color})


def _build_view() -> TTkKeyPressView:
    view = TTkKeyPressView(width=40, height=3)
    view._startFade = lambda: None
    return view


def test_process_input_dispatches_key_and_mouse_handlers(monkeypatch):
    view = _build_view()
    key_evt = TTkKeyEvent_Character('a', 'a', TTkK.NoModifier)
    mouse_evt = TTkMouseEvent(1, 2, TTkMouseEvent.LeftButton, TTkMouseEvent.Press, TTkK.NoModifier, 1, 'raw')

    seen = {'key': 0, 'mouse': 0}

    def _key(_: Any) -> None:
        seen['key'] += 1

    def _mouse(_: Any) -> None:
        seen['mouse'] += 1

    monkeypatch.setattr(view, '_addKey', _key)
    monkeypatch.setattr(view, '_addMouse', _mouse)

    view._processInput(key_evt, mouse_evt)

    assert seen == {'key': 1, 'mouse': 1}


def test_add_key_concatenates_consecutive_character_events():
    view = _build_view()

    view._addKey(TTkKeyEvent_Character('a', 'a', TTkK.NoModifier))
    view._addKey(TTkKeyEvent_Character('b', 'b', TTkK.NoModifier))

    assert len(view._keys) == 1
    assert view._keys[0][1] == 'ab'
    assert view._keys[0][2] == TTkK.Character
    assert view._keys[0][0] == 1


def test_add_key_creates_separate_entry_for_special_key_with_modifier_label():
    view = _build_view()
    key_evt = TTkKeyEvent_SpecialKey(TTkK.Key_Left, '\033[D', TTkK.ControlModifier | TTkK.ShiftModifier)

    view._addKey(TTkKeyEvent_Character('x', 'x', TTkK.NoModifier))
    view._addKey(key_evt)

    assert len(view._keys) == 2
    assert view._keys[1][1] == 'Shift,Control Left'
    assert view._keys[1][2] == TTkK.SpecialKey


def test_add_mouse_ignores_no_button_events():
    view = _build_view()
    evt = TTkMouseEvent(2, 3, TTkMouseEvent.NoButton, TTkMouseEvent.Move, TTkK.NoModifier, 1, 'raw')

    view._addMouse(evt)

    assert view._keys == []


def test_add_mouse_formats_drag_and_release_descriptions():
    view = _build_view()
    drag_evt = TTkMouseEvent(4, 5, TTkMouseEvent.LeftButton, TTkMouseEvent.Drag, TTkK.AltModifier, 1, 'raw')
    release_evt = TTkMouseEvent(4, 5, TTkMouseEvent.LeftButton, TTkMouseEvent.Release, TTkK.NoModifier, 2, 'raw')

    view._addMouse(drag_evt)
    view._addMouse(release_evt)

    assert view._keys[0][1] == 'M:(4, 5) Left Drag Alt'
    assert view._keys[1][1] == 'M:(4, 5) Left DoubleClick Release '


def test_start_fade_configures_animation_and_starts_it():
    view = TTkKeyPressView(width=10, height=3)

    calls = {}

    class _Anim:
        def setDuration(self, v):
            calls['duration'] = v

        def setStartValue(self, v):
            calls['start'] = v

        def setEndValue(self, v):
            calls['end'] = v

        def setEasingCurve(self, v):
            calls['curve'] = v

        def start(self):
            calls['started'] = True

    view._anim = _Anim()
    view._fadeDuration = 1.75

    view._startFade()

    assert calls['duration'] == 1.75
    assert calls['start'] == 0
    assert calls['end'] == 1
    assert calls['curve'] == TTkEasingCurve.OutExpo
    assert calls['started'] is True


def test_push_fade_decrements_existing_entries_and_keeps_last_entry_synced():
    view = _build_view()
    updates = {'count': 0}
    view.update = lambda: updates.__setitem__('count', updates['count'] + 1)
    view._keys = [
        [0.9, 'old', TTkK.SpecialKey],
        [0.8, 'new', TTkK.Character],
    ]

    view._pushFade(0.25)

    assert view._keys[0][0] == 0.65
    assert view._keys[1][0] == 0.75
    assert updates['count'] == 1


def test_txt2map_uses_fallback_bitmap_for_unknown_characters():
    view = _build_view()

    mapped = view.txt2map('\x00')

    assert mapped == ['...', '. .', '...']


def test_paint_event_draws_three_lines_for_each_key_entry():
    view = _build_view()
    view._keys = [[1.0, 'A', TTkK.Character]]
    canvas = _CanvasSpy()

    view.paintEvent(canvas)

    assert len(canvas.calls) == 3
    assert [call['pos'][1] for call in canvas.calls] == [0, 1, 2]
    assert all(call['text'] for call in canvas.calls)