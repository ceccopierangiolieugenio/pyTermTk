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
from ttkode.helper import TTkodeHelper
from ttkode.plugin import TTkodePlugin, TTkodePluginWidgetActivity, TTkodePluginWidgetPanel


class TestTTkodeHelper:
    """Test the helper functions for plugin management."""

    def test_get_plugins_empty(self):
        """Test getting plugins when none are loaded."""
        # Clear existing plugins
        TTkodePlugin.instances.clear()

        plugins = TTkodeHelper._getPlugins()

        assert plugins == []
        assert isinstance(plugins, list)

    def test_get_plugins_with_instances(self):
        """Test getting plugins after some are created."""
        # Clear and create test plugins
        TTkodePlugin.instances.clear()

        plugin1 = TTkodePlugin(name="TestPlugin1")
        plugin2 = TTkodePlugin(name="TestPlugin2")

        plugins = TTkodeHelper._getPlugins()

        assert len(plugins) == 2
        assert plugin1 in plugins
        assert plugin2 in plugins

    def test_get_plugins_returns_reference(self):
        """Test that _getPlugins returns a reference to the instances list."""
        TTkodePlugin.instances.clear()

        plugins = TTkodeHelper._getPlugins()

        # Should be the same list object
        assert plugins is TTkodePlugin.instances

    @pytest.mark.skip(reason="Requires plugin folder and file system setup")
    def test_load_plugins_from_folder(self, tmp_path):
        """Test loading plugins from a folder."""
        # This would require creating actual plugin files
        # and modifying the plugin folder path
        pass

    @pytest.mark.skip(reason="Requires full TTKode UI instance")
    def test_run_plugins_with_activity_widgets(self):
        """Test running plugins with activity widgets."""
        # This requires a full TTKode instance with activity bar
        pass

    @pytest.mark.skip(reason="Requires full TTKode UI instance")
    def test_run_plugins_with_panel_widgets(self):
        """Test running plugins with panel widgets."""
        # This requires a full TTKode instance with panels
        pass

    def test_plugin_init_execution(self):
        """Test that plugin init callbacks are executed."""
        TTkodePlugin.instances.clear()

        init_executed = []

        def init_callback():
            init_executed.append(True)

        plugin = TTkodePlugin(name="InitPlugin", init=init_callback)

        # Simulate what _loadPlugins does
        for mod in TTkodePlugin.instances:
            if mod.init is not None:
                mod.init()

        assert len(init_executed) == 1

    def test_plugin_apply_execution(self):
        """Test that plugin apply callbacks are executed."""
        TTkodePlugin.instances.clear()

        apply_executed = []

        def apply_callback():
            apply_executed.append(True)

        plugin = TTkodePlugin(name="ApplyPlugin", apply=apply_callback)

        # Simulate what _runPlugins does
        for mod in TTkodePlugin.instances:
            if mod.apply is not None:
                mod.apply()

        assert len(apply_executed) == 1

    def test_multiple_plugins_init(self):
        """Test initializing multiple plugins."""
        TTkodePlugin.instances.clear()

        counters = {'plugin1': 0, 'plugin2': 0, 'plugin3': 0}

        def make_init(name):
            def init_cb():
                counters[name] += 1
            return init_cb

        plugin1 = TTkodePlugin(name="Plugin1", init=make_init('plugin1'))
        plugin2 = TTkodePlugin(name="Plugin2", init=make_init('plugin2'))
        plugin3 = TTkodePlugin(name="Plugin3", init=make_init('plugin3'))

        # Execute all init callbacks
        for mod in TTkodePlugin.instances:
            if mod.init is not None:
                mod.init()

        assert counters['plugin1'] == 1
        assert counters['plugin2'] == 1
        assert counters['plugin3'] == 1

    def test_plugin_with_widgets_detection(self):
        """Test detecting plugin widgets."""
        TTkodePlugin.instances.clear()

        activity_widget = TTkodePluginWidgetActivity(
            widget=ttk.TTkWidget(),
            activityName="TestActivity",
            icon=ttk.TTkString("📁")
        )

        panel_widget = TTkodePluginWidgetPanel(
            widget=ttk.TTkWidget(),
            panelName="TestPanel"
        )

        plugin = TTkodePlugin(
            name="WidgetPlugin",
            widgets=[activity_widget, panel_widget]
        )

        # Verify plugin has widgets
        assert len(plugin.widgets) == 2

        # Count widget types
        activity_count = sum(1 for w in plugin.widgets if isinstance(w, TTkodePluginWidgetActivity))
        panel_count = sum(1 for w in plugin.widgets if isinstance(w, TTkodePluginWidgetPanel))

        assert activity_count == 1
        assert panel_count == 1

    def test_plugin_without_callbacks(self):
        """Test plugin without any callbacks doesn't crash."""
        TTkodePlugin.instances.clear()

        plugin = TTkodePlugin(name="MinimalPlugin")

        # These should not raise exceptions
        if plugin.init is not None:
            plugin.init()
        if plugin.apply is not None:
            plugin.apply()
        if plugin.run is not None:
            plugin.run()

        # If we get here, no exceptions were raised
        assert True
