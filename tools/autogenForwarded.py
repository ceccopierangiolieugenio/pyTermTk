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

def read_file_to_lines(file_path: str) -> Optional[List[str]]:
    """
    Reads a file and returns a list of strings, one for each line.

    Args:
        file_path (str): The path to the file.

    Returns:
        list: A list of strings, where each string is a line from the file.
              Returns None if the file cannot be opened.
    """
    try:
        with open(file_path, 'r') as f:
            lines: List[str] = f.readlines()
        return lines
    except FileNotFoundError:
        print(f"Error: File not found at path: {file_path}")
        return None
    except Exception as e:
        print(f"Error: An error occurred while reading the file: {e}")
        return None

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

from typing import List, Optional

def extract_and_process_lines(lines: List[str]) -> Tuple[Dict,List[str]]:
    """
    Extracts lines between '#--START-FORWARD-AUTOGEN--#' and '#--END--#' delimiters,
    uncomments them, and removes the slice after the '#' character.

    Args:
        lines (List[str]): A list of strings representing the lines of a file.
    """
    start_delimiter = "#--START-FORWARD-AUTOGEN--#"
    end_delimiter = "#--END--#"
    filtered_lines: List[str] = []
    extracted_lines: List[str] = []
    extracting = False

    content_re = re.compile(r'^ *#([^#]*)(?:#.*)?$')
    for line in lines:
        if start_delimiter in line:
            filtered_lines.append(line)
            extracting = True
            continue
        if end_delimiter in line:
            filtered_lines.append(line)
            extracting = False
            break

        if not extracting:
            filtered_lines.append(line)
        elif _m:=content_re.match(line):
            filtered_lines.append(line)
            # Uncomment the line by removing the leading '#' and space (if present)
            uncommented_line = _m.group(1)
            extracted_lines.append(uncommented_line)

    if not extracted_lines:
        return {},[]

    return json.loads(''.join(extracted_lines)), filtered_lines

def autogen_methods(data: Dict[str, Any]) -> List[str]:
    """
    Generates a list of method signatures and return types for a given class.

    Args:
        data (Dict[str, Any]): A dictionary containing the class name and a list of methods.
            Example: {'class': 'TTkTexteditView', 'methods': ['clear', 'setText', ...]}

    Returns:
        List[str]: A list of strings, where each string is a method signature and return type.
    """
    import TermTk as ttk

    class_name = data.get('class')
    methods = data.get('methods', [])
    signatures: List[str] = []

    if not class_name or not methods:
        print("Error: 'class' or 'methods' key missing or empty in JSON data.")
        return []

    try:
        # Get the class from the ttk module
        cls = getattr(ttk, class_name)
    except AttributeError:
        print(f"Error: Class '{class_name}' not found in TermTk module.")
        return []

    for method_name in methods:
        try:
            # Get the method from the class
            method = getattr(cls, method_name)
            sig = inspect.signature(method)
            return_type = sig.return_annotation
            params = ', '.join([f"{_p}={_p}" for _p in sig.parameters.keys() if _p != 'self'])

            source = inspect.getsource(method)
            # Extract the first line, which should be the method definition
            lines = source.splitlines()
            for i,line in enumerate(lines):
                if line.startswith('    def '):
                    lines = lines[:i]
                    lines.append(line)
                    break
            # Format the signature string
            signatures.extend([
                *[f"{_l}\n" for _l in lines],
                # f"    def {method_name}{sig}:",
                ])
            if '=kwargs' in params and '=args' in params:
                signatures.append(f"        return {data['instance']}.{method_name}(*args, **kwargs)\n")
            elif '=kwargs' in params:
                signatures.append(f"        return {data['instance']}.{method_name}(**kwargs)\n")
            elif '=args' in params:
                signatures.append(f"        return {data['instance']}.{method_name}(*args)\n")
            else:
                signatures.append(f"        return {data['instance']}.{method_name}({params})\n")

        except AttributeError:
            print(f"Error: Method '{method_name}' not found in class '{class_name}'.")
        except Exception as e:
            print(f"Error: An error occurred while processing method '{method_name}': {e}")

    return signatures

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Read a file and write its lines to another file.")
    parser.add_argument("input_path", type=str, help="The path to the input file to read.")
    parser.add_argument("output_path", type=str, nargs='?', default=None, help="The path to the output file to write. If not specified, prints to stdout.")

    args = parser.parse_args()

    lines = read_file_to_lines(args.input_path)

    if lines:
        autogen_data, filtered_source = extract_and_process_lines(lines)
        print(autogen_data)

        if autogen_data:
            autogenenerated = autogen_methods(autogen_data)
            # print('\n'.join(autogenenerated))
            end_delimiter = "    #--END--#"
            if not (index := filtered_source.index(end_delimiter)):
                raise ValueError("End Delimiter not found in the filtered lines")
            filtered_source[index:index] = autogenenerated
            print(''.join(filtered_source))
            if args.output_path:
                if not write_lines_to_file(filtered_source, args.output_path):
                    print("Error: Failed to write to output file.")
        # else:
        #     for line in lines:
        #         print(line, end='')  # Print each line without extra newlines