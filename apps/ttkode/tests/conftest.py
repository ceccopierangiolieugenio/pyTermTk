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

import sys
import os
import pytest

# Add the library path for pyTermTk
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../libs/pyTermTk'))

# Add the ttkode package path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Reuse the pytest mocks used by the core test suite
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../tests/pytest'))

from mock_term import Mock_TTkTerm
from mock_input import Mock_TTkInput

moduleTerm = type(sys)('TermTk.TTkCore.drivers.term_unix_common')
moduleTerm._TTkTerm = Mock_TTkTerm

moduleInput = type(sys)('TermTk.TTkCore.TTkTerm.input')
moduleInput.TTkInput = Mock_TTkInput

sys.modules['TermTk.TTkCore.drivers.term_unix_common'] = moduleTerm
sys.modules['TermTk.TTkCore.TTkTerm.input'] = moduleInput

@pytest.fixture(autouse=True)
def reset_plugin_instances():
    """Reset plugin instances before each test to avoid state leakage."""
    from ttkode.plugin import TTkodePlugin
    original_instances = TTkodePlugin.instances.copy()
    yield
    TTkodePlugin.instances.clear()
    TTkodePlugin.instances.extend(original_instances)
