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
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../libs/pyTermTk'))

import TermTk as ttk
from ttkode.plugin import (
    TTkodePlugin,
    TTkodePluginWidget,
    TTkodePluginWidgetActivity,
    TTkodePluginWidgetPanel
)


class TestTTkodePluginWidget:
    """Test the base plugin widget class."""

    def test_plugin_widget_creation(self):
        """Test creating a basic plugin widget."""
        widget = ttk.TTkWidget()
        plugin_widget = TTkodePluginWidget(widget=widget)

        assert plugin_widget.widget is widget

    def test_plugin_widget_activity_creation(self):
        """Test creating an activity plugin widget."""
        widget = ttk.TTkWidget()
        icon = ttk.TTkString("📁")
        name = "TestActivity"

        activity_widget = TTkodePluginWidgetActivity(
            widget=widget,
            activityName=name,
            icon=icon
        )

        assert activity_widget.widget is widget
        assert activity_widget.activityName == name
        assert activity_widget.icon == icon

    def test_plugin_widget_panel_creation(self):
        """Test creating a panel plugin widget."""
        widget = ttk.TTkWidget()
        panel_name = "TestPanel"

        panel_widget = TTkodePluginWidgetPanel(
            widget=widget,
            panelName=panel_name
        )

        assert panel_widget.widget is widget
        assert panel_widget.panelName == panel_name


class TestTTkodePlugin:
    """Test the plugin system."""

    def test_plugin_basic_creation(self):
        """Test creating a basic plugin."""
        plugin = TTkodePlugin(name="TestPlugin")

        assert plugin.name == "TestPlugin"
        assert plugin.init is None
        assert plugin.apply is None
        assert plugin.run is None
        assert plugin.widgets == []
        assert plugin in TTkodePlugin.instances

    def test_plugin_with_callbacks(self):
        """Test plugin with init, apply, and run callbacks."""
        init_called = []
        apply_called = []
        run_called = []

        def init_cb():
            init_called.append(True)

        def apply_cb():
            apply_called.append(True)

        def run_cb():
            run_called.append(True)

        plugin = TTkodePlugin(
            name="CallbackPlugin",
            init=init_cb,
            apply=apply_cb,
            run=run_cb
        )

        # Execute callbacks
        if plugin.init:
            plugin.init()
        if plugin.apply:
            plugin.apply()
        if plugin.run:
            plugin.run()

        assert len(init_called) == 1
        assert len(apply_called) == 1
        assert len(run_called) == 1

    def test_plugin_with_widgets(self):
        """Test plugin with associated widgets."""
        widget1 = ttk.TTkWidget()
        widget2 = ttk.TTkWidget()

        plugin_widget1 = TTkodePluginWidget(widget=widget1)
        plugin_widget2 = TTkodePluginWidgetActivity(
            widget=widget2,
            activityName="Activity",
            icon=ttk.TTkString("🔧")
        )

        plugin = TTkodePlugin(
            name="WidgetPlugin",
            widgets=[plugin_widget1, plugin_widget2]
        )

        assert len(plugin.widgets) == 2
        assert plugin.widgets[0] is plugin_widget1
        assert plugin.widgets[1] is plugin_widget2

    def test_plugin_instances_list(self):
        """Test that plugins are registered in instances list."""
        initial_count = len(TTkodePlugin.instances)

        plugin1 = TTkodePlugin(name="Plugin1")
        plugin2 = TTkodePlugin(name="Plugin2")

        assert len(TTkodePlugin.instances) == initial_count + 2
        assert plugin1 in TTkodePlugin.instances
        assert plugin2 in TTkodePlugin.instances

    def test_plugin_with_all_widget_types(self):
        """Test plugin containing different types of widgets."""
        base_widget = ttk.TTkWidget()
        activity_widget = ttk.TTkWidget()
        panel_widget = ttk.TTkWidget()

        widgets = [
            TTkodePluginWidget(widget=base_widget),
            TTkodePluginWidgetActivity(
                widget=activity_widget,
                activityName="MyActivity",
                icon=ttk.TTkString("⚙️")
            ),
            TTkodePluginWidgetPanel(
                widget=panel_widget,
                panelName="MyPanel"
            )
        ]

        plugin = TTkodePlugin(name="CompletePlugin", widgets=widgets)

        assert len(plugin.widgets) == 3
        assert isinstance(plugin.widgets[0], TTkodePluginWidget)
        assert isinstance(plugin.widgets[1], TTkodePluginWidgetActivity)
        assert isinstance(plugin.widgets[2], TTkodePluginWidgetPanel)

    def test_plugin_callback_execution_order(self):
        """Test that plugin callbacks can be executed in order."""
        execution_order = []

        def init_cb():
            execution_order.append('init')

        def apply_cb():
            execution_order.append('apply')

        def run_cb():
            execution_order.append('run')

        plugin = TTkodePlugin(
            name="OrderPlugin",
            init=init_cb,
            apply=apply_cb,
            run=run_cb
        )

        # Simulate the plugin lifecycle
        if plugin.init:
            plugin.init()
        if plugin.apply:
            plugin.apply()
        if plugin.run:
            plugin.run()

        assert execution_order == ['init', 'apply', 'run']
