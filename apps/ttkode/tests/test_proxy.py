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

from ttkode.proxy import TTKodeViewerProxy


class TestTTKodeViewerProxy:
    """Test the viewer proxy class."""

    def test_viewer_proxy_creation(self):
        """Test creating a viewer proxy with a filename."""
        filename = "/path/to/test/file.py"
        proxy = TTKodeViewerProxy(filename)

        assert proxy.fileName() == filename

    def test_viewer_proxy_empty_filename(self):
        """Test viewer proxy with an empty filename."""
        proxy = TTKodeViewerProxy("")
        assert proxy.fileName() == ""

    def test_viewer_proxy_relative_path(self):
        """Test viewer proxy with a relative path."""
        filename = "relative/path/file.txt"
        proxy = TTKodeViewerProxy(filename)
        assert proxy.fileName() == filename

    def test_viewer_proxy_absolute_path(self):
        """Test viewer proxy with an absolute path."""
        filename = "/absolute/path/to/file.py"
        proxy = TTKodeViewerProxy(filename)
        assert proxy.fileName() == filename

    def test_viewer_proxy_with_special_chars(self):
        """Test viewer proxy with special characters in filename."""
        filename = "/path/with spaces/and-dashes/file_name.py"
        proxy = TTKodeViewerProxy(filename)
        assert proxy.fileName() == filename

    def test_multiple_viewer_proxies(self):
        """Test creating multiple viewer proxies."""
        filenames = [
            "/path/file1.py",
            "/path/file2.txt",
            "/path/file3.md"
        ]

        proxies = [TTKodeViewerProxy(fn) for fn in filenames]

        for proxy, filename in zip(proxies, filenames):
            assert proxy.fileName() == filename

    def test_viewer_proxy_filename_immutability(self):
        """Test that filename is set during initialization and retrieved correctly."""
        original_filename = "/original/path/file.py"
        proxy = TTKodeViewerProxy(original_filename)

        # Verify we can retrieve it
        assert proxy.fileName() == original_filename

        # Note: The proxy doesn't expose a setter, so filename should remain stable


# Note: TTKodeProxy requires a full TTKode instance which depends on the UI framework
# These tests would need a more complex setup with mocked UI components
# For now, we test the simpler TTKodeViewerProxy
# Integration tests for TTKodeProxy should be added when UI mocking infrastructure is available

class TestTTKodeProxyIntegration:
    """Integration tests for TTKodeProxy - these require more setup."""

    @pytest.mark.skip(reason="Requires full TTKode UI instance setup")
    def test_proxy_ttkode_reference(self):
        """Test that proxy maintains reference to TTKode instance."""
        # This would require setting up a full TTKode instance
        # which depends on the TTk UI framework
        pass

    @pytest.mark.skip(reason="Requires full TTKode UI instance setup")
    def test_proxy_open_file(self):
        """Test opening a file through the proxy."""
        # This would require a full TTKode instance
        pass

    @pytest.mark.skip(reason="Requires full TTKode UI instance setup")
    def test_proxy_iter_widgets(self):
        """Test iterating through widgets via proxy."""
        # This would require a full TTKode instance with widgets
        pass

    @pytest.mark.skip(reason="Requires full TTKode UI instance setup")
    def test_proxy_close_tab(self):
        """Test closing a tab through the proxy."""
        # This would require a full TTKode instance with tabs
        pass
