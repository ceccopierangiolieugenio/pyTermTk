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
import sys
import glob
import json
import argparse
import fileinput
from dataclasses import dataclass
from enum import Enum

from typing import List, Dict

class MatrixType(Enum):
    ALL = "all"
    PYPI = "pypi"
    ITCH = "itch"

@dataclass
class _AppData():
    name: str
    path: str
    version: str
    pypi: bool = False
    itch: bool = False

    def to_dict(self) -> Dict[str, str]:
        return {
            "name": self.name,
            "path": self.path,
            "version" : self.version,
            "pypi": self.pypi,
            "itch": self.itch
        }

def _print_info(apps_data:List[_AppData]) -> None:
    for _a in apps_data:
        print(f"{_a.name} : {_a.version}")

# for item in $(jq -r '.[].path' <<< ${APPS_ARRAY}) ; do; do
#   # Update version in the project
#   _VERSION=$(_get_version ${item})
#   _NAME=$(_get_name ${item})
#   if grep -q "${_NAME}: ${_VERSION}" <<< ' ${{ steps.release-please.outputs.pr }}' ; then
#     sed -i \
#       "s|__version__:str.*|__version__:str = '${_VERSION}'|" \
#       ${item}/*/__init__.py
#     sed  "s|'pyTermTk *>=[^']*'|'pyTermTk>=${_VERSION_TTK}'|" -i ${item}/pyproject.toml
#     echo ✅ Bumped ${_NAME} to ${_VERSION}
#   else
#     echo 🆗 No new release found for ${_NAME}
#   fi
# done
def _upgrade_files(apps_data:List[_AppData], rp_data:Dict, dry_run:bool) -> None:
    _ttk = [_a for _a in apps_data if _a.name=='pyTermTk'][0]
    for _a in apps_data:
        print(f"{_a.name} : {_a.version}")
        if f"{_a.name}: {_a.version}" in rp_data.get('pr',''):
            print(f"sed {_a.path}/*/__init__.py <<< {_a.version}")

            pattern = re.compile(r"__version__:str.*")
            replacement=f"__version__:str = '{_a.version}'"
            files = glob.glob(f"{_a.path}/*/__init__.py")
            if dry_run:
                print(files, replacement)
            else:
                for line in fileinput.input(files, inplace=True):
                    print(pattern.sub(replacement, line), end="")

            pattern = re.compile(r"'pyTermTk *>=[^']*'")
            replacement = f"'pyTermTk>={_ttk.version}'"

            files = glob.glob(f"{_a.path}/pyproject.toml")
            if dry_run:
                print(files, replacement)
            else:
                for line in fileinput.input(files, inplace=True):
                    print(pattern.sub(replacement, line), end="")


def _gen_matrix(matrix_type: MatrixType, rp_data:Dict, apps_data:List[_AppData]) -> List[_AppData]:
    if matrix_type == MatrixType.PYPI:
        apps = [app for app in apps_data if app.pypi]
    elif matrix_type == MatrixType.ITCH:
        apps = [app for app in apps_data if app.itch]
    elif matrix_type == MatrixType.ALL:
        apps = apps_data
    else:
        raise ValueError(f"Invalid matrix type: {matrix_type}")

    if 'pr' not in rp_data:
        return []

    pr = json.loads(rp_data['pr'])

    apps = [app for app in apps if f"<summary>{app.name}:" in pr.get('body', "")]

    return apps

def main():
    parser = argparse.ArgumentParser(description="Release Helper Script")
    subparsers = parser.add_subparsers(title="Features", dest="feature")

    # Apps Feature
    info_parser = subparsers.add_parser("info", help="Print release info")

    upgrade_parser = subparsers.add_parser("upgrade", help="update the app versions")
    upgrade_parser.add_argument("--dry-run", action="store_true", help="Do not apply thw changes")

    # Apps Feature
    apps_parser = subparsers.add_parser("apps", help="Apps related operations")
    apps_parser.add_argument("--list", action="store_true", help="List available apps")
    apps_parser.add_argument("--build", metavar="app_name", type=str, help="Build a specific app")

    # Matrix Feature
    matrix_parser = subparsers.add_parser("matrix", help="Matrix related operations")
    matrix_parser.add_argument("type", metavar="matrix_type", type=str, choices=[e.value for e in MatrixType], help="Specify the type of matrix to generate")
    matrix_parser.add_argument("--generate", action="store_true", help="Generate a matrix configuration")

    # Configuration File Argument
    parser.add_argument("--config",   metavar="config_file", type=argparse.FileType("r"), help="Path to the configuration file")
    parser.add_argument("--manifest", metavar="config_file", type=argparse.FileType("r"), help="Path to the configuration file")

    args = parser.parse_args()

    # Load and parse configuration file if provided
    config = {}
    if args.config:
        try:
            config = json.load(args.config)  # Parse the JSON file
            # print(f"Loaded configuration: {json.dumps(config, indent=2)}")
        except json.JSONDecodeError:
            print(f"Error: Configuration file '{args.config.name}' is not valid JSON.")
            sys.exit(1)

    # Load and parse configuration file if provided
    manifest = {}
    if args.manifest:
        try:
            manifest = json.load(args.manifest)  # Parse the JSON file
            # print(f"Loaded manifesturation: {json.dumps(manifest, indent=2)}")
        except json.JSONDecodeError:
            print(f"Error: Configuration file '{args.manifest.name}' is not valid JSON.")
            sys.exit(1)

    input_data = {}
    if not sys.stdin.isatty(): # or sys.stdin.peek(1):
        try:
            read = sys.stdin.read()
            input_data = json.loads(read)
        except json.JSONDecodeError:
            print("Error: Invalid JSON input.")
            sys.exit(1)

    apps_data = [
        _AppData(
            name=_v.get('package-name',''),
            path=_a,
            version=manifest.get(_a,"0.0.0"),
            itch=_v.get('itch',False),
            pypi=_v.get('pypi',False))
                for _a,_v in config.get('packages',{}).items()]

    # print(apps_data)

    if args.feature == "info":
        _print_info(apps_data)
    elif args.feature == "upgrade":
        print(args)
        _upgrade_files(apps_data, input_data, args.dry_run)
    elif args.feature == "apps":
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
        matrix_type = MatrixType(args.type)
        matrix = _gen_matrix(matrix_type, input_data, apps_data)
        print(json.dumps(
                {
                    'has_matrix': bool(matrix),
                    'matrix':[app.to_dict() for app in matrix]
                }
            , indent=2))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()