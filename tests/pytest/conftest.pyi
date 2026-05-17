"""Type stub for conftest.py fixtures."""

from typing import Callable
import TermTk as ttk

class _FakeCanvas(ttk.TTkCanvas):
    def text_in_line(self, line: int, text: str) -> bool: ...

def fake_canvas() -> Callable[[int, int], _FakeCanvas]: ...
