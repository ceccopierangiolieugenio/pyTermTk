#!/usr/bin/env python3
# MIT License
#
# Copyright (c) 2025 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

import re
import json
import argparse
import inspect
from typing import List, Optional, Dict, Tuple, Any

def read_file_to_lines(file_path: str) -> List[str]:
    """
    Reads a file and returns a list of strings, one for each line.

    Args:
        file_path (str): The path to the file.

    Returns:
        list: A list of strings, where each string is a line from the file.
              Returns None if the file cannot be opened.
    """
    with open(file_path, 'r') as f:
        lines: List[str] = f.readlines()
        return lines
    raise Exception()

def write_lines_to_file(lines: List[str], output_path: str) -> bool:
    """
    Writes a list of strings to a file, one string per line.

    Args:
        lines (list): The list of strings to write.
        output_path (str): The path to the output file.

    Returns:
        bool: True if the write was successful, False otherwise.
    """
    try:
        with open(output_path, 'w') as f:
            for line in lines:
                f.write(line)
        return True
    except Exception as e:
        print(f"Error: An error occurred while writing to the file: {e}")
        return False

def find_method_origin(cls, method_name: str) -> type | None:
    """
    Finds the class in which a method is originally defined in a class hierarchy.

    Args:
        cls: The class to start searching from.
        method_name: The name of the method to find.

    Returns:
        The class in which the method is originally defined, or None if the method is not found
        in the class hierarchy.
    """
    for base in inspect.getmro(cls):
        if method_name in base.__dict__:
            return base
    return None

def get_field_docstring(cls, field_name: str) -> str | None:
    """
    Retrieves the docstring of a field (attribute) in a class.

    This function assumes the docstring is defined directly after the field
    declaration in the class definition.

    Args:
        cls: The class object.
        field_name: The name of the field.

    Returns:
        The docstring of the field, or None if the field or docstring is not found.
    """
    try:

        # Get the source code of the class
        source = inspect.getsource(cls)

        # Construct a regex to find the field and its docstring
        pattern = rf'\s*{field_name}:.*\n\s*"""(.*?)"""'

        # Search for the pattern in the source code
        match = re.search(pattern, source, re.DOTALL)  # re.DOTALL allows . to match newlines

        if match:
            return match.group(1).strip()  # Return the docstring, stripping whitespace
        else:
            print(f"Docstring not found for field '{field_name}' in class '{cls.__name__}'.")
            return None

    except AttributeError:
        print(f"Error: Field '{field_name}' not found in class '{cls.__name__}'.")
        return None
    except OSError:
        print(f"Error: Could not retrieve source code for class '{cls.__name__}'.")
        return None
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")
        return None


def _index_of(_m:str, lines:List[str]) -> int:
    for i,l in enumerate(lines):
        if _m in l:
            return i
    raise ValueError(f"End Delimiter '{_m}' not found in the filtered lines")

marker_params = "#--FORWARD-AUTOGEN-PARAMS--#"
marker_start = "#--FORWARD-AUTOGEN-START--#"
marker_end = "#--FORWARD-AUTOGEN-END--#"

def extract_and_process_lines(lines: List[str]) -> Dict:
    """
    Extracts lines between '#--START-FORWARD-AUTOGEN--#' and '#--END--#' delimiters,
    uncomments them, and removes the slice after the '#' character.

    Args:
        lines (List[str]): A list of strings representing the lines of a file.
    """

    index_params = _index_of(marker_params,lines)
    index_start = _index_of(marker_start,lines)
    index_end = _index_of(marker_end,lines)

    param_lines: List[str] = lines[index_params+1:index_start]
    extracted_lines: List[str] = []
    lines[index_start+1:index_end] = []

    content_re = re.compile(r'^ *#([^#]*)(?:#.*)?$')
    for line in param_lines:
        if _m:=content_re.match(line):
            uncommented_line = _m.group(1)
            extracted_lines.append(uncommented_line)

    if not extracted_lines:
        return {}

    return json.loads(''.join(extracted_lines))

