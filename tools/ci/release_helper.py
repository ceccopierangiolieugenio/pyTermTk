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

import argparse
from dataclasses import dataclass
from typing import List

@dataclass
class _AppData():
    name: str
    path: str
    pypi: bool = False
    itch: bool = False

apps_data = [
        _AppData( name="pyTermTk"      , path="libs/pyTermTk"      , pypi=True ),
        _AppData( name="dumbPaintTool" , path="apps/dumbPaintTool" , pypi=True , itch=True  ),
        _AppData( name="ttkDesigner"   , path="apps/ttkDesigner"   , pypi=True ),
        _AppData( name="ttkode"        , path="apps/ttkode"        , pypi=True ),
        _AppData( name="tlogg"         , path="apps/tlogg"         , pypi=True )
      ]

def main():
    parser = argparse.ArgumentParser(description="Release Helper Script")
    subparsers = parser.add_subparsers(title="Features", dest="feature")

    # Apps Feature
    apps_parser = subparsers.add_parser("apps", help="Apps related operations")
    apps_parser.add_argument("--list", action="store_true", help="List available apps")
    apps_parser.add_argument("--build", metavar="app_name", type=str, help="Build a specific app")

    # Matrix Feature
    matrix_parser = subparsers.add_parser("matrix", help="Matrix related operations")
    matrix_parser.add_argument("--generate", action="store_true", help="Generate a matrix configuration")
    matrix_parser.add_argument("--os", metavar="os_name", type=str, help="Specify the OS for the matrix")

    # Add more features as needed

    args = parser.parse_args()

    if args.feature == "apps":
        if args.list:
            print("Available Apps:")
            for app in apps_data:
                print(f"  - {app.name}")
        elif args.build:
            print(f"Building app: {args.build}")
            # Implement build logic here
        else:
            apps_parser.print_help()

    elif args.feature == "matrix":
        if args.generate:
            print("Generating matrix configuration")
            # Implement matrix generation logic here
        elif args.os:
            print(f"Specifying OS: {args.os}")
            # Implement OS specific logic here
        else:
            matrix_parser.print_help()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()