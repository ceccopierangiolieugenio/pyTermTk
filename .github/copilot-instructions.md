# pyTermTk Copilot Instructions

## Project Overview

pyTermTk is a Text-based User Interface (TUI) library for Python inspired by Qt5, GTK, and tkinter APIs. It creates cross-platform terminal applications with rich widgets, layouts, and an event-driven architecture.

## Architecture

### Core Structure
- **`libs/pyTermTk/TermTk/`** - Main library code organized into logical modules:
  - `TTkCore/` - Core functionality (signals, colors, canvas, configuration)
  - `TTkWidgets/` - All UI widgets inherit from `TTkWidget` base class
  - `TTkLayouts/` - Layout managers (GridLayout, HBoxLayout, VBoxLayout)
  - `TTkGui/` - GUI components (drag & drop, application management)
  - `TTkTemplates/` - Mixin classes for event handling (`TKeyEvents`, `TMouseEvents`, `TDragEvents`)

### Widget Inheritance Pattern
All widgets follow this pattern:
```python
class TTkMyWidget(TTkWidget):  # Or TTkContainer for composite widgets
    # Class-level styling
    classStyle = {
        'default':  {'color': TTkColor.fg("#dddd88"), 'borderColor': TTkColor.RST},
        'hover':    {'color': TTkColor.fg("#ffffff"), 'borderColor': TTkColor.BOLD},
        'focus':    {'borderColor': TTkColor.fg("#ffff00")},
        'disabled': {'color': TTkColor.fg('#888888')}
    }

    # Signal declarations
    mySignal: pyTTkSignal

    __slots__ = ('_private_vars',)  # Always use slots for performance

    def __init__(self, **kwargs):
        self.mySignal = pyTTkSignal(int)  # Define signals in __init__
        super().__init__(**kwargs|{'size': (w, h)})  # Merge kwargs, set default size
```

### Signal-Slot System (Qt-inspired)
Use type-safe signal-slot patterns:
```python
# Define signals with types
signal = pyTTkSignal(int)
# Define slots with decorators
@pyTTkSlot(int)
def my_slot(value: int):
    pass
# Connect them
signal.connect(my_slot)
```

### Event Handling
Widgets handle events by overriding template methods:
- `keyEvent()`, `mousePressEvent()`, `paintEvent()` - Core events
- `focusInEvent()`, `focusOutEvent()` - Focus management
- `dropEvent()`, `dragEnterEvent()` - Drag & drop
- Always return `True` if event is handled, `False` to propagate

## Development Workflows

### Testing
- **Unit tests**: `pytest tests/pytest/` (run via Makefile: `make test`)
- **Performance tests**: `tests/timeit/` - Contains signal/slot benchmarks and optimization tests
- **Manual tests**: `tests/t.*/` - Interactive UI tests
- **CI**: Tests run on Python 3.9-3.14 with flake8 linting

### Build & Deploy
- **Local build**: `pip install -e libs/pyTermTk` (uses `pip`)
- **Documentation**: `make doc` (Sphinx-based, outputs to `docs/source/_build/html/`)
- **Apps deployment**: Individual apps in `apps/` have their own `pyproject.toml`

### Running Examples
- **Demo**: `python demo/demo.py -f`
- **Designer**: `pip install -e apps/ttkDesigner ; ttkDesigner`
- **Individual tests**: `python tests/t.ui/test.ui.036.datetime.01.py`

## Project-Specific Patterns

### Widget State Management
Many widgets use internal state classes (see `datetime_date_form.py`):
```python
class _TTkWidgetState:
    __slots__ = ('_data', 'signal_name')
    def __init__(self):
        self.signal_name = pyTTkSignal()
```

### File Organization
- One widget per file in `TTkWidgets/`
- Use `__all__ = ['ClassName']` exports
- Import from `TermTk.TTkCore`, `TermTk.TTkWidgets` etc (not relative imports)
- Apps in `apps/` are self-contained with `pyproject.toml`

### Color & Theming
Use `TTkColor` constants and theme system:
```python
TTkColor.fg("#ffffff") + TTkColor.bg("#000044") + TTkColor.BOLD
style = self.currentStyle()  # Get theme-aware colors
```

### Cross-Platform Considerations
- Platform-specific code in `TTkCore/drivers/`
- Terminal compatibility testing in `tests/ansi.images.json`
- HTML5 export capabilities via `tools/webExporter/`

