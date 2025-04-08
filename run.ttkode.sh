#!/usr/bin/env bash
_PATH_SCRIPT="$(dirname $(realpath $0))"
PYTHONPATH=${_PATH_SCRIPT}/libs/pyTermTk:${_PATH_SCRIPT}/apps/ttkode python3 -m ttkode $@
