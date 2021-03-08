# [pyTermTk](https://github.com/ceccopierangiolieugenio/pyTermTk) - Hello World

## Intro
 - Creating a simple GUI application using [pyTermTk](https://github.com/ceccopierangiolieugenio/pyTermTk) involves the following steps −
 - Import TermTk package.
 - Create an [TTk](https://ceccopierangiolieugenio.github.io/pyTermTk/TTkCore/ttk.html) object.
 - Add a [TTkLabel](https://ceccopierangiolieugenio.github.io/pyTermTk/TTkWidgets/label.html) object in it with the caption "**hello world**" in the position (x=5,y=2).
 - Enter the mainloop of application by [mainloop()](https://ceccopierangiolieugenio.github.io/pyTermTk/TTkCore/ttk.html#TermTk.TTkCore.ttk.TTk.mainloop) method.

## Example 1
Following is the code to execute [Hello World program](helloworld/helloworld.001.py) in [pyTermTk](https://github.com/ceccopierangiolieugenio/pyTermTk) −

```python
import sys, os
import TermTk as ttk

root = ttk.TTk()
ttk.TTkLabel(parent=root, pos=(5,2), text="Hello World")
root.mainloop()
```

The above code produces the following output (yuhuuuuu!!!)−
```text


     Hello World


```

## Example 2 - Your first Window
Following is the code to execute [Hello World program](helloworld/helloworld.002.py) in [pyTermTk](https://github.com/ceccopierangiolieugenio/pyTermTk) −

```python
import sys, os
import TermTk as ttk

# Create a root object (it is a widget that represent the terminal)
root = ttk.TTk()
# Create a window and attach it to the root (parent=root)
helloWin = ttk.TTkWindow(parent=root,pos = (1,1), size=(30,10), title="Hello Window", border=True)
# Define the Label and attach it to the window (parent=helloWin)
ttk.TTkLabel(parent=helloWin, pos=(5,5), text="Hello World")
# Start the Main loop
root.mainloop()
```

The above code produces the following output (yuhuuuuu!!!)−
```text

 ╔════════════════════════════╗
 ║ Hello Window               ║
 ╟────────────────────────────╢
 ║                            ║
 ║                            ║
 ║    Hello World             ║
 ║                            ║
 ║                            ║
 ║                            ║
 ╚════════════════════════════╝

```