### Documentation & Docstrings
Use **Sphinx-compatible docstring format** with Epytext-style field lists:
```python
# In any sphinx reference
# i.e. ':py:class:' or ':py:meth:'
# the full path is not required but just che class name,
# the link will be resolved in one of the sphynx custom plugins.
def ttkStringData(self, row:int, col:int) -> TTkString:
    '''
    Returns the :py:class:`TTkString` reprsents the data stored in the row/column.

    :param row: the row position of the data
    :type row: int
    :param col: the column position of the data
    :type col: int

    :return: the formatted string
    :rtype: :py:class:`TTkString`
    '''
    data = self.data(row,col)
    return TTkAbstractTableModel._dataToTTkString(data)

def setGeometry(self, x: int, y: int, width: int, height: int):
    ''' Resize and move the widget

    :param x: the horizontal position
    :type x: int
    :param y: the vertical position
    :type y: int
    :param width: the new width
    :type width: int
    :param height: the new height
    :type height: int
    '''

# For class/module docstrings include ASCII art examples,
# a link to the demo and the sandbox link if available:
# A small code example if not too complex
class TTkDate(TTkWidget):
    ''' TTkDate:

    A widget for displaying and editing dates. (`demo <https://ceccopierangiolieugenio.github.io/pyTermTk-Docs/sandbox/sandbox.html?filePath=demo/showcase/date_time.py>`__)

    ::

        2025/11/04 📅

    .. code:: python

        import TermTk as ttk

        root = ttk.TTk(mouseTrack=True)

        ttk.TTkDate(parent=root) # Defaults to the current date

        root.mainloop()

    '''

class TTkAppTemplate(TTkContainer):
    ''' TTkAppTemplate:

    A flexible application template layout with multiple resizable panels.

    ::

        App Template Layout
        ┌─────────────────────────────────┐
        │         Header                  │
        ├─────────┬──────────────┬────────┤ H
        │         │   Top        │        │
        │         ├──────────────┤        │ T
        │         │              │        │
        │  Right  │   Main       │  Left  │
        │         │   Center     │        │
        │         │              │        │
        │         ├──────────────┤        │ B
        │         │   Bottom     │        │
        ├─────────┴──────────────┴────────┤ F
        │         Footer                  │
        └─────────────────────────────────┘
                  R              L

    Demo: `apptemplate.py <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/demo/showcase/apptemplate.py>`_
    `online <https://ceccopierangiolieugenio.github.io/pyTermTk-Docs/sandbox/sandbox.html?filePath=showcase/apptemplate.py>`_
    '''

# For signals, document parameters:
toggled:pyTTkSignal
'''
This signal is emitted whenever the button state changes if checkeable,
i.e., whenever the user checks or unchecks it.

:param checked: True if checked otherwise False
:type checked: bool
'''
```

**Key conventions**:
- Use single quotes `'''` for docstrings
- Include ASCII art for visual widgets showing borders/layout
- Link to demo files with full GitHub URLs
- Use `:py:class:` for cross-references to other classes
- Document all parameters with `:param name:` and `:type name:`
- Include `:return:` and `:rtype:` for non-void methods
- Signal docstrings document emitted parameters, not the signal itself

## Apps Ecosystem
The project includes several full applications demonstrating patterns:
- **ttkDesigner** - Visual UI designer (like Qt Designer)
- **ttkode** - Code editor with syntax highlighting
- **dumbPaintTool** - ASCII art editor
- **tlogg** - Log file viewer

### Testing App Integration
Apps use the main library via path manipulation:
```python
sys.path.append(os.path.join(sys.path[0],'../../libs/pyTermTk'))
import TermTk as ttk
```

## Key Integration Points

### Layout System
Use Qt-like layout managers:
```python
layout = TTkGridLayout()
layout.addWidget(widget, row, col, rowspan, colspan)
container.setLayout(layout)
```

### Focus & Input Handling
Set focus policy and handle keyboard navigation:
```python
self.setFocusPolicy(TTkK.ClickFocus | TTkK.TabFocus)
```

When implementing new widgets, study existing patterns in `TTkWidgets/` and ensure signal-slot integration follows the established type-safe patterns shown in `tests/pytest/test_004_signals_slots.py`.