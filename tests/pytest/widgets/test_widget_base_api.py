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

import TermTk as ttk


def test_set_default_size_only_applies_when_size_is_not_already_defined():
    widget = ttk.TTkWidget()

    no_size_args = {}
    widget.setDefaultSize(no_size_args, 11, 7)
    assert no_size_args == {'width': 11, 'height': 7}

    explicit_size_args = {'size': (9, 3)}
    widget.setDefaultSize(explicit_size_args, 11, 7)
    assert explicit_size_args == {'size': (9, 3)}

    explicit_width_args = {'width': 5}
    widget.setDefaultSize(explicit_width_args, 11, 7)
    assert explicit_width_args == {'width': 5}


def test_set_visible_toggles_widget_visibility_state():
    widget = ttk.TTkWidget()

    assert widget.isVisible() is True

    widget.setVisible(False)
    assert widget.isVisible() is False

    widget.setVisible(True)
    assert widget.isVisible() is True


def test_set_current_style_emits_signal_only_when_style_changes():
    widget = ttk.TTkWidget()
    emitted = []
    widget.currentStyleChanged.connect(lambda style: emitted.append(style.copy()))

    current_style = widget.currentStyle()
    widget.setCurrentStyle(current_style.copy())
    assert emitted == []

    new_style = {'color': ttk.TTkColor.fg('#abcdef')}
    widget.setCurrentStyle(new_style)
    assert emitted == [new_style]


def test_merge_style_updates_current_style_when_active_bucket_changes():
    widget = ttk.TTkWidget()
    widget.setStyle({
        'default': {'color': ttk.TTkColor.fg('#111111')},
        'hover': {'color': ttk.TTkColor.fg('#222222')},
    })
    widget._processStyleEvent(ttk.TTkWidget._S_HOVER)

    emitted = []
    widget.currentStyleChanged.connect(lambda style: emitted.append(style.copy()))

    widget.mergeStyle({'hover': {'borderColor': ttk.TTkColor.fg('#333333')}})

    assert emitted
    assert 'borderColor' in widget.currentStyle()


def test_set_enabled_and_disabled_update_enabled_state():
    widget = ttk.TTkWidget()

    widget.setEnabled(False)
    assert widget.isEnabled() is False

    widget.setDisabled(False)
    assert widget.isEnabled() is True


def test_tooltip_and_name_lookup_behave_as_public_api():
    widget = ttk.TTkWidget(name='root-name')

    widget.setToolTip('my tooltip')
    assert str(widget.toolTip()) == 'my tooltip'

    assert widget.getWidgetByName('root-name') is widget
    assert widget.getWidgetByName('missing') is None


def test_close_unparents_hides_and_emits_closed_signal():
    container = ttk.TTkContainer()
    widget = ttk.TTkWidget(parent=container)

    closed = []
    widget.closed.connect(lambda closed_widget: closed.append(closed_widget))

    widget.close()

    assert widget.parentWidget() is None
    assert widget.isVisible() is False
    assert closed == [widget]
