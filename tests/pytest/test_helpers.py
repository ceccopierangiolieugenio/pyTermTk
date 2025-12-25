# MIT License
#
# Copyright (c) 2025 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

"""
Helper utilities for pyTermTk tests.
"""

from typing import Any, List, Tuple


class MockSlot:
    """
    A mock slot for testing signal-slot connections.

    Tracks all calls and allows querying call count and arguments.

    Example:
        ms = mock_slot(int, str)
        widget.someSignal.connect(ms)

        # Trigger signal
        widget.doSomething()

        # Check calls
        assert ms.called() == 1
        assert ms.arg(0) == 123
        assert ms.arg(1) == "test"
        assert ms.args() == [(123, "test")]
    """

    def __init__(self, *arg_types):
        """
        Initialize mock slot with expected argument types.

        :param arg_types: Expected types for the signal arguments (for documentation only)
        :type arg_types: type
        """
        self._arg_types = arg_types
        self._calls: List[Tuple[Any, ...]] = []

    def __call__(self, *args):
        """
        Called when the signal is emitted.

        :param args: Arguments passed by the signal
        """
        self._calls.append(args)

    def called(self) -> int:
        """
        Get the number of times this slot was called.

        :return: Number of calls
        :rtype: int
        """
        return len(self._calls)

    def arg(self, index: int, call_index: int = -1) -> Any:
        """
        Get a specific argument from a specific call.

        :param index: Index of the argument (0-based)
        :type index: int
        :param call_index: Index of the call (-1 for last call)
        :type call_index: int
        :return: The argument value
        :rtype: Any
        :raises IndexError: If call_index or index is out of range
        """
        if not self._calls:
            raise IndexError("No calls recorded")
        return self._calls[call_index][index]

    def args(self, call_index: int = -1) -> Tuple[Any, ...]:
        """
        Get all arguments from a specific call.

        :param call_index: Index of the call (-1 for last call)
        :type call_index: int
        :return: Tuple of all arguments from that call
        :rtype: tuple
        :raises IndexError: If call_index is out of range
        """
        if not self._calls:
            raise IndexError("No calls recorded")
        return self._calls[call_index]

    def all_args(self) -> List[Tuple[Any, ...]]:
        """
        Get all arguments from all calls.

        :return: List of tuples, each containing arguments from one call
        :rtype: list[tuple]
        """
        return self._calls.copy()

    def reset(self):
        """
        Reset the call history.
        """
        self._calls.clear()

    def assert_called(self, times: int = None):
        """
        Assert that the slot was called a specific number of times.

        :param times: Expected number of calls (None = at least once)
        :type times: int, optional
        :raises AssertionError: If assertion fails
        """
        if times is None:
            assert self._calls, "Expected at least one call, but slot was never called"
        else:
            assert len(self._calls) == times, f"Expected {times} calls, but got {len(self._calls)}"

    def assert_not_called(self):
        """
        Assert that the slot was never called.

        :raises AssertionError: If slot was called
        """
        assert not self._calls, f"Expected no calls, but got {len(self._calls)}"

    def assert_called_with(self, *args, call_index: int = -1):
        """
        Assert that a specific call was made with specific arguments.

        :param args: Expected arguments
        :param call_index: Index of the call to check (-1 for last call)
        :type call_index: int
        :raises AssertionError: If arguments don't match
        """
        if not self._calls:
            raise AssertionError("Expected call with arguments, but slot was never called")
        actual = self._calls[call_index]
        assert actual == args, f"Expected call with {args}, but got {actual}"

    def assert_any_call(self, *args):
        """
        Assert that at least one call was made with specific arguments.

        :param args: Expected arguments
        :raises AssertionError: If no matching call found
        """
        assert args in self._calls, f"Expected at least one call with {args}, but not found in {self._calls}"


