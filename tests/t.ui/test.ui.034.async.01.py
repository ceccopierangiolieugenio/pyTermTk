import asyncio
import inspect
import sys, os
import time

sys.path.append(os.path.join(sys.path[0],'..'))
import TermTk as ttk

root = ttk.TTk(layout=ttk.TTkVBoxLayout())
res = ttk.TTkLabel(parent=root)
num = ttk.TTkLabel(parent=root, text=1)
button_add = ttk.TTkButton(parent=root, text="+")
button_add.clicked.connect(lambda: num.setText(int(num.text()) + 1))
button_call = ttk.TTkButton(parent=root, text="Call")
ttk.TTkButton(parent=root, text="Quit").clicked.connect(ttk.TTkHelper.quit)

@ttk.pyTTkSlot()
def call0():
    res.setText("0 Calling...")
    time.sleep(1)
    res.setText("0 Calling... - DONE")

async def call1():
    res.setText("1 Calling...")
    await asyncio.sleep(3)
    res.setText("1 Calling... - DONE")

@ttk.pyTTkSlot()
async def call2():
    res.setText("2 Calling...")
    await asyncio.sleep(5)
    res.setText("2 Calling... - DONE")

@ttk.pyTTkSlot(int)
async def call3(val):
    res.setText(f"3 Calling... {val}")
    await asyncio.sleep(5)
    res.setText(f"3 Calling... {val} - DONE")

print(inspect.iscoroutinefunction(call0))
print(inspect.iscoroutinefunction(call1))
print(inspect.iscoroutinefunction(call2))
print(inspect.iscoroutinefunction(call3))

button_call.clicked.connect(call0)
button_call.clicked.connect(call1)
button_call.clicked.connect(call2)

root.mainloop()