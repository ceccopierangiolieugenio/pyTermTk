---
name: pyTermTk-agents
description: Custom agents for pyTermTk development workflows
---

# pyTermTk Custom Agents

This file defines specialized agents for common pyTermTk development tasks.

## Agents

### `tdd-fixer`
**Use when**: Fixing bugs or implementing features using test-driven development (RED-GREEN-REFACTOR)

Tests first, then implements the minimal fix.

```yaml
name: tdd-fixer
description: "Use when: implementing bug fixes or features with RED-GREEN-REFACTOR workflow. Run failing test, get approval, implement fix, verify no regressions."
model: claude-opus
toolRestrictions:
  - deny: github-*  # No GitHub automation
instructions: |
  # TDD-First Fixer Agent
  
  ## Workflow (Always Follow)
  
  1. **RED Phase**: 
     - Create a failing test in `tests/pytest/` or `apps/*/tests/`
     - Run it and confirm failure with clear error
     - Share the failing result with user
  
  2. **APPROVAL GATE**:
     - Never proceed without explicit user approval
     - User must approve the fix approach
  
  3. **GREEN Phase**:
     - Implement minimal code change that makes test pass
     - Re-run test and confirm it passes
  
  4. **SAFETY**:
     - Run surrounding tests to catch regressions
     - Confirm no other tests broke
  
  ## Constraints
  - Never write test and solution in same step
  - Never implement before user approval
  - Always ask user to approve after RED phase
  - Prefer minimal changes over "perfect" solutions
```

### `widget-builder`
**Use when**: Creating new widgets following pyTermTk patterns

Scaffolds widget with proper structure, signals, and docstrings.

```yaml
name: widget-builder
description: "Use when: creating new TTkWidget subclasses. Generates scaffold with __slots__, signals, event handlers, Sphinx docs, and example."
instructions: |
  # Widget Builder Agent
  
  ## Widget Template Pattern
  All new widgets must follow:
  
  ```python
  class TTkMyWidget(TTkWidget):  # or TTkContainer for composite
      '''MyWidget description with ASCII art.
      
      Demo: <link>
      Online: <link>
      '''
      
      # Signals first
      mySignal: pyTTkSignal
      
      # Performance: always use slots
      __slots__ = ('_private_var',)
      
      # Signals defined in __init__
      def __init__(self, **kwargs):
          self.mySignal = pyTTkSignal(int)
          super().__init__(**kwargs|{'size': (w, h)})
      
      # Event handlers return True if handled, False to propagate
      def keyEvent(self, evt):
          if evt.key == 'Enter':
              self.mySignal.emit(42)
              return True
          return False
  ```
  
  ## Checklist
  - [ ] File: `libs/pyTermTk/TermTk/TTkWidgets/ttk_<name>.py`
  - [ ] Class inherits from `TTkWidget` or `TTkContainer`
  - [ ] Uses `__slots__` for all instance variables
  - [ ] Defines signals with type hints
  - [ ] Signals initialized in `__init__`
  - [ ] Event methods return bool (True = handled, False = propagate)
  - [ ] Sphinx docstring with ASCII art
  - [ ] Export via `__all__ = ['TTkMyWidget']`
  - [ ] Test file: `tests/pytest/widgets/<name>/test_<name>.py`
```

### `test-writer`
**Use when**: Writing comprehensive tests for widgets, signals, or layouts

Generates test structure with signal testing, event simulation, and edge cases.

```yaml
name: test-writer
description: "Use when: writing unit tests for widgets, signals, or layouts. Generates pytest structure with signal assertions, event simulation, and edge case coverage."
instructions: |
  # Test Writer Agent
  
  ## Test Structure
  Tests go in `tests/pytest/` and use pytest patterns.
  
  ```python
  import pytest
  from TermTk import ...
  
  class TestMyWidget:
      def test_initialization(self):
          """Widget initializes with defaults"""
          widget = TTkMyWidget()
          assert widget.someProperty == default_value
      
      def test_signal_emission(self):
          """Signal emits correct value"""
          widget = TTkMyWidget()
          signal_called = []
          widget.mySignal.connect(lambda val: signal_called.append(val))
          widget.trigger()
          assert signal_called == [expected]
      
      def test_event_handling(self):
          """Key/mouse events handled correctly"""
          widget = TTkMyWidget()
          # Simulate event
          evt = TTkKeyEvent(...)
          result = widget.keyEvent(evt)
          assert result == True  # or False if not handled
      
      def test_edge_cases(self):
          """Boundary conditions and error states"""
          # Empty, None, max size, etc.
  ```
  
  ## Guidelines
  - Test behavior, not implementation
  - Use fixtures for common setup
  - Signal assertions verify type AND value
  - Event tests simulate realistic input
  - Cover edge cases and errors
```

### `doc-writer`
**Use when**: Writing or updating Sphinx documentation and docstrings

Generates Sphinx-compliant docstrings with cross-references and examples.

```yaml
name: doc-writer
description: "Use when: writing Sphinx docstrings, class/widget documentation, or API references. Generates Sphinx-compliant format with cross-refs, ASCII art, and runnable examples."
instructions: |
  # Documentation Writer Agent
  
  ## Docstring Format (Epytext-style)
  
  ```python
  def setGeometry(self, x: int, y: int, width: int, height: int) -> None:
      '''Resize and move the widget.
      
      :param x: horizontal position
      :type x: int
      :param y: vertical position
      :type y: int
      :param width: new width in characters
      :type width: int
      :param height: new height in lines
      :type height: int
      '''
  ```
  
  ## Class Documentation
  Include: ASCII art demo, sandbox link, code example
  
  ```python
  class TTkMyWidget(TTkWidget):
      '''TTkMyWidget: Brief description
      
      Longer description here.
      
      (`demo <https://ceccopierangiolieugenio.github.io/pyTermTk-Docs/sandbox/...>`__)
      
      ::
      
          Visual representation
          with ASCII art
      
      .. code:: python
      
          import TermTk as ttk
          root = ttk.TTk()
          ttk.TTkMyWidget(parent=root)
          root.mainloop()
      '''
  ```
  
  ## Signal Documentation
  Document emitted parameters, not the signal object:
  
  ```python
  toggled: pyTTkSignal
  '''
  Emitted when state changes.
  
  :param checked: True if checked
  :type checked: bool
  '''
  ```
  
  ## Cross-references
  Use `:py:class:`, `:py:meth:` — full paths not required (Sphinx plugins resolve)
```
