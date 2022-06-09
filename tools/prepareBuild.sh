#!/usr/bin/env bash

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


_PWD=`pwd`
_TOOLS_BASE_PATH=$(dirname $(readlink -f $0))
_BASE_PATH=${_TOOLS_BASE_PATH}/..
_TMP_PATH=${_BASE_PATH}/tmp
_VERSION=$(git describe | sed 's,\([^-]*\)-\([^-]*\)-[^-]*,\1\2,')

_tools_usage()
{
        echo "usage:"
        echo "    $0 <command>"
        echo ""
        echo "The $0 commands are:"
        echo "    test     - prepare test build environment"
        echo "    release  - prepare release build environment"
}


if [ "$#" -ne 1 ]; then
        _tools_usage
        exit 1
fi

case $1 in
        -h | --help)
                _tools_usage
                exit 1
                ;;
        test)
                _NAME='example-pkg-ceccopierangiolieugenio'
                ;;
        release)
                _NAME='pyTermTk'
                ;;
        *)
                echo "Option \"$2\" not recognized"
                echo ""
                _tools_usage
                exit 0
                ;;
esac

echo Version: ${_VERSION}
echo Name: ${_NAME}

mkdir -p ${_TMP_PATH}
rm -rf ${_TMP_PATH}/*

cp setup.py README.md LICENSE ${_TMP_PATH}

cp -a ${_BASE_PATH}/TermTk ${_TMP_PATH}
sed "s,__VERSION__,${_VERSION}," -i ${_TMP_PATH}/TermTk/TTkCore/cfg.py
sed "s,__NAME__,${_NAME}," -i ${_TMP_PATH}/TermTk/TTkCore/cfg.py
