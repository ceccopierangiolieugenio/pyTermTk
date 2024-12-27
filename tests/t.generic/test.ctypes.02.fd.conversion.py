#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2021 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Example from:
#   https://www.linuxjournal.com/article/4600
#   https://stackoverflow.com/questions/3794309/python-ctypes-python-file-object-c-file

import os
import sys

import ctypes

libc = ctypes.cdll.LoadLibrary('libc.so.6') # libc.so.6
# libc = ctypes.CDLL(ctypes.util.find_library("c"))

cstdout = ctypes.c_void_p.in_dll(libc, 'stdout')
cstdin = ctypes.c_void_p.in_dll(libc, 'stdin')

print(f"{cstdout=}                    {cstdin=}")
print(f"{sys.stdout.fileno()=}        {sys.stdin.fileno()=}")
print(f"{sys.stdout=}                 {sys.stdin=}")

# Get the file descriptor of stdin
# fd = sys.stdin.fileno()
# fd = sys.stdout.fileno()
fd = sys.stderr.fileno()

# Define the prototype of fdopen
libc.fdopen.argtypes = [ctypes.c_int, ctypes.c_char_p]
libc.fdopen.restype = ctypes.c_void_p  # FILE * is a void pointer

# Convert to FILE *
mode = b"r"  # File mode (read)
file_ptr = libc.fdopen(fd, mode)

print(f"FILE * pointer: {file_ptr}")

# Define the prototype of fileno
libc.fileno.argtypes = [ctypes.c_void_p]
libc.fileno.restype = ctypes.c_int

# Convert FILE * back to file descriptor
fd_back = libc.fileno(file_ptr)

print(f"Back to file descriptor: {fd_back}")

# Convert file descriptor to Python file object
with os.fdopen(fd_back, "r") as file_obj:
    print(f"File obj: {file_obj=} {file_obj.fileno()=} ")