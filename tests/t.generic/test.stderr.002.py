import sys
import contextlib

class StderrHandler:
    def __init__(self, callback=None):
        """
        Create a handler for stderr output.

        Args:
            callback: A function that will be called with each piece of text written to stderr
        """
        self.buffer = ""
        self.callback = callback

    def write(self, text):
        self.buffer += text
        if self.callback:
            self.callback(text)
        return len(text)

    def flush(self):
        # Required to be a proper file-like object
        pass

    def getvalue(self):
        return self.buffer


@contextlib.contextmanager
def redirect_stderr_to_handler(callback=None):
    """Context manager for temporarily redirecting stderr to our handler."""
    handler = StderrHandler(callback)
    original_stderr = sys.stderr
    sys.stderr = handler
    try:
        yield handler
    finally:
        sys.stderr = original_stderr


# Example 1: Using the context manager
def my_handler(text):
    print(f"Captured stderr: {text!r}")

with redirect_stderr_to_handler(my_handler):
    # Any stderr output inside this block will be handled by my_handler
    print("This is an error", file=sys.stderr)
    raise Exception("This will also be captured")

# Example 2: Manual redirection
handler = StderrHandler(lambda text: print(f"Got: {text}"))
original_stderr = sys.stderr
sys.stderr = handler

try:
    # Now stderr is redirected
    print("Error message", file=sys.stderr)
finally:
    # Always restore the original stderr
    sys.stderr = original_stderr

# Get the accumulated output
print(f"Captured content: {handler.getvalue()}")