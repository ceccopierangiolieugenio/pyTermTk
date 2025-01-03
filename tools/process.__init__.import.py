#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2024 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

import os, sys, re
import ast
import _ast

sys.path.append(os.path.join(sys.path[0],'..'))

import TermTk as ttk

def find_init_and_files(folder_path):
    """
    Recursively scan a folder to find __init__.py files and list all files in their directories.

    Args:
        folder_path (str): The folder to scan.

    Returns:
        dict: A dictionary with __init__.py paths as keys and arrays of files in their directories as values.
    """
    init_files_dict = {}

    for root, _, files in os.walk(folder_path):
        if "__init__.py" in files:
            init_path = os.path.join(root, "__init__.py")
            files_in_folder = [os.path.join(root, f) for f in files if f != "__init__.py"]
            init_files_dict[init_path] = files_in_folder

    return init_files_dict

def find_init_and_files(folder_path):
    """
    Recursively scan a folder to find __init__.py files and list all files in their directories.

    Args:
        folder_path (str): The folder to scan.

    Returns:
        dict: A dictionary with __init__.py paths as keys and arrays of files in their directories as values.
    """
    init_files_dict = {}

    for root, _, files in os.walk(folder_path):
        if "__init__.py" in files:
            init_path = os.path.join(root, "__init__.py")
            files_in_folder = [os.path.join(root, f) for f in files if f != "__init__.py"]
            init_files_dict[init_path] = files_in_folder

    return init_files_dict

def get_variables(node):
    variables = {}
    if hasattr(node, 'body'):
        for subnode in node.body:
            variables |= get_variables(subnode)
    elif isinstance(node, _ast.Assign):
        for name in node.targets:
            if isinstance(name, _ast.Name) and name.id == '__all__':
                variables[name.id] = sorted([x.value for x in node.value.elts])
    return variables

def get_variables2(tree):
    return {
            node.targets[0].id: node.value.id
            for node in ast.walk(tree)
            if isinstance(node, ast.Assign)
        }


ret = find_init_and_files('TermTk')
for init in ret:
    dirname = os.path.dirname(init)
    initName = os.path.basename(init)
    print(f"{dirname} - {initName}")
    initLines = []
    with open(init) as fh:
        initLines = fh.read().split('\n')
    outLines = []
    for line in initLines:
        if not (m := re.match('( *from *\.([^ ]*) *import *)\*', line)):
            outLines.append(line)
        else:
            prefix   = m.group(1)
            fileName = f"{dirname}/{m.group(2)}.py"
            print(f"{m.group(0)} | {m.group(1)} | {m.group(2)}")
            if fileName in ret[init]:
                vars = get_variables(ast.parse(open(fileName).read()))
                if '__all__' in vars:
                    if _va:=vars['__all__']:
                        _line = f"{prefix}{', '.join(_va)}"
                    else:
                        _line = f"# {prefix}*"
                    print(_line)
                    print(ttk.TTkString(f"  - {fileName}:{vars['__all__']}", ttk.TTkColor.GREEN).toAnsi())
                    outLines.append(_line)
                else:
                    print(ttk.TTkString(f"  - {fileName}: No __all__ Found", ttk.TTkColor.RED).toAnsi())
                    outLines.append(line)
            else:
                outLines.append(line)
                print(f"{fileName} not in {ret[init]}")
    print('\n'.join(outLines))
    with open(init, 'w') as fp:
        fp.write('\n'.join(outLines))




    # with open(fileName, 'w') as fp:
    #         fp.write(textEdit.toPlainText())

    # os.path.basename(init)
    # for file in ret[init]:
    #     vars = get_variables(ast.parse(open(file).read()))
    #     if '__all__' in vars:
    #         print(ttk.TTkString(f"  - {file}:{vars['__all__']}", ttk.TTkColor.GREEN).toAnsi())
    #     else:
    #         print(ttk.TTkString(f"  - {file}: No __all__ Found", ttk.TTkColor.RED).toAnsi())

# for root, _, files in os.walk('TermTk'):
#     for file in files:
#         initLines = []
#         with open(f"{root}/{file}") as fh:
#             initLines = fh.read().split('\n')

