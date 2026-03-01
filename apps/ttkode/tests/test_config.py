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
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../libs/pyTermTk'))

from ttkode.app.cfg import TTKodeCfg
from ttkode import __version__


class TestTTKodeCfg:
    """Test the configuration management system."""

    def test_default_values(self):
        """Test that configuration has correct default values."""
        assert TTKodeCfg.version == __version__
        assert TTKodeCfg.name == "ttkode"
        assert TTKodeCfg.cfgVersion == '1.0'
        assert TTKodeCfg.pathCfg == "."
        assert isinstance(TTKodeCfg.options, dict)
        assert TTKodeCfg.maxsearches == 200

    def test_options_is_dict(self):
        """Test that options is a dictionary."""
        assert isinstance(TTKodeCfg.options, dict)
        # Options can be modified
        original_options = TTKodeCfg.options.copy()
        TTKodeCfg.options['test_key'] = 'test_value'
        assert TTKodeCfg.options['test_key'] == 'test_value'
        # Restore original state
        TTKodeCfg.options = original_options

    def test_save_creates_directory(self, tmp_path):
        """Test that save creates the configuration directory if it doesn't exist."""
        original_path = TTKodeCfg.pathCfg
        TTKodeCfg.pathCfg = str(tmp_path / "config")

        # Directory shouldn't exist yet
        assert not os.path.exists(TTKodeCfg.pathCfg)

        # Save should create it
        TTKodeCfg.save()

        assert os.path.exists(TTKodeCfg.pathCfg)
        assert os.path.isdir(TTKodeCfg.pathCfg)

        # Restore original path
        TTKodeCfg.pathCfg = original_path

    def test_save_with_different_flags(self, tmp_path):
        """Test save method with different flag combinations."""
        original_path = TTKodeCfg.pathCfg
        TTKodeCfg.pathCfg = str(tmp_path / "config2")

        # Test with all flags
        TTKodeCfg.save(searches=True, filters=True, colors=True, options=True)
        assert os.path.exists(TTKodeCfg.pathCfg)

        # Test with individual flags
        TTKodeCfg.save(searches=False, filters=False, colors=False, options=True)
        TTKodeCfg.save(searches=True, filters=False, colors=False, options=False)
        TTKodeCfg.save(searches=False, filters=True, colors=False, options=False)
        TTKodeCfg.save(searches=False, filters=False, colors=True, options=False)

        # Restore original path
        TTKodeCfg.pathCfg = original_path

    def test_maxsearches_value(self):
        """Test that maxsearches has a reasonable default value."""
        assert isinstance(TTKodeCfg.maxsearches, int)
        assert TTKodeCfg.maxsearches > 0
        assert TTKodeCfg.maxsearches == 200

    def test_version_matches_package_version(self):
        """Test that config version matches package version."""
        from ttkode import __version__ as pkg_version
        assert TTKodeCfg.version == pkg_version

    def test_config_path_modification(self, tmp_path):
        """Test that pathCfg can be modified."""
        original_path = TTKodeCfg.pathCfg
        new_path = str(tmp_path / "new_config")

        TTKodeCfg.pathCfg = new_path
        assert TTKodeCfg.pathCfg == new_path

        # Restore original path
        TTKodeCfg.pathCfg = original_path

    def test_options_persistence(self):
        """Test that options can be set and retrieved."""
        original_options = TTKodeCfg.options.copy()

        # Set some options
        test_options = {
            'editor.fontSize': 12,
            'editor.tabSize': 4,
            'theme': 'dark'
        }
        TTKodeCfg.options = test_options

        # Verify options are set
        assert TTKodeCfg.options['editor.fontSize'] == 12
        assert TTKodeCfg.options['editor.tabSize'] == 4
        assert TTKodeCfg.options['theme'] == 'dark'

        # Restore original options
        TTKodeCfg.options = original_options