from TermTk.TTkAbstract.abstractscrollarea import _ForwardData
def autogen_methods(data: _ForwardData) -> List[str]:
    """
    Generates a list of method signatures and return types for a given class.

    Args:
        data (Dict[str, Any]): A dictionary containing the class name and a list of methods.
            Example: {'class': 'TTkTexteditView', 'methods': ['clear', 'setText', ...]}

    Returns:
        List[str]: A list of strings, where each string is a method signature and return type.
    """
    import TermTk as ttk

    class_name = data.forwardClass.__name__
    signatures: List[str] = []

    for method_name in data.methods:
        try:
            # Get the method from the class
            method = getattr(data.forwardClass, method_name)
            sig = inspect.signature(method)
            doc = inspect.getdoc(method)
            return_type = sig.return_annotation
            params = ', '.join([f"{_p}={_p}" for _p in sig.parameters.keys() if _p != 'self'])

            source = inspect.getsource(method)
            # Extract the first line, which should be the method definition
            lines = source.splitlines()
            index_func = _index_of('    def ',lines)
            lines = lines[:index_func+1]
            doc_indent = "        "
            lines.extend([
                doc_indent + f"'''",
                doc_indent + f".. seealso:: this method is forwarded to :py:meth:`{class_name}.{method_name}`\n",
            ])
            if doc:
                lines.extend([doc_indent + _l for _l in doc.split('\n')])
            lines.append(doc_indent + "'''")
            # Format the signature string
            signatures.extend([
                *[f"{_l}\n" for _l in lines],
                # f"    def {method_name}{sig}:",
                ])
            if '=kwargs' in params and '=args' in params:
                signatures.append(f"        return {data.instance}.{method_name}(*args, **kwargs)\n")
            elif '=kwargs' in params:
                signatures.append(f"        return {data.instance}.{method_name}(**kwargs)\n")
            elif '=args' in params:
                signatures.append(f"        return {data.instance}.{method_name}(*args)\n")
            else:
                signatures.append(f"        return {data.instance}.{method_name}({params})\n")

        except AttributeError:
            print(f"Error: Method '{method_name}' not found in class '{class_name}'.")
        except Exception as e:
            print(f"Error: An error occurred while processing method '{method_name}': {e}")

    return signatures


def autogen_signals(data: Dict[str, Any]) -> List[str]:
    """
    Generates a list of signal signatures and return types for a given class.

    Args:
        data (Dict[str, Any]): A dictionary containing the class name and a list of signals.
            Example: {'signals': 'TTkTextedit._signals'}

    Returns:
        List[str]: A list of strings, where each string is a method signature and return type.
    """
    import TermTk as ttk

    if not 'signals' in data:
        raise ValueError('"sigals" not in data')

    class_name,signals_list_name = data['signals'].split('.')
    signatures: List[str] = []

    try:
        # Get the class from the ttk module
        cls = getattr(ttk, class_name)
        signals = getattr(cls, signals_list_name)
        cls = getattr(ttk, data['class'])
    except AttributeError:
        print(f"Error: Class '{class_name}' not found in TermTk module.")
        return []

    for signal_name in signals:
        try:
            # Get the method from the class
            signal = getattr(cls, signal_name)
            doc = get_field_docstring(cls, signal_name)
            print(doc)
        except AttributeError:
            print(f"Error: Signal '{signal_name}' not found in class '{class_name}'.")
        except Exception as e:
            print(f"Error: An error occurred while processing signal '{signal_name}': {e}")

    return signatures

def get_classes_with_source_from_module(module) -> List[Dict[str, Any]]:
    classes_with_source: List[Dict[str, Any]] = []

    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj) and hasattr(obj,'_ttk_forward'):
            try:
                source = inspect.getsource(obj)
                filename = inspect.getfile(obj)
                classes_with_source.append({
                    'class': obj,
                    'name': name,
                    'forward': obj._ttk_forward,
                    'module': module.__name__,
                    'filename': filename,
                    'source': source
                })
            except OSError as e:
                print(f"Could not get source for class {name}: {e}")
            except Exception as e:
                print(f"Unexpected error getting source for class {name}: {e}")

    return classes_with_source


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Read a file and write its lines to another file.")
    parser.add_argument('--apply', action='store_true', help='Apply the changes')
    args = parser.parse_args()

    import TermTk as ttk
    classes = get_classes_with_source_from_module(ttk)
    args = parser.parse_args()
    if classes:
        for class_data in classes:
            print(f"Class Name: {class_data['name']}")
            print(f"  Class: {class_data['class']}")
            print(f"  Forward: {class_data['forward']}")
            print(f"  Module: {class_data['module']}")
            print(f"  Filename: {class_data['filename']}")
            # print(f"  Source:\n{class_data['source']}")
            autogenenerated = autogen_methods(class_data['forward'])
            if args.apply:
                lines = read_file_to_lines(class_data['filename'])
                index_start = _index_of(marker_start,lines)
                index_end = _index_of(marker_end,lines)
                lines[index_start+1:index_end] = autogenenerated
                write_lines_to_file(lines,class_data['filename'])
            else:
                print(''.join(autogenenerated))
    else:
        print("No classes found in the module.")