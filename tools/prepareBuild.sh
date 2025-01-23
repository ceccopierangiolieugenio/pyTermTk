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

_MAJOR=$( git describe --tags | sed 's,\([0-9]*\)\..*,\1,'                     )
_MINOR=$( git describe --tags | sed 's,[0-9]*\.\([0-9]*\)\..*,\1,'             )
_PATCH=$( git describe --tags | sed 's,[0-9]*\.[0-9]*\.\([0-9]*\)[^0-9].*,\1,' )
_STAGE=$( git describe --tags | sed 's,[^-]*-a-\?\([0-9]*\).*,\1,'             )

_VERSION="${_MAJOR}.${_MINOR}.${_PATCH}-a${_STAGE}"
_DOCVERSION="${_MAJOR}.${_MINOR}.${_PATCH}-a"

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
                _BUILD_LIB='TermTk'
                _SETUP='setup.py'
                _README='README.md'
                _CFG='TermTk/TTkCore/cfg.py'
                ;;
        release)
                _NAME='pyTermTk'
                _BUILD_LIB='TermTk'
                _SETUP='setup.py'
                _README='README.md'
                _CFG='TermTk/TTkCore/cfg.py'
                ;;
        ttkDesigner)
                _NAME='ttkDesigner'
                _BUILD_LIB='apps/ttkDesigner'
                _SETUP='setup.ttkDesigner.py'
                _README='apps/ttkDesigner/README.md'
                _CFG='ttkDesigner/app/cfg.py'
                ;;
        dumbPaintTool)
                _NAME='dumbPaintTool'
                _BUILD_LIB='apps/dumbPaintTool'
                _SETUP='setup.dumbPaintTool.py'
                _README='apps/dumbPaintTool/README.md'
                _CFG='dumbPaintTool/app/cfg.py'
                ;;
        doc)
                rm -rf ${_TMP_PATH}
                mkdir -p ${_TMP_PATH}
                echo ${_DOCVERSION} > ${_TMP_PATH}/docversion.txt
                exit 0
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

cp ${_SETUP} ${_TMP_PATH}/setup.py
cp ${_README} LICENSE ${_TMP_PATH}

cp -a  ${_BASE_PATH}/${_BUILD_LIB}  ${_TMP_PATH}
sed "s,__VERSION__,${_VERSION}," -i ${_TMP_PATH}/${_CFG} ${_TMP_PATH}/setup.py
sed "s,__NAME__,${_NAME},"       -i ${_TMP_PATH}/${_CFG} ${_TMP_PATH}/setup.py
