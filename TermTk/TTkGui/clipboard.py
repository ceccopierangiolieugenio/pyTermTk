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
# SOFTWARE.

__all__ = ['TTkClipboard']

import importlib.util
from TermTk.TTkCore.log import TTkLog

class TTkClipboard():
    '''TTkClipboard

    :ref:`Clipboard`

    Example:

    .. code:: python

        from TermTk import TTkClipboard

        # Initialize the clipboard manager
        clipboard = TTkClipboard()

        # Push some text to the clipboard
        clipboard.setText("Example")

        # Get the text from the clipboard
        text = clipboard.text()


    '''
    _clipboard = ""
    _manager = None
    _setText = None
    _text = None

    def __init__(self) -> None:
        if not TTkClipboard._manager:
            TTkClipboard._loadClipboardManager()

    @staticmethod
    def _loadClipboardManager():
        try:
            if importlib.util.find_spec('pyodideProxy'):
                TTkLog.info("Using 'pyodideProxy' as clipboard manager")
                import pyodideProxy
                import asyncio
                async def _async_co():
                    text = await pyodideProxy.paste()
                    TTkLog.debug(f"ttkProxy paste_co: {text}")
                    return text
                def _paste():
                    loop = asyncio.get_event_loop()
                    text = loop.run_until_complete(_async_co())
                    # text = loop.run_until_complete(pyodideProxy.paste())
                    TTkLog.debug(f"ttkProxy paste: {text=} {_async_co()=}")
                    return text
                TTkClipboard._manager = pyodideProxy
                TTkClipboard._setText = pyodideProxy.copy
                TTkClipboard._text = pyodideProxy.paste # _paste
            elif importlib.util.find_spec('copykitten'):
                TTkLog.info("Using 'copykitten' as clipboard manager")
                import copykitten as _c
                TTkClipboard._manager = _c
                TTkClipboard._setText = _c.copy
                TTkClipboard._text = _c.paste
            elif importlib.util.find_spec('pyperclip'):
                TTkLog.info("Using 'pyperclip' as clipboard manager")
                import pyperclip as _c
                TTkClipboard._manager = _c
                TTkClipboard._setText = _c.copy
                TTkClipboard._text = _c.paste
            elif importlib.util.find_spec('pyperclip3'):
                TTkLog.info("Using 'pyperclip3' as clipboard manager")
                import pyperclip3 as _c
                TTkClipboard._manager = _c
                TTkClipboard._setText = _c.copy
                TTkClipboard._text = _c.paste
            elif importlib.util.find_spec('pyclip'):
                TTkLog.info("Using 'pyclip' as clipboard manager")
                import pyclip as _c
                TTkClipboard._manager = _c
                TTkClipboard._setText = _c.copy
                TTkClipboard._text = _c.paste
            elif importlib.util.find_spec('clipboard'):
                TTkLog.info("Using 'clipboard' as clipboard manager")
                import clipboard as _c
                TTkClipboard._manager = _c
                TTkClipboard._setText = _c.copy
                TTkClipboard._text = _c.paste
            else:
                TTkLog.info("No clipboard manager found")
                TTkClipboard._manager = "Not Found"
        except Exception as e:
           TTkLog.error("Clipboard error, try to export X11 if you are running this UI via SSH")
           for line in str(e).split("\n"):
               TTkLog.error(line)

    @staticmethod
    def setText(text):
        '''setText'''
        TTkClipboard._clipboard = text
        if TTkClipboard._setText:
            try:
                TTkClipboard._setText(str(text))
            except Exception as e:
                TTkLog.error("Clipboard error, try to export X11 if you are running this UI via SSH")
                for line in str(e).split("\n"):
                    TTkLog.error(str(line))

    @staticmethod
    def text():
        '''text'''
        if TTkClipboard._text:
            txt = None
            try:
                txt = TTkClipboard._text()
            except Exception as e:
                TTkLog.error("Clipboard error, try to export X11 if you are running this UI via SSH")
                for line in str(e).split("\n"):
                    TTkLog.error(line)
            if txt == None or txt == str(TTkClipboard._clipboard):
                return TTkClipboard._clipboard
            return txt
        return TTkClipboard._clipboard
