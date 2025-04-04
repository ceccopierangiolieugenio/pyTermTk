#!/usr/bin/env python3

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

__all__ = ['TloggCfg']

import os
import yaml

from .. import __version__

class TloggCfg:
    version=__version__
    name="tlogg"
    cfgVersion = '1.0'
    pathCfg="."
    colors=[]
    filters=[]
    options={}
    searches=[]
    maxsearches=200

    @staticmethod
    def save(searches=True, filters=True, colors=True, options=True):
        os.makedirs(TloggCfg.pathCfg, exist_ok=True)
        colorsPath   = os.path.join(TloggCfg.pathCfg,'colors.yaml')
        filtersPath  = os.path.join(TloggCfg.pathCfg,'filters.yaml')
        optionsPath  = os.path.join(TloggCfg.pathCfg,'options.yaml')
        searchesPath = os.path.join(TloggCfg.pathCfg,'searches.yaml')

        def writeCfg(path, cfg):
            fullCfg = {
                'version':TloggCfg.cfgVersion,
                'cfg':cfg }
            with open(path, 'w') as f:
                yaml.dump(fullCfg, f, sort_keys=False, default_flow_style=False)

        if colors:   writeCfg(colorsPath,   TloggCfg.colors)
        if filters:  writeCfg(filtersPath,  TloggCfg.filters)
        if options:  writeCfg(optionsPath,  TloggCfg.options)
        if searches: writeCfg(searchesPath, TloggCfg.searches)

    @staticmethod
    def load():
        colorsPath   = os.path.join(TloggCfg.pathCfg,'colors.yaml')
        filtersPath  = os.path.join(TloggCfg.pathCfg,'filters.yaml')
        optionsPath  = os.path.join(TloggCfg.pathCfg,'options.yaml')
        searchesPath = os.path.join(TloggCfg.pathCfg,'searches.yaml')

        if os.path.exists(colorsPath):
            with open(colorsPath) as f:
                TloggCfg.colors = yaml.load(f, Loader=yaml.SafeLoader)['cfg']
        if os.path.exists(filtersPath):
            with open(filtersPath) as f:
                TloggCfg.filters = yaml.load(f, Loader=yaml.SafeLoader)['cfg']
        if os.path.exists(optionsPath):
            with open(optionsPath) as f:
                TloggCfg.options = yaml.load(f, Loader=yaml.SafeLoader)['cfg']
        if os.path.exists(searchesPath):
            with open(searchesPath) as f:
                TloggCfg.searches = yaml.load(f, Loader=yaml.SafeLoader)['cfg']
