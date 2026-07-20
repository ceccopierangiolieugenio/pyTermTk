#!/usr/bin/env python3

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

import sys
import json
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Release Helper Script")
    # Configuration File Argument
    parser.add_argument("--release", metavar="release_file", required=True, help="Path to the release file")

    args = parser.parse_args()

    # Load and parse configuration file if provided
    release_content = {}
    release_path = Path(args.release)

    if release_path.exists():
        try:
            release_content = json.loads(release_path.read_text())  # Parse the JSON file
        except json.JSONDecodeError:
            print(f"Error: Release file '{release_path}' is not valid JSON.")
            sys.exit(1)
        except OSError as e:
            print(f"Error: Could not read release file '{release_path}': {e}")
            sys.exit(1)

    input_data = {}
    if not sys.stdin.isatty():
        try:
            read = sys.stdin.read()
            input_data = json.loads(read)
        except json.JSONDecodeError:
            print("Error: Invalid JSON input.")
            sys.exit(1)

    # Merge release and input_data, with input_data taking priority
    merged = {**release_content, **input_data}

    # Save merged data back to release file
    try:
        release_path.write_text(json.dumps(merged, indent=2))
    except IOError as e:
        print(f"Error: Could not write to release file '{release_path}': {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

