# [pyTermTk](https://github.com/ceccopierangiolieugenio/pyTermTk) - Logging

## Intro
The [TTkLog](https://ceccopierangiolieugenio.github.io/pyTermTk/TTkCore/log.html) class provide a set of api to allow and configure the logging.


## Example 1 - Log to file
From [example1.logtofile.py](logging/example1.logtofile.py)

```python
import TermTk as ttk

    # session.log is used by default
ttk.TTkLog.use_default_file_logging()

ttk.TTkLog.info(    "Test Info Messgae")
ttk.TTkLog.debug(   "Test Debug Messgae")
ttk.TTkLog.error(   "Test Error Messgae")
ttk.TTkLog.warn(    "Test Warning Messgae")
ttk.TTkLog.critical("Test Critical Messgae")
ttk.TTkLog.fatal(   "Test Fatal Messgae")
```

## Example 2 - Log to stdout
From [example2.logtostdout.py ](logging/example2.logtostdout.py )
```python
import TermTk as ttk

ttk.TTkLog.use_default_stdout_logging()

ttk.TTkLog.info(    "Test Info Messgae")
ttk.TTkLog.debug(   "Test Debug Messgae")
ttk.TTkLog.error(   "Test Error Messgae")
ttk.TTkLog.warn(    "Test Warning Messgae")
ttk.TTkLog.critical("Test Critical Messgae")
ttk.TTkLog.fatal(   "Test Fatal Messgae")
```

## Example 3 - custom logging
From [example3.customlogging.py ](logging/example3.customlogging.py )
```python
import TermTk as ttk

    # define the callback used to process the log message
def message_handler(mode, context, message):
    msgType = "NONE"
    if mode == ttk.TTkLog.InfoMsg:       msgType = "[INFO]"
    elif mode == ttk.TTkLog.WarningMsg:  msgType = "[WARNING]"
    elif mode == ttk.TTkLog.CriticalMsg: msgType = "[CRITICAL]"
    elif mode == ttk.TTkLog.FatalMsg:    msgType = "[FATAL]"
    elif mode == ttk.TTkLog.ErrorMsg:    msgType = "[ERROR]"
    print(f"{msgType} {context.file} {message}")

    # Register the callback to the message handler
ttk.TTkLog.installMessageHandler(message_handler)

ttk.TTkLog.info(    "Test Info Messgae")
ttk.TTkLog.debug(   "Test Debug Messgae")
ttk.TTkLog.error(   "Test Error Messgae")
ttk.TTkLog.warn(    "Test Warning Messgae")
ttk.TTkLog.critical("Test Critical Messgae")
ttk.TTkLog.fatal(   "Test Fatal Messgae")
```

## Example 4 - Use [TTkLogViewer](https://ceccopierangiolieugenio.github.io/pyTermTk/TTkTestWidgets/logviewer.html) widget
From [example4.ttklogviewer.py](logging/example4.ttklogviewer.py)
```python
import TermTk as ttk

root = ttk.TTk()

    # Create a window and attach it to the root (parent=root)
logWin = ttk.TTkWindow(parent=root,pos = (1,1), size=(80,20), title="LogViewer Window", border=True, layout=ttk.TTkVBoxLayout())

    # Attach the logViewer widget to the window
ttk.TTkLogViewer(parent=logWin)

ttk.TTkLog.info(    "Test Info Messgae")
ttk.TTkLog.debug(   "Test Debug Messgae")
ttk.TTkLog.error(   "Test Error Messgae")
ttk.TTkLog.warn(    "Test Warning Messgae")
ttk.TTkLog.critical("Test Critical Messgae")
ttk.TTkLog.fatal(   "Test Fatal Messgae")

    # Start the Main loop
root.mainloop()
```
The above code produces the following output

```text
╔══════════════════════════════════════════════════════════════════════════════╗
║ LogViewer Window                                                             ║
╟──────────────────────────────────────────────────────────────────────────────╢
║                                                                              ║
║INFO : tutorial/logging/example4.ttklogviewer.py:36 Test Info Messgae         ║
║DEBUG: tutorial/logging/example4.ttklogviewer.py:37 Test Debug Messgae        ║
║ERROR: tutorial/logging/example4.ttklogviewer.py:38 Test Error Messgae        ║
║WARNING : tutorial/logging/example4.ttklogviewer.py:39 Test Warning Messgae   ║
║CRITICAL: tutorial/logging/example4.ttklogviewer.py:40 Test Critical Messgae  ║
║FATAL: tutorial/logging/example4.ttklogviewer.py:41 Test Fatal Messgae        ║
║DEBUG: _/.venv/lib/python3.8/site-packages/TermTk/TTkCore/ttk.py:70 Starting M║
║DEBUG: _/.venv/lib/python3.8/site-packages/TermTk/TTkCore/ttk.py:80 Signal Eve║
║DEBUG: _/.venv/lib/python3.8/site-packages/TermTk/TTkCore/ttk.py:65 fps: 33   ║
║DEBUG: _/.venv/lib/python3.8/site-packages/TermTk/TTkCore/ttk.py:65 fps: 34   ║
║DEBUG: _/.venv/lib/python3.8/site-packages/TermTk/TTkCore/ttk.py:65 fps: 34   ║
║                                                                              ║
║                                                                              ║
║                                                                              ║
║◀▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓┄┄┄┄┄┄┄┄┄┄┄▶║
╚══════════════════════════════════════════════════════════════════════════════╝
```