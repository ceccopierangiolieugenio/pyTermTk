---
name: widget-creation
description: "Use when: creating new TTkWidget subclasses with proper structure, signals, slots, and documentation"
---

# Widget Creation Skill

## Overview
This skill scaffolds new pyTermTk widgets following project patterns:
- Proper class structure with `__slots__`
- Signal definitions with type hints
- Event handlers with correct return semantics
- Sphinx documentation with ASCII art
- Test file structure
- Example/demo integration

## When to Use
- Building new interactive widgets (button, input, selector variants)
- Creating container widgets (custom layouts, panels)
- Adding display widgets (custom text renderers, charts)

## File Structure

### 1. Widget File
Location: `libs/pyTermTk/TermTk/TTkWidgets/ttk_<widget_name>.py`

Template:
```python
"""
Module: TTkMyWidget
Implements a custom widget for [purpose]
"""

from TermTk import TTkWidget, TTkColor, pyTTkSignal, pyTTkSlot

class TTkMyWidget(TTkWidget):
    '''TTkMyWidget: [One-line description]

    [Longer description of purpose and behavior]

    (`demo <https://ceccopierangiolieugenio.github.io/pyTermTk-Docs/sandbox/...>`__)

    ::

        [ASCII art showing visual representation]
        [Multiple lines if needed]

    .. code:: python

        import TermTk as ttk

        root = ttk.TTk()
        widget = ttk.TTkMyWidget(parent=root)
        root.mainloop()
    '''

    # Performance: always use __slots__
    __slots__ = (
        '_privateVar',
        '_anotherVar',
        'stateChanged',
    )

    _privateVar: int
    _anotherVar: int
    stateChanged: pyTTkSignal
    '''
    Emitted when widget state changes.

    :param value: new state value
    :type value: [type]
    '''

    # Class-level styling
    classStyle = {
        'default':  {'color': TTkColor.fg("#dddd88"), 'borderColor': TTkColor.RST},
        'hover':    {'color': TTkColor.fg("#ffffff"), 'borderColor': TTkColor.BOLD},
        'focus':    {'borderColor': TTkColor.fg("#ffff00")},
        'disabled': {'color': TTkColor.fg('#888888')}
    }

    def __init__(self, **kwargs):
        '''Initialize the widget.

        :param parent: parent widget
        :type parent: TTkWidget
        [Other parameters as needed]
        '''
        # Instantiate signals in __init__ (do not instantiate at class level)
        self.stateChanged = pyTTkSignal(int)

        # Initialize private variables
        self._privateVar = 0  # Replace with appropriate default for your widget

        # Call parent with merged kwargs and default size
        super().__init__(**kwargs|{'size': (10, 3)})  # Replace with appropriate default dimensions

    # Property getters/setters
    def getValue(self) -> int:
        '''Get the current value.

        :return: current value
        :rtype: int
        '''
        return self._privateVar

    def setValue(self, value: int) -> None:
        '''Set the value.

        :param value: new value
        :type value: int
        '''
        if self._privateVar != value:
            self._privateVar = value
            self.stateChanged.emit(value)
            self.update()

    # Return True when this widget fully processes the event; otherwise return False to let parent widgets handle it.
    def keyEvent(self, evt) -> bool:
        '''Handle keyboard events.'''
        if evt.key == 'Enter':
            self.stateChanged.emit(self._privateVar)
            return True
        return False

    def mousePressEvent(self, evt) -> bool:
        '''Handle mouse press events.'''
        # Handle click, return True if consumed
        return False

    def paintEvent(self) -> None:
        '''Render the widget.'''
        # Use currentStyle() for theme-aware colors
        canvas = self.canvas
        style = self.currentStyle()

        # Draw widget content
        canvas.drawText(pos=(0, 0), text="MyWidget")

__all__ = ['TTkMyWidget']
```

### 2. Test File
Location: `tests/pytest/widgets/<widget_name>/test_<widget_name>.py`

Template:
```python
import pytest
from TermTk import TTkMyWidget

class TestTTkMyWidget:
    '''Test suite for TTkMyWidget'''

    def test_initialization(self):
        """Widget initializes with defaults"""
        widget = TTkMyWidget()
        assert widget.getValue() == 0  # Or expected default

    def test_signal_emission(self):
        """Signal emits when state changes"""
        widget = TTkMyWidget()
        emitted = []
        widget.stateChanged.connect(lambda val: emitted.append(val))

        widget.setValue(42)
        assert emitted == [42]

    def test_key_event_handling(self):
        """Key events handled correctly"""
        widget = TTkMyWidget()
        from TermTk import TTkKeyEvent

        evt = TTkKeyEvent(key='Enter')
        result = widget.keyEvent(evt)
        assert result == True  # Event was handled

    def test_disabled_state(self):
        """Widget respects disabled state"""
        widget = TTkMyWidget()
        widget.setDisabled(True)
        # Verify widget doesn't respond to events, etc.
```

### 3. Example/Demo
Add to `demo/showcase/` or `tutorial/examples/` if creating showcase:

```python
"""
Example: TTkMyWidget

Demonstrates the TTkMyWidget in action.
"""

import TermTk as ttk

def main():
    root = ttk.TTk()

    # Create and configure widget
    widget = ttk.TTkMyWidget(parent=root)
    widget.setValue(10)

    # Connect signal
    @ttk.pyTTkSlot(int)
    def on_state_changed(value):
        print(f"State changed to: {value}")

    widget.stateChanged.connect(on_state_changed)

    root.mainloop()

if __name__ == '__main__':
    main()
```

## Key Patterns to Follow

### Signals
- Keep signal entries in `__slots__` and type-annotate them there
- Instantiate signals in `__init__` with specific type: `pyTTkSignal(int)` not `pyTTkSignal()`
- Emit with actual value: `self.stateChanged.emit(value)`

### __slots__
```python
__slots__ = (
    '_variable1',
    '_variable2',
    'valueChanged',
    # Always use slots for memory efficiency
)

_variable1: int
_variable2: int
valueChanged: pyTTkSignal
```

Rules:
- All non-signal slot names must start with `_`.
- Public (non-underscore) slot names are allowed only for exposed signals.
- Add a class-level type annotation for each slot entry immediately below `__slots__`.

### Class Styling
```python
classStyle = {
    'default':  {...},
    'hover':    {...},
    'focus':    {...},
    'disabled': {...}
}
```

### Event Return Values
- Return `True` if event fully handled (don't propagate)
- Return `False` to let event propagate up widget tree

### Documentation
- ASCII art for visual widgets
- Demo/sandbox links
- Runnable code examples
- Sphinx cross-references: `:py:class:`, `:py:meth:`

## Checklist

### File and Class Structure
- [ ] File location: `libs/pyTermTk/TermTk/TTkWidgets/ttk_*.py`
- [ ] Inherits from `TTkWidget` or `TTkContainer`
- [ ] `__slots__` defined
- [ ] Non-signal slot names use leading `_`
- [ ] Public slot names are signals only
- [ ] Every slot entry has a class-level type annotation
- [ ] `__all__` export defined
- [ ] Register the widget export in `libs/pyTermTk/TermTk/TTkWidgets/__init__.py` with `from .ttk_<widget_name> import TTkMyWidget`

### Signals and Events
- [ ] Signals with type hints
- [ ] Signals initialized in `__init__`
- [ ] Event methods return bool

### Documentation and Examples
- [ ] Sphinx docstring with ASCII art
- [ ] Example added to demo or tutorial

### Testing and Quality
- [ ] Test file created
- [ ] Tests cover initialization, signals, events, edge cases
- [ ] Flake8 passes

## Common Mistakes to Avoid
- ❌ Signals instantiated at class level instead of `__init__`
- ❌ Event handlers don't return bool (should always return True/False)
- ❌ Missing `__slots__` (memory waste)
- ❌ Hardcoded colors instead of using theme via `currentStyle()`
- ❌ Tests that only check implementation, not behavior
- ❌ No documentation or examples
