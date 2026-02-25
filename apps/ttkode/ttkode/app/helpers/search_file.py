# MIT License
#
# Copyright (c) 2026 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

__all__ = ['TTKode_SearchFile']

import os
import fnmatch
import mimetypes
from threading import Thread,Event,Lock

from pathlib import Path
from typing import List, Generator, Tuple, Optional

import TermTk as ttk

def is_text_file(file_path, block_size=512):
    # Check MIME type
    mime_type, _ = mimetypes.guess_type(file_path)
    text_based_mime_types = [
        'text/', 'application/json', 'application/xml',
        'application/javascript', 'application/x-httpd-php',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    ]
    if mime_type is not None and any(mime_type.startswith(mime) for mime in text_based_mime_types):
        return True

    # Check for non-printable characters
    try:
        with open(file_path, 'rb') as file:
            block = file.read(block_size)
        if b'\0' in block:
            return False
        text_characters = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)) - {0x7f})
        return not bool(block.translate(None, text_characters))
    except Exception as e:
        print(f"Error reading file: {e}")
        return False

def _load_gitignore_patterns(gitignore_path):
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r') as f:
            patterns = f.read().splitlines()
        return patterns
    return []

def _glob_match_patterns(path, patterns) -> bool:
    if path == '.':
        check_path = ''
    elif path.startswith('./'):
        check_path = path[2:]
    else:
        check_path = path
    return any(f"/{_p}/" in path for _p in patterns if _p) or any(fnmatch.fnmatch(check_path, _p) for _p in patterns if _p)

def _custom_walk(directory:str, include_patterns:List[str]=[], exclude_patterns:List[str]=[]) -> Generator[Tuple[str, str], None, None]:
    gitignore_path = os.path.join(directory, '.gitignore')
    exclude_patterns = exclude_patterns + _load_gitignore_patterns(gitignore_path)
    for entry in sorted(os.listdir(directory)):
        full_path = os.path.join(directory, entry)
        if _glob_match_patterns(full_path, exclude_patterns):
            continue
        if not os.path.exists(full_path):
            continue
        if os.path.isdir(full_path):
            if entry == '.git':
                continue
            yield from _custom_walk(full_path, include_patterns, exclude_patterns)
        else:
            if include_patterns and not _glob_match_patterns(full_path, include_patterns):
                continue
            yield directory, entry

class TTKode_SearchFile():
    @staticmethod
    def getFilesFromPattern(root_folder:Path, pattern:str) -> Generator[Tuple[Path], None, None]:
        for _dir, _fileName in _custom_walk(directory=root_folder):
            if not _glob_match_patterns(f"{_dir}/{_fileName}", [f"*{pattern}*"]):
                continue
            yield Path(_dir) / _fileName
