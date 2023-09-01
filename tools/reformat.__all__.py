#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2023 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

# usage:
#
#    # Prepare the folders:
#    cp -a TermTk tmp
#
#    # Run the script
#    for i in $(find TermTk -name "*.py") ;
#        do echo $i ;
#        tools/reformat.__all__.py $i > tmp/$i ;
#    done
#

__all__ = []
__version__ = '1.0'
__author__ = 'Eugenio Parodi'

import os
import sys
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str, help='the filename')
    args = parser.parse_args()

    lines = []
    all = ''

    with open(args.filename) as f:
        while l := f.readline():
            # removing the python  header
            if "env python3" in l:
                while (l:=f.readline()) == '\n': pass

            # Process the __all__ directive
            if l.startswith('__all__'):
                all = l
                l = f.readline()
                if l != '\n':
                    lines.append(l)
            else:
                lines.append(l)

    for l in lines:
        if l == '# SOFTWARE.\n' and all:
            print(f"{l}\n{all}",end='')
        else:
            print(l,end='')

if __name__ == "__main__":
    main()