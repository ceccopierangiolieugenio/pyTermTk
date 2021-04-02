# [pyTermTk](https://github.com/ceccopierangiolieugenio/pyTermTk) - Hello World

## Intro
[TTkLayouts](https://ceccopierangiolieugenio.github.io/pyTermTk/TTkLayouts/index.html) are specialised classes that allow the placement of the widgets.
### [TTkLayout](https://ceccopierangiolieugenio.github.io/pyTermTk/TTkLayouts/layout.html#TermTk.TTkLayouts.layout.TTkLayout)
This is the base class for all the different layouts.
It allows free placement of the widgets in the layout area.
Used mainly to have free range moving [windows](https://ceccopierangiolieugenio.github.io/pyTermTk/TTkWidgets/window.html) because the widgets are not automatically replaced after a layout event
```text
TTkLayout
 ╔════════════════════════════╗
 ║   pos(4,2)                 ║
 ║   ┌───────┐   pos(16,4)    ║
 ║   │Widget1│   ┌─────────┐  ║
 ║   │       │   │ Widget2 │  ║
 ║   │       │   └─────────┘  ║
 ║   │       │                ║
 ║   └───────┘                ║
 ║                            ║
 ╚════════════════════════════╝
```

### [TTkHBoxLayout](https://ceccopierangiolieugenio.github.io/pyTermTk/TTkLayouts/boxlayout.html#TermTk.TTkLayouts.boxlayout.TTkHBoxLayout)
This layout allow an automatic place all the widgets horizontally
```text
TTkHBoxLayout
 ╔═════════╤═════════╤═════════╗
 ║ Widget1 │ Widget2 │ Widget3 ║
 ║         │         │         ║
 ║         │         │         ║
 ║         │         │         ║
 ║         │         │         ║
 ║         │         │         ║
 ╚═════════╧═════════╧═════════╝
```

### [TTkVBoxLayout](https://ceccopierangiolieugenio.github.io/pyTermTk/TTkLayouts/boxlayout.html#TermTk.TTkLayouts.boxlayout.TTkVBoxLayout)
This layout allow an automatic place all the widgets vertically
```text
TTkVBoxLayout
 ╔═════════════════════════════╗
 ║         Widget 1            ║
 ╟─────────────────────────────╢
 ║         Widget 2            ║
 ╟─────────────────────────────╢
 ║         Widget 3            ║
 ╟─────────────────────────────╢
 ║         Widget 4            ║
 ╚═════════════════════════════╝
```

### [TTkGridLayout](https://ceccopierangiolieugenio.github.io/pyTermTk/TTkLayouts/gridlayout.html#TermTk.TTkLayouts.gridlayout.TTkGridLayout)
This layout allow an automatic place all the widgets in a grid
the empty rows/cols are resized to the "columnMinHeight,columnMinWidth" parameters
```
TTkGridLayout        ┌┐ columnMinWidth
 ╔═════════╤═════════╤╤═════════╗
 ║ Widget1 │ Widget2 ││ Widget3 ║
 ║ (0,0)   │ (0,1)   ││ (0,3)   ║
 ╟─────────┼─────────┼┼─────────╢ ┐ columnMinHeight
 ╟─────────┼─────────┼┼─────────╢ ┘
 ║ Widget4 │         ││         ║
 ║ (2,0)   │         ││         ║
 ╟─────────┼─────────┼┼─────────╢
 ║         │         ││ Widget5 ║
 ║         │         ││ (3,3)   ║
 ╚═════════╧═════════╧╧═════════╝
```



## Example 1 - Simple [TTkLayout](https://ceccopierangiolieugenio.github.io/pyTermTk/TTkLayouts/layout.html#TermTk.TTkLayouts.layout.TTkLayout)
Following is the code to execute [VBox Example](layout/example1.simple.layout.py) in [pyTermTk](https://github.com/ceccopierangiolieugenio/pyTermTk)

```python
import TermTk as ttk

    # TTkLayout is used by default
root = ttk.TTk()

    # Attach 4 buttons to the root widget
ttk.TTkButton(parent=root, pos=(0,0),  size=(15,5), border=True, text="Button1")
ttk.TTkButton(parent=root, pos=(0,5),  size=(10,4), border=True, text="Button2")
ttk.TTkButton(parent=root, pos=(10,6), size=(10,3), border=True, text="Button3")
ttk.TTkButton(parent=root, pos=(13,1), size=(15,3), border=True, text="Button4")

root.mainloop()
```

The above code produces the following output
```text
┌─────────────┐
│            ┌─────────────┐
│   Button1  │   Button4   │
│            ╘═════════════╛
╘═════════════╛
┌────────┐
│Button2 │┌────────┐
│        ││Button3 │
╘════════╛╘════════╛

```

## Example 2 - Simple [TTkVBoxLayout](https://ceccopierangiolieugenio.github.io/pyTermTk/TTkLayouts/boxlayout.html#TermTk.TTkLayouts.boxlayout.TTkVBoxLayout)
Following is the code to execute [VBox Example](layout/example2.simple.vbox.py) in [pyTermTk](https://github.com/ceccopierangiolieugenio/pyTermTk)

```python
import TermTk as ttk

    # Set the VBoxLayout as defaut in the terminal widget
root = ttk.TTk(layout=ttk.TTkVBoxLayout())

    # Attach 4 buttons to the root widget
ttk.TTkButton(parent=root, border=True, text="Button1")
ttk.TTkButton(parent=root, border=True, text="Button2")
ttk.TTkButton(parent=root, border=True, text="Button3")
ttk.TTkButton(parent=root, border=True, text="Button4")

root.mainloop()
```

The above code produces the following output
```text
┌───────────────────────────────────────────────────────────┐
│                                                           │
│                          Button1                          │
│                                                           │
╘═══════════════════════════════════════════════════════════╛
┌───────────────────────────────────────────────────────────┐
│                                                           │
│                          Button2                          │
│                                                           │
╘═══════════════════════════════════════════════════════════╛
┌───────────────────────────────────────────────────────────┐
│                                                           │
│                          Button3                          │
│                                                           │
╘═══════════════════════════════════════════════════════════╛
┌───────────────────────────────────────────────────────────┐
│                                                           │
│                          Button4                          │
│                                                           │
╘═══════════════════════════════════════════════════════════╛
```

## Example 3 - Simple [TTkHBoxLayout](https://ceccopierangiolieugenio.github.io/pyTermTk/TTkLayouts/boxlayout.html#TermTk.TTkLayouts.boxlayout.TTkHBoxLayout)
Following is the code to execute [HBox Example](layout/example3.simple.hbox.py) in [pyTermTk](https://github.com/ceccopierangiolieugenio/pyTermTk)

```python
import TermTk as ttk

    # Set the HBoxLayout as defaut in the terminal widget
root = ttk.TTk()
root.setLayout(ttk.TTkHBoxLayout())

    # Attach 4 buttons to the root widget
ttk.TTkButton(parent=root, border=True, text="Button1")
ttk.TTkButton(parent=root, border=True, text="Button2")
ttk.TTkButton(parent=root, border=True, text="Button3")
ttk.TTkButton(parent=root, border=True, text="Button4")

root.mainloop()
```
The above code produces the following output
```text
┌─────────────┐┌─────────────┐┌─────────────┐┌──────────────┐
│             ││             ││             ││              │
│             ││             ││             ││              │
│             ││             ││             ││              │
│             ││             ││             ││              │
│             ││             ││             ││              │
│             ││             ││             ││              │
│             ││             ││             ││              │
│             ││             ││             ││              │
│   Button1   ││   Button2   ││   Button3   ││   Button4    │
│             ││             ││             ││              │
│             ││             ││             ││              │
│             ││             ││             ││              │
│             ││             ││             ││              │
│             ││             ││             ││              │
│             ││             ││             ││              │
│             ││             ││             ││              │
│             ││             ││             ││              │
│             ││             ││             ││              │
╘═════════════╛╘═════════════╛╘═════════════╛╘══════════════╛

```

## Example 4 - Simple [TTkGridLayout](https://ceccopierangiolieugenio.github.io/pyTermTk/TTkLayouts/gridlayout.html#TermTk.TTkLayouts.gridlayout.TTkGridLayout)
Following is the code to execute [HBox Example](layout/example4.simple.grid.py) in [pyTermTk](https://github.com/ceccopierangiolieugenio/pyTermTk)

```python
import TermTk as ttk

    # Set the GridLayout as defaut in the terminal widget
gridLayout = ttk.TTkGridLayout(columnMinHeight=0,columnMinWidth=2)
root = ttk.TTk(layout=gridLayout)

    # Attach 2 buttons to the root widget using the default method
    # this will append them to the first row
ttk.TTkButton(parent=root, border=True, text="Button1")
ttk.TTkButton(parent=root, border=True, text="Button2")
    # Attach 2 buttons to a specific position in the grid
gridLayout.addWidget(ttk.TTkButton(parent=root, border=True, text="Button3"), 1,2)
gridLayout.addWidget(ttk.TTkButton(parent=root, border=True, text="Button4"), 3,4)

root.mainloop()
```
The above code produces the following output
```text
┌───────────┐┌───────────┐
│           ││           │
│  Button1  ││  Button2  │
│           ││           │
╘═══════════╛╘═══════════╛
                          ┌───────────┐
                          │           │
                          │  Button3  │
                          │           │
                          ╘═══════════╛
                                         ┌───────────┐
                                         │           │
                                         │  Button4  │
                                         │           │
                                         ╘═══════════╛
```

## Example 5 - Nested Layouts
Following is the code to execute [Nested Layouts Example](layout/example5.nested.layouts.py) in [pyTermTk](https://github.com/ceccopierangiolieugenio/pyTermTk)

```python
import TermTk as ttk

    # Set the GridLayout as defaut in the terminal widget
root = ttk.TTk()

gridLayout = ttk.TTkGridLayout()
root.setLayout(gridLayout)

    # Attach 2 buttons to the root widget using the default method
    # this will append them to the first row
    # NOTE: it is not recommended to use this legacy method in a gridLayout
ttk.TTkButton(parent=root, border=True, text="Button1")
ttk.TTkButton(parent=root, border=True, text="Button2")
    # Attach 2 buttons to a specific position in the grid
gridLayout.addWidget(ttk.TTkButton(border=True, text="Button3"), 1,2)
gridLayout.addWidget(ttk.TTkButton(border=True, text="Button4"), 2,4)

    # Create a VBoxLayout and add it to the gridLayout
vboxLayout = ttk.TTkVBoxLayout()
gridLayout.addItem(vboxLayout,1,3)
    # Attach 2 buttons to the vBoxLayout
vboxLayout.addWidget(ttk.TTkButton(border=True, text="Button5"))
vboxLayout.addWidget(ttk.TTkButton(border=True, text="Button6"))

root.mainloop()
```
The above code produces the following output
```text
┌─────────┐┌─────────┐
│         ││         │
│ Button1 ││ Button2 │
│         ││         │
╘═════════╛╘═════════╛
                      ┌─────────┐┌─────────┐
                      │         ││ Button5 │
                      │ Button3 │╘═════════╛
                      │         │┌─────────┐
                      │         ││ Button6 │
                      ╘═════════╛╘═════════╛
                                            ┌─────────┐
                                            │         │
                                            │ Button4 │
                                            │         │
                                            ╘═════════╛
```


## Example 6 - Rowspan/Colspan in Grid Layout
Following is the code to execute [Nested Layouts Example](layout/example6.grid.span.py) in [pyTermTk](https://github.com/ceccopierangiolieugenio/pyTermTk)

```python
import TermTk as ttk

root = ttk.TTk()

gridLayout = ttk.TTkGridLayout()
root.setLayout(gridLayout)

# | x = 0   | x = 1 | x = 2   |
# |         |       |         |
# ┌────────────────┐┌─────────┐ ──────
# │y=0 x=0 h=1 w=2 ││y=0 x=2  │  y = 0
# │    Button1     ││h=2 w=1  │
# ╘════════════════╛│         │ ──────
# ┌─────────┐       │ Button2 │  y = 1
# │y=1 x=0  │       ╘═════════╛
# │h=2 w=1  │┌────────────────┐ ──────
# │         ││y=2 x=1 h=1 w=2 |  y = 2
# │ Button3 ││    Button4     │
# ╘═════════╛╘════════════════╛ ──────

gridLayout.addWidget(ttk.TTkButton(border=True, text="Button1"), 0,0, 1,2)
gridLayout.addWidget(ttk.TTkButton(border=True, text="Button2"), 0,2, 2,1)
gridLayout.addWidget(ttk.TTkButton(border=True, text="Button3"), 1,0, 2,1)
gridLayout.addWidget(ttk.TTkButton(border=True, text="Button4"), 2,1, 1,2)

root.mainloop()
```
The above code produces the following output
```text
┌───────────────────────┐┌───────────┐
│                       ││           │
│        Button1        ││           │
│                       ││           │
╘═══════════════════════╛│  Button2  │
┌───────────┐            │           │
│           │            │           │
│           │            │           │
│           │            ╘═══════════╛
│  Button3  │┌───────────────────────┐
│           ││                       │
│           ││        Button4        │
│           ││                       │
╘═══════════╛╘═══════════════════════╛
```
