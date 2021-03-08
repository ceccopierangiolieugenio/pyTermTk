# [pyTermTk](https://github.com/ceccopierangiolieugenio/pyTermTk) - Hello World

## Intro
 - Creating a simple GUI application using [pyTermTk](https://github.com/ceccopierangiolieugenio/pyTermTk) involves the following steps −
 - Import TermTk package.
 - Create an [TTk](https://ceccopierangiolieugenio.github.io/pyTermTk/TTkCore/ttk.html) object.
 - Add a [TTkLabel](https://ceccopierangiolieugenio.github.io/pyTermTk/TTkWidgets/label.html) object in it with the caption "**hello world**" in the position (x=5,y=2).
 - Enter the mainloop of application by [mainloop()](https://ceccopierangiolieugenio.github.io/pyTermTk/TTkCore/ttk.html#TermTk.TTkCore.ttk.TTk.mainloop) method.

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