# MIT License
#
# Copyright (c) 2023 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

__all__ = ["TTkodeHelper"]

import os
import importlib, pkgutil

import TermTk as ttk
from .plugin import TTkodePlugin, TTkodePluginActivity
from .proxy import ttkodeProxy

class TTkodeHelper():
    @staticmethod
    def _loadPlugins():
        # Check for the plugin folder
        pluginFolder = os.path.join(os.path.dirname(os.path.abspath(__file__)),'plugins')
        if not os.path.exists(pluginFolder):
            ttk.TTkLog.error("No 'plugins' folder found in the 'tlogg' main directory")
        else:
            for fn in sorted(os.listdir(pluginFolder)):
                filePath = os.path.join(pluginFolder,fn)
                if not os.path.isfile(filePath): continue
                absolute_name = importlib.util.resolve_name(filePath, None)
                ttk.TTkLog.debug(absolute_name)
                loader = importlib.machinery.SourceFileLoader(fn, filePath)
                spec = importlib.util.spec_from_loader(loader.name, loader)
                mod = importlib.util.module_from_spec(spec)
                loader.exec_module(mod)

        # Check installed plugins
        for finder, name, ispkg in pkgutil.iter_modules():
            if name.startswith("ttkode_"):
                loader = importlib.find_loader(name)
                spec = importlib.util.find_spec(name)
                mod = importlib.util.module_from_spec(spec)
                # runpy.run_module(name)
                loader.exec_module(mod)

        # check the plugin folder
        for mod in TTkodePlugin.instances:
            if mod.init is not None:
                mod.init()

    @staticmethod
    def _runPlugins():
        for mod in TTkodePlugin.instances:
            if isinstance(mod, TTkodePluginActivity):
                ttkodeProxy.ttkode()._activityBar.addActivity(
                    name=mod.activityName,
                    icon=mod.icon,
                    widget=mod.widget)
            if mod.apply is not None:
                mod.apply()

    @staticmethod
    def _getPlugins():
        return TTkodePlugin.instances

