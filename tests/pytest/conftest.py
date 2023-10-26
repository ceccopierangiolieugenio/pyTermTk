# MIT License
#
# Copyright (c) 2022 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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
# SOFTWARE.import sys

# Thanks to: https://stackoverflow.com/questions/43162722/mocking-a-module-import-in-pytest

import sys

from mock_term  import Mock_TTkTerm
from mock_input import Mock_TTkInput

moduleTerm = type(sys)('TermTk.TTkCore.drivers.term_unix')
moduleTerm.TTkTerm = Mock_TTkTerm

moduleInput = type(sys)('TermTk.TTkCore.TTkTerm.input')
moduleInput.TTkInput = Mock_TTkInput

sys.modules['TermTk.TTkCore.drivers.term_unix']  = moduleTerm
sys.modules['TermTk.TTkCore.TTkTerm.input'] = moduleInput