### mouse drag
https://github.com/vim/vim/blob/545c8a506e7e0921ded7eb7ffe3518279cbcb16a/src/os_unix.c
CSI ? 1000 h = enable the mouse press release reported by the terminal
CSI ? 1002 h = enable the mouse press release drag reported by the mouse terminal
if vim does not recognise the ttym flags either as (SGR, RXVT, XTERM2, XTERM), the mouse drag report is not requested
Note: My fault, my .vimrc does not set xterm2 if the environment is not inside tmux