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

import TermTk as ttk

class SuperObject():
    @staticmethod
    def dumpParams(obj,exclude=[]):
        def _dumpPrimitive(val):
            return val
        def _dumpTTkString(val):
            return val.toAnsi(True)
        def _dumpTTkColor(val):
            return str(val)
        def _dumpTTkLayout(val):
            return type(val).__name__
        def _dumpFlag(val):
            return val
        def _dumpList(val, propType):
            ret = []
            for i,t in enumerate(propType):
                if t['type'] in (int,str,float,bool):
                    ret.append(_dumpPrimitive(val[i]))
                elif type(t['type']) in (list,tuple):
                    ttk.TTkLog.warn("Feature not Implemented yet")
                elif t['type'] is ttk.TTkLayout:
                    ret.append(_dumpTTkLayout(val[i]))
                elif t['type'] in (ttk.TTkString,'singleLineTTkString'):
                    ret.append(_dumpTTkString(val[i]))
                elif t['type'] is ttk.TTkColor:
                    ret.append(_dumpTTkColor(val[i]))
                elif t['type'] in ('singleFlag','multiFlag'):
                    ret.append(_dumpFlag(val[i]))
                else:
                    ttk.TTkLog.warn("Type not Recognised")
            return ret

        params = {}
        for cc in reversed(type(obj).__mro__):
            # if hasattr(cc,'_ttkProperties'):
            if issubclass(cc, ttk.TTkWidget) or issubclass(cc, ttk.TTkLayout):
                ccName = cc.__name__
                if ccName in ttk.TTkUiProperties:
                    for p in ttk.TTkUiProperties[ccName]['properties']:
                        if p in exclude: continue
                        prop = ttk.TTkUiProperties[ccName]['properties'][p]
                        propType = prop['get']['type']
                        propCb = prop['get']['cb']
                        # ttk.TTkLog.debug(ccName)
                        if propType in (int,str,float,bool):
                            params |= {p: _dumpPrimitive(propCb(obj))}
                        elif type(propType) in (list,tuple):
                            params |= {p: _dumpList(propCb(obj), propType)}
                        elif propType is ttk.TTkLayout:
                            params |= {p: _dumpTTkLayout(propCb(obj))}
                        elif propType in (ttk.TTkString,'singleLineTTkString'):
                            params |= {p: _dumpTTkString(propCb(obj))}
                        elif propType is ttk.TTkColor:
                            params |= {p: _dumpTTkColor(propCb(obj))}
                        elif propType in ('singleflag','multiflags'):
                            params |= {p: _dumpFlag(propCb(obj))}
                        else:
                            ttk.TTkLog.warn("Type not Recognised")
        return params
