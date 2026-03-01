import TermTk as ttk

class TTkode_Terminal(ttk.TTkTerminal):
    __slots__ = ('_isRunning')
    def __init__(self, **kwargs):
        self._isRunning = False
        super().__init__(**kwargs)

    def show(self):
        if not self._isRunning:
            self._isRunning = True
            _th = ttk.TTkTerminalHelper(term=self)
            _th.runShell()
        return super().show()