# Run Python - pyTermTk on Wine32:
```bash
# cmd in the terminal
~/.var/app/net.lutris.Lutris/data/lutris/runners/wine/lutris-GE-Proton8-5-x86_64/bin/wine cmd
# cmd in a wine window
~/.var/app/net.lutris.Lutris/data/lutris//runners/wine/lutris-GE-Proton8-5-x86_64/bin/wine wineconsole

# Install python from https://www.python.org/downloads/windows/
# Copy the pyTermTk demo and TermTk folder in
# ~/.wine/drive_c/users/one/AppData/Local/Programs/Python/Python310-32

C:
cd C:\users\one\AppData\Local\Programs\Python\Python310-32
python.exe demo/demo.py
python.exe tests/test.input.win.py
```

# termios wrappers
 - termiWin -> https://github.com/veeso/termiWin

# Competitors with MS-Win support

### Textual -> https://github.com/Textualize/textual
https://github.com/Textualize/textual/blob/main/src/textual/drivers/win32.py

### TheVTPyProject -> https://github.com/srccircumflex/TheVTPyProject

# Incompatible code (the one using termios):
 - TermTk/TTkCore/TTkTerm/readinputlinux.py
 - TermTk/TTkCore/TTkTerm/readinputlinux_thread.py
 - TermTk/TTkCore/TTkTerm/term_unix.py
