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

__all__ = []

from TermTk.TTkCore.string import TTkString

# Note:
# This Class is supposed to be inherited by and only by
# terminal_screen.py : _TTkTerminalScreen
# Due to the huge amount of Escape commands required to be handled
# I decided to split tham in multiple files
class _TTkTerminalScreen_CSI():
    # CSI Ps @  Insert Ps (Blank) Character(s) (default = 1) (ICH).
    def _CSI___ICH(self, ps, _):
        x,y = self._terminalCursor
        w = self._w
        self._canvas._data[y][x:x] = ['']*ps
        self._canvas._colors[y][x:x] = [self._color]*ps
        self._canvas._data[y] = self._canvas._data[y][:w]
        self._canvas._colors[y] = self._canvas._colors[y][:w]

    # CSI Ps SP @   (SP = Space)
    #           Shift left Ps columns(s) (default = 1) (SL), ECMA-48.
    # def _CSI___SL( self, ps, _):
    #     x,y = self._terminalCursor
    #     self._canvas.drawText(' '*ps,pos=(x,y))

    # CSI Ps A  Cursor Up Ps Times (default = 1) (CUU).
    def _CSI_A_CUU(self, ps, _):
        x,y = self._terminalCursor
        self._terminalCursor = (x,max(0,y-ps))

    # CSI Ps SP A   (SP = Space)
    #           Shift right Ps columns(s) (default = 1) (SR), ECMA-48.
    # def _CSI_A_SR( self, ps, _):
    #     x,y = self._terminalCursor
    #     w,h = self._w, self._h
    #     self._terminalCursor = (min(x+ps,w-1),y)

    # CSI Ps B  Cursor Down Ps Times (default = 1) (CUD).
    def _CSI_B_CUD(self, ps, _):
        x,y = self._terminalCursor
        w,h = self._w, self._h
        self._terminalCursor = (x,min(y+ps,h-1))

    # CSI Ps C  Cursor Forward Ps Times (default = 1) (CUF).
    def _CSI_C_CUF(self, ps, _):
         x,y = self._terminalCursor
         w,h = self._w, self._h
         self._terminalCursor = (min(x+ps,w-1),y)

    # CSI Ps D  Cursor Backward Ps Times (default = 1) (CUB).
    def _CSI_D_CUB(self, ps, _):
         x,y = self._terminalCursor
         self._terminalCursor = (max(0,x-ps),y)

    # CSI Ps E  Cursor Next Line Ps Times (default = 1) (CNL).
    def _CSI_E_CNL(self, ps, _):
        x,y = self._terminalCursor
        w,h = self._w, self._h
        self._terminalCursor = (0,min(y+ps,h-1))

    # CSI Ps F  Cursor Preceding Line Ps Times (default = 1) (CPL).
    def _CSI_F_CPL(self, ps, _):
        x,y = self._terminalCursor
        self._terminalCursor = (0,max(0,y-ps))

    # CSI Ps G  Cursor Character Absolute  [column] (default = [row,1]) (CHA).
    def _CSI_G_CHA(self, col, _):
        x,y = self._terminalCursor
        w,h = self._w, self._h
        self._terminalCursor = (min(col-1,w-1),y)


    # CSI Ps ; Ps H
    #           Cursor Position [row;column] (default = [1,1]) (CUP).
    def _CSI_H_CUP(self, row, col):
        w,h = self._w, self._h
        self._terminalCursor = (min(col-1,w-1), min(row-1,h-1))

    # CSI Ps I  Cursor Forward Tabulation Ps tab stops (default = 1) (CHT).
    # def _CSI_I_CHT(self, ps, _): pass

    # CSI Ps J  Erase in Display (ED), VT100.
    #             Ps = 0  ⇒  Erase Below (default).
    #             Ps = 1  ⇒  Erase Above.
    #             Ps = 2  ⇒  Erase All.
    #             Ps = 3  ⇒  Erase Saved Lines, xterm.
    def _CSI_J_ED(self, ps, _):
        x,y = self._terminalCursor
        w,h = self._w,self._h
        if ps == 0:
            self._canvas.fill(char=' ', pos=(0,y+1),size=(w,h))
            self._canvas.fill(char=' ', pos=(x,y),size=(w,1))
        elif ps == 1:
            self._canvas.fill(char=' ', pos=(0,0),size=(w,y-1))
            self._canvas.fill(char=' ', pos=(0,y),size=(x,1))
        elif ps == 2:
            self._canvas.fill(char=' ', pos=(0,0),size=(w,h))

    # CSI ? Ps J
    #           Erase in Display (DECSED), VT220.
    #             Ps = 0  ⇒  Selective Erase Below (default).
    #             Ps = 1  ⇒  Selective Erase Above.
    #             Ps = 2  ⇒  Selective Erase All.
    #             Ps = 3  ⇒  Selective Erase Saved Lines, xterm.

    # CSI Ps K  Erase in Line (EL), VT100.
    #             Ps = 0  ⇒  Erase to Right (default).
    #             Ps = 1  ⇒  Erase to Left.
    #             Ps = 2  ⇒  Erase All.
    def _CSI_K_EL(self, ps, _):
        x,y = self._terminalCursor
        w,h = self._w,self._h
        if ps == 0:
            self._canvas.fill(char=' ', pos=(x,y),size=(w,1), color=self._color)
        elif ps == 1:
            self._canvas.fill(char=' ', pos=(0,y),size=(x,1), color=self._color)
        elif ps == 2:
            self._canvas.fill(char=' ', pos=(0,y),size=(w,1), color=self._color)

    # CSI ? Ps K
    #           Erase in Line (DECSEL), VT220.
    #             Ps = 0  ⇒  Selective Erase to Right (default).
    #             Ps = 1  ⇒  Selective Erase to Left.
    #             Ps = 2  ⇒  Selective Erase All.

    # CSI Ps L  Insert Ps Line(s) (default = 1) (IL).
    def _CSI_L_IL(self, ps, _):
        x,y = self._terminalCursor
        t,b = self._scrollingRegion
        w,h = self._w, self._h
        bkl = h-b
        l = len(self._canvas._data)
        #TODO: Avoid this HACK
        baseData = [' ']*w
        baseColors = [self._color]*w
        bkData   = self._canvas._data[-bkl:]
        bkColors = self._canvas._colors[-bkl:]
        self._canvas._data[y:y]   = [baseData.copy() for _ in range(ps)]
        self._canvas._colors[y:y] = [baseColors.copy() for _ in range(ps)]
        self._canvas._data   = self._canvas._data[:h-bkl] + bkData
        self._canvas._colors = self._canvas._colors[:h-bkl] + bkColors


    # CSI Ps M  Delete Ps Line(s) (default = 1) (DL).
    def _CSI_M_DL(self, ps, _):
        x,y = self._terminalCursor
        t,b = self._scrollingRegion
        w,h = self._w, self._h
        t=min(b,max(t,y))
        #TODO: Avoid this HACK
        baseData = [' ']*w
        baseColors = [self._color]*w
        # Split the content in 3 slices [top, center, bottom]
        topd = self._canvas._data[:t]
        topc = self._canvas._colors[:t]
        centerd = self._canvas._data[t:b]
        centerc = self._canvas._colors[t:b]
        bottomd = self._canvas._data[b:]
        bottomc = self._canvas._colors[b:]
        # Rotate the center part
        centerd = centerd[ps:] + [baseData.copy() for _ in range(ps)  ]
        centerc = centerc[ps:] + [baseColors.copy() for _ in range(ps)]
        centerd = centerd[:b-t]
        centerc = centerc[:b-t]
        # assemble it back
        self._canvas._data   = topd + centerd + bottomd
        self._canvas._colors = topc + centerc + bottomc

    # CSI Ps P  Delete Ps Character(s) (default = 1) (DCH).
    #   s1 = "abc12fg"
    #   x  = 3   |
    #   ps = 2
    #   s2 = "abcfg"
    def _CSI_P_DCH(self, ps, _):
        x,y = self._terminalCursor
        w,h = self._w, self._h
        ps = min(ps,w-x)
        self._canvas._data[y][x:x+ps]   = []
        self._canvas._colors[y][x:x+ps] = []
        self._canvas._data[y]   += [' ']*ps
        self._canvas._colors[y] += [self._color]*ps

    # CSI # P
    # CSI Pm # P
    #           Push current dynamic- and ANSI-palette colors onto stack
    #           (XTPUSHCOLORS), xterm.  Parameters (integers in the range 1
    #           through 10, since the default 0 will push) may be used to
    #           store the palette into the stack without pushing.

    # CSI # Q
    # CSI Pm # Q
    #           Pop stack to set dynamic- and ANSI-palette colors
    #           (XTPOPCOLORS), xterm.  Parameters (integers in the range 1
    #           through 10, since the default 0 will pop) may be used to
    #           restore the palette from the stack without popping.

    # CSI # R   Report the current entry on the palette stack, and the number
    #           of palettes stored on the stack, using the same form as
    #           XTPOPCOLOR (default = 0) (XTREPORTCOLORS), xterm.

    # CSI Ps S  Scroll up Ps lines (default = 1) (SU), VT420, ECMA-48.
    def _CSI_S_SU(self, ps, _=None):
        t,b = self._scrollingRegion
        w,h = self._w, self._h
        #TODO: Avoid this HACK... HAHAHHAHAHHAHA H HAHAHAHAH AHAHAHA HHAHA HA
        baseData = [' ']*w
        baseColors = [self._color]*w
        # Split the content in 3 slices [top, center, bottom]
        topd = self._canvas._data[:t]
        topc = self._canvas._colors[:t]
        topCNL = self._canvasNewLine[:t]
        topCLS = self._canvasLineSize[:t]
        centerd = self._canvas._data[t:b]
        centerc = self._canvas._colors[t:b]
        centerCNL = self._canvasNewLine[t:b]
        centerCLS = self._canvasLineSize[t:b]
        bottomd = self._canvas._data[b:]
        bottomc = self._canvas._colors[b:]
        bottomCNL = self._canvasNewLine[b:]
        bottomCLS = self._canvasLineSize[b:]
        # Push the rotated slices to the buffer
        for d,c,nl,sz in zip(
                    centerd[:ps],
                    centerc[:ps],
                    centerCNL[:ps],
                    centerCLS[:ps]):
            if sz:
                txt = TTkString._importString1(''.join(d[:sz]),c[:sz])
            else:
                txt = TTkString()
            if nl:
                self._bufferedLines[-1] += txt
            else:
                self._bufferedLines.append(txt)
            # from TermTk.TTkCore.log import TTkLog
            # TTkLog.debug(str(self._bufferedLines[-1])+f" - {sz=} {t=} {ps=} {self._canvasLineSize=}")
        # Rotate the center part
        centerd = centerd[ps:] + [baseData.copy() for _ in range(ps)  ]
        centerc = centerc[ps:] + [baseColors.copy() for _ in range(ps)]
        centerd = centerd[:b-t]
        centerc = centerc[:b-t]
        centerCNL = centerCNL[ps:] + [False]*ps
        centerCLS = centerCLS[ps:] + [0]*ps
        centerCNL = centerCNL[:b-t]
        centerCLS = centerCLS[:b-t]
        # assemble it back
        self._canvas._data   = topd + centerd + bottomd
        self._canvas._colors = topc + centerc + bottomc
        self._canvasNewLine  = topCNL + centerCNL + bottomCNL
        self._canvasLineSize = topCLS + centerCLS + bottomCLS
        self.bufferedLinesChanged.emit()

    # CSI ? Pi ; Pa ; Pv S
    #           Set or request graphics attribute (XTSMGRAPHICS), xterm.  If
    #           configured to support either Sixel Graphics or ReGIS Graphics,
    #           xterm accepts a three-parameter control sequence, where Pi, Pa
    #           and Pv are the item, action and value:
    #
    #             Pi = 1  ⇒  item is number of color registers.
    #             Pi = 2  ⇒  item is Sixel graphics geometry (in pixels).
    #             Pi = 3  ⇒  item is ReGIS graphics geometry (in pixels).
    #
    #             Pa = 1  ⇒  read attribute.
    #             Pa = 2  ⇒  reset to default.
    #             Pa = 3  ⇒  set to value in Pv.
    #             Pa = 4  ⇒  read the maximum allowed value.
    #
    #             Pv is ignored by xterm except when setting (Pa == 3 ).
    #             Pv = n ⇐  A single integer is used for color registers.
    #             Pv = width ; height ⇐  Two integers for graphics geometry.
    #
    #           xterm replies with a control sequence of the same form:
    #
    #                CSI ? Pi ; Ps ; Pv S
    #
    #           where Ps is the status:
    #             Ps = 0  ⇐  success.
    #             Ps = 1  ⇐  error in Pi.
    #             Ps = 2  ⇐  error in Pa.
    #             Ps = 3  ⇐  failure.
    #
    #           On success, Pv represents the value read or set.
    #
    #           Notes:
    #           o   The current implementation allows reading the graphics
    #               sizes, but disallows modifying those sizes because that is
    #               done once, using resource-values.
    #           o   Graphics geometry is not necessarily the same as "window
    #               size" (see the dtterm window manipulation extensions).
    #               XTerm limits the maximum graphics geometry according to
    #               the maxGraphicSize resource.
    #               The maxGraphicSize resource can be either an explicit
    #               heightxwidth (default: 1000x1000 as of version 328) or the
    #               word "auto" (telling XTerm to use limits the decGraphicsID
    #               or decTerminalID resource to determine the limits).
    #           o   XTerm uses the minimum of the window size and the graphic
    #               size to obtain the maximum geometry.
    #           o   While resizing a window will always change the current
    #               graphics geometry, the reverse is not true.  Setting
    #               graphics geometry does not affect the window size.
    #           o   If xterm is able to support graphics (compile-time), but
    #               is not configured (runtime) for graphics, these responses
    #               will indicate a failure.  Other implementations which do
    #               not use the maximum graphics dimensions but are configured
    #               for graphics should report zeroes for the maximum geometry
    #               rather than a failure.

    # CSI Ps T  Scroll down Ps lines (default = 1) (SD), VT420.
    def _CSI_T_SD(self, ps, _=None):
        t,b = self._scrollingRegion
        w,h = self._w, self._h
        #TODO: Avoid this HACK
        baseData = [' ']*w
        baseColors = [self._color]*w
        # Split the content in 3 slices [top, center, bottom]
        topd = self._canvas._data[:t]
        topc = self._canvas._colors[:t]
        centerd = self._canvas._data[t:b]
        centerc = self._canvas._colors[t:b]
        bottomd = self._canvas._data[b:]
        bottomc = self._canvas._colors[b:]
        # Rotate the center part
        centerd = [baseData.copy() for _ in range(ps)  ] + centerd
        centerc = [baseColors.copy() for _ in range(ps)] + centerc
        centerd = centerd[:b-t]
        centerc = centerc[:b-t]
        # assemble it back
        self._canvas._data   = topd + centerd + bottomd
        self._canvas._colors = topc + centerc + bottomc

    # CSI Ps ; Ps ; Ps ; Ps ; Ps T
    #           Initiate highlight mouse tracking (XTHIMOUSE), xterm.
    #           Parameters are [func;startx;starty;firstrow;lastrow].  See the
    #           section Mouse Tracking.

    # CSI > Pm T
    #           Reset title mode features to default value (XTRMTITLE), xterm.
    #           Normally, "reset" disables the feature.  It is possible to
    #           disable the ability to reset features by compiling a different
    #           default for the title modes into xterm.
    #
    #             Ps = 0  ⇒  Do not set window/icon labels using hexadecimal.
    #             Ps = 1  ⇒  Do not query window/icon labels using
    #           hexadecimal.
    #             Ps = 2  ⇒  Do not set window/icon labels using UTF-8.
    #             Ps = 3  ⇒  Do not query window/icon labels using UTF-8.
    #
    #           (See discussion of Title Modes).

    # CSI Ps X  Erase Ps Character(s) (default = 1) (ECH).
    def _CSI_X_ECH(self, ps, _):
        x,y = self._terminalCursor
        w,h = self._w, self._h
        ps = min(ps,w-x)
        self._canvas._data[y][x:x+ps]   = [' ']*ps
        self._canvas._colors[y][x:x+ps] = [self._color]*ps
        self._canvas._data[y] = self._canvas._data[y][:w]
        self._canvas._colors[y] = self._canvas._colors[y][:w]

    # CSI Ps Z  Cursor Backward Tabulation Ps tab stops (default = 1) (CBT).
    def _CSI_Z_CBT(self, ps, _): pass

    # CSI Ps ^  Scroll down Ps lines (default = 1) (SD), ECMA-48.
    #           This was a publication error in the original ECMA-48 5th
    #           edition (1991) corrected in 2003.
    def _CSI___SD(self, ps, _): pass

    # CSI Ps `  Character Position Absolute  [column] (default = [row,1])
    #           (HPA).
    def _CSI___HPA(self, ps, _): pass

    # CSI Ps a  Character Position Relative  [columns] (default = [row,col+1])
    #           (HPR).
    def _CSI_a_HPR(self, ps, _): pass

    # CSI Ps b  Repeat the preceding graphic character Ps times (REP).
    def _CSI_b_REP(self, ps, _):
        if self._last:
            self._pushTxt(self._last*ps)

    # CSI Ps c  Send Device Attributes (Primary DA).
    #             Ps = 0  or omitted ⇒  request attributes from terminal.  The
    #           response depends on the decTerminalID resource setting.
    #             ⇒  CSI ? 1 ; 2 c  ("VT100 with Advanced Video Option")
    #             ⇒  CSI ? 1 ; 0 c  ("VT101 with No Options")
    #             ⇒  CSI ? 4 ; 6 c  ("VT132 with Advanced Video and Graphics")
    #             ⇒  CSI ? 6 c  ("VT102")
    #             ⇒  CSI ? 7 c  ("VT131")
    #             ⇒  CSI ? 1 2 ; Ps c  ("VT125")
    #             ⇒  CSI ? 6 2 ; Ps c  ("VT220")
    #             ⇒  CSI ? 6 3 ; Ps c  ("VT320")
    #             ⇒  CSI ? 6 4 ; Ps c  ("VT420")
    #
    #           The VT100-style response parameters do not mean anything by
    #           themselves.  VT220 (and higher) parameters do, telling the
    #           host what features the terminal supports:
    #             Ps = 1  ⇒  132-columns.
    #             Ps = 2  ⇒  Printer.
    #             Ps = 3  ⇒  ReGIS graphics.
    #             Ps = 4  ⇒  Sixel graphics.
    #             Ps = 6  ⇒  Selective erase.
    #             Ps = 8  ⇒  User-defined keys.
    #             Ps = 9  ⇒  National Replacement Character sets.
    #             Ps = 1 5  ⇒  Technical characters.
    #             Ps = 1 6  ⇒  Locator port.
    #             Ps = 1 7  ⇒  Terminal state interrogation.
    #             Ps = 1 8  ⇒  User windows.
    #             Ps = 2 1  ⇒  Horizontal scrolling.
    #             Ps = 2 2  ⇒  ANSI color, e.g., VT525.
    #             Ps = 2 8  ⇒  Rectangular editing.
    #             Ps = 2 9  ⇒  ANSI text locator (i.e., DEC Locator mode).
    #
    #           XTerm supports part of the User windows feature, providing a
    #           single page (which corresponds to its visible window).  Rather
    #           than resizing the font to change the number of lines/columns
    #           in a fixed-size display, xterm uses the window extension
    #           controls (DECSNLS, DECSCPP, DECSLPP) to adjust its visible
    #           window's size.  The "cursor coupling" controls (DECHCCM,
    #           DECPCCM, DECVCCM) are ignored.
    def _CSI_c_Pri_DA(self, ps, _): pass

    # CSI = Ps c
    #           Send Device Attributes (Tertiary DA).
    #             Ps = 0  ⇒  report Terminal Unit ID (default), VT400.  XTerm
    #           uses zeros for the site code and serial number in its DECRPTUI
    #           response.
    # def _CSI_c_Ter_DA(self, ps, _): pass

    # CSI > Ps c
    #           Send Device Attributes (Secondary DA).
    #             Ps = 0  or omitted ⇒  request the terminal's identification
    #           code.  The response depends on the decTerminalID resource
    #           setting.  It should apply only to VT220 and up, but xterm
    #           extends this to VT100.
    #             ⇒  CSI  > Pp ; Pv ; Pc c
    #           where Pp denotes the terminal type
    #             Pp = 0  ⇒  "VT100".
    #             Pp = 1  ⇒  "VT220".
    #             Pp = 2  ⇒  "VT240" or "VT241".
    #             Pp = 1 8  ⇒  "VT330".
    #             Pp = 1 9  ⇒  "VT340".
    #             Pp = 2 4  ⇒  "VT320".
    #             Pp = 3 2  ⇒  "VT382".
    #             Pp = 4 1  ⇒  "VT420".
    #             Pp = 6 1  ⇒  "VT510".
    #             Pp = 6 4  ⇒  "VT520".
    #             Pp = 6 5  ⇒  "VT525".
    #
    #           and Pv is the firmware version (for xterm, this was originally
    #           the XFree86 patch number, starting with 95).  In a DEC
    #           terminal, Pc indicates the ROM cartridge registration number
    #           and is always zero.
    # def _CSI_c_DA(self, ps, _): pass

    # CSI Ps d  Line Position Absolute  [row] (default = [1,column]) (VPA).
    def _CSI_d_VPA(self, ps, _):
        x,y = self._terminalCursor
        w,h = self._w, self._h
        self._terminalCursor = (x,max(0,min(h-1,ps-1)))

    # CSI Ps e  Line Position Relative  [rows] (default = [row+1,column])
    #           (VPR).
    def _CSI_e_VPR(self, ps, _): pass

    # CSI Ps ; Ps f
    #           Horizontal and Vertical Position [row;column] (default =
    #           [1,1]) (HVP).
    def _CSI_f_HVP(self, row, col):
        w,h = self._w, self._h
        self._terminalCursor = (min(col-1,w-1), min(row-1,h-1))

    # CSI Ps g  Tab Clear (TBC).  ECMA-48 defines additional codes, but the
    #           VT100 user manual notes that it ignores other codes.  DEC's
    #           later terminals (and xterm) do the same, for compatibility.
    #             Ps = 0  ⇒  Clear Current Column (default).
    #             Ps = 3  ⇒  Clear All.
    def _CSI_g_TBC(self, ps, _): pass

    # CSI Pm h  Set Mode (SM).
    #             Ps = 2  ⇒  Keyboard Action Mode (KAM).
    #             Ps = 4  ⇒  Insert Mode (IRM).
    #             Ps = 1 2  ⇒  Send/receive (SRM).
    #             Ps = 2 0  ⇒  Automatic Newline (LNM).
    #             Ps = 3 4  ⇒  Normal Cursor Visibility
    def _CSI_h_SM(self, ps, _): pass

    # CSI ? Pm h
    #           DEC Private Mode Set (DECSET).
    #             Ps = 1  ⇒  Application Cursor Keys (DECCKM), VT100.
    #             Ps = 2  ⇒  Designate USASCII for character sets G0-G3
    #           (DECANM), VT100, and set VT100 mode.
    #             Ps = 3  ⇒  132 Column Mode (DECCOLM), VT100.
    #             Ps = 4  ⇒  Smooth (Slow) Scroll (DECSCLM), VT100.
    #             Ps = 5  ⇒  Reverse Video (DECSCNM), VT100.
    #             Ps = 6  ⇒  Origin Mode (DECOM), VT100.
    #             Ps = 7  ⇒  Auto-Wrap Mode (DECAWM), VT100.
    #             Ps = 8  ⇒  Auto-Repeat Keys (DECARM), VT100.
    #             Ps = 9  ⇒  Send Mouse X & Y on button press.  See the
    #           section Mouse Tracking.  This is the X10 xterm mouse protocol.
    #             Ps = 1 0  ⇒  Show toolbar (rxvt).
    #             Ps = 1 2  ⇒  Start blinking cursor (AT&T 610).
    #             Ps = 1 3  ⇒  Start blinking cursor (set only via resource or
    #           menu).
    #             Ps = 1 4  ⇒  Enable XOR of blinking cursor control sequence
    #           and menu.
    #             Ps = 1 8  ⇒  Print Form Feed (DECPFF), VT220.
    #             Ps = 1 9  ⇒  Set print extent to full screen (DECPEX),
    #           VT220.
    #             Ps = 2 5  ⇒  Show cursor (DECTCEM), VT220.
    #             Ps = 3 0  ⇒  Show scrollbar (rxvt).
    #             Ps = 3 5  ⇒  Enable font-shifting functions (rxvt).
    #             Ps = 3 8  ⇒  Enter Tektronix mode (DECTEK), VT240, xterm.
    #             Ps = 4 0  ⇒  Allow 80 ⇒  132 mode, xterm.
    #             Ps = 4 1  ⇒  more(1) fix (see curses resource).
    #             Ps = 4 2  ⇒  Enable National Replacement Character sets
    #           (DECNRCM), VT220.
    #             Ps = 4 3  ⇒  Enable Graphic Expanded Print Mode (DECGEPM),
    #           VT340.
    #             Ps = 4 4  ⇒  Turn on margin bell, xterm.
    #             Ps = 4 4  ⇒  Enable Graphic Print Color Mode (DECGPCM),
    #           VT340.
    #             Ps = 4 5  ⇒  Reverse-wraparound mode (XTREVWRAP), xterm.
    #             Ps = 4 5  ⇒  Enable Graphic Print Color Syntax (DECGPCS),
    #           VT340.
    #             Ps = 4 6  ⇒  Start logging (XTLOGGING), xterm.  This is
    #           normally disabled by a compile-time option.
    #             Ps = 4 6  ⇒  Graphic Print Background Mode, VT340.
    #             Ps = 4 7  ⇒  Use Alternate Screen Buffer, xterm.  This may
    #           be disabled by the titeInhibit resource.
    #             Ps = 4 7  ⇒  Enable Graphic Rotated Print Mode (DECGRPM),
    #           VT340.
    #             Ps = 6 6  ⇒  Application keypad mode (DECNKM), VT320.
    #             Ps = 6 7  ⇒  Backarrow key sends backspace (DECBKM), VT340,
    #           VT420.  This sets the backarrowKey resource to "true".
    #             Ps = 6 9  ⇒  Enable left and right margin mode (DECLRMM),
    #           VT420 and up.
    #             Ps = 8 0  ⇒  Enable Sixel Display Mode (DECSDM), VT330,
    #           VT340, VT382.
    #             Ps = 9 5  ⇒  Do not clear screen when DECCOLM is set/reset
    #           (DECNCSM), VT510 and up.
    #             Ps = 1 0 0 0  ⇒  Send Mouse X & Y on button press and
    #           release.  See the section Mouse Tracking.  This is the X11
    #           xterm mouse protocol.
    #             Ps = 1 0 0 1  ⇒  Use Hilite Mouse Tracking, xterm.
    #             Ps = 1 0 0 2  ⇒  Use Cell Motion Mouse Tracking, xterm.  See
    #           the section Button-event tracking.
    #             Ps = 1 0 0 3  ⇒  Use All Motion Mouse Tracking, xterm.  See
    #           the section Any-event tracking.
    #             Ps = 1 0 0 4  ⇒  Send FocusIn/FocusOut events, xterm.
    #             Ps = 1 0 0 5  ⇒  Enable UTF-8 Mouse Mode, xterm.
    #             Ps = 1 0 0 6  ⇒  Enable SGR Mouse Mode, xterm.
    #             Ps = 1 0 0 7  ⇒  Enable Alternate Scroll Mode, xterm.  This
    #           corresponds to the alternateScroll resource.
    #             Ps = 1 0 1 0  ⇒  Scroll to bottom on tty output (rxvt).
    #           This sets the scrollTtyOutput resource to "true".
    #             Ps = 1 0 1 1  ⇒  Scroll to bottom on key press (rxvt).  This
    #           sets the scrollKey resource to "true".
    #             Ps = 1 0 1 5  ⇒  Enable urxvt Mouse Mode.
    #             Ps = 1 0 1 6  ⇒  Enable SGR Mouse PixelMode, xterm.
    #             Ps = 1 0 3 4  ⇒  Interpret "meta" key, xterm.  This sets the
    #           eighth bit of keyboard input (and enables the eightBitInput
    #           resource).
    #             Ps = 1 0 3 5  ⇒  Enable special modifiers for Alt and
    #           NumLock keys, xterm.  This enables the numLock resource.
    #             Ps = 1 0 3 6  ⇒  Send ESC   when Meta modifies a key, xterm.
    #           This enables the metaSendsEscape resource.
    #             Ps = 1 0 3 7  ⇒  Send DEL from the editing-keypad Delete
    #           key, xterm.
    #             Ps = 1 0 3 9  ⇒  Send ESC  when Alt modifies a key, xterm.
    #           This enables the altSendsEscape resource, xterm.
    #             Ps = 1 0 4 0  ⇒  Keep selection even if not highlighted,
    #           xterm.  This enables the keepSelection resource.
    #             Ps = 1 0 4 1  ⇒  Use the CLIPBOARD selection, xterm.  This
    #           enables the selectToClipboard resource.
    #             Ps = 1 0 4 2  ⇒  Enable Urgency window manager hint when
    #           Control-G is received, xterm.  This enables the bellIsUrgent
    #           resource.
    #             Ps = 1 0 4 3  ⇒  Enable raising of the window when Control-G
    #           is received, xterm.  This enables the popOnBell resource.
    #             Ps = 1 0 4 4  ⇒  Reuse the most recent data copied to
    #           CLIPBOARD, xterm.  This enables the keepClipboard resource.
    #             Ps = 1 0 4 5  ⇒  Extended Reverse-wraparound mode
    #           (XTREVWRAP2), xterm.
    #             Ps = 1 0 4 6  ⇒  Enable switching to/from Alternate Screen
    #           Buffer, xterm.  This works for terminfo-based systems,
    #           updating the titeInhibit resource.
    #             Ps = 1 0 4 7  ⇒  Use Alternate Screen Buffer, xterm.  This
    #           may be disabled by the titeInhibit resource.
    #             Ps = 1 0 4 8  ⇒  Save cursor as in DECSC, xterm.  This may
    #           be disabled by the titeInhibit resource.
    #             Ps = 1 0 4 9  ⇒  Save cursor as in DECSC, xterm.  After
    #           saving the cursor, switch to the Alternate Screen Buffer,
    #           clearing it first.  This may be disabled by the titeInhibit
    #           resource.  This control combines the effects of the 1 0 4 7
    #           and 1 0 4 8  modes.  Use this with terminfo-based applications
    #           rather than the 4 7  mode.
    #             Ps = 1 0 5 0  ⇒  Set terminfo/termcap function-key mode,
    #           xterm.
    #             Ps = 1 0 5 1  ⇒  Set Sun function-key mode, xterm.
    #             Ps = 1 0 5 2  ⇒  Set HP function-key mode, xterm.
    #             Ps = 1 0 5 3  ⇒  Set SCO function-key mode, xterm.
    #             Ps = 1 0 6 0  ⇒  Set legacy keyboard emulation, i.e, X11R6,
    #           xterm.
    #             Ps = 1 0 6 1  ⇒  Set VT220 keyboard emulation, xterm.
    #             Ps = 2 0 0 1  ⇒  Enable readline mouse button-1, xterm.
    #             Ps = 2 0 0 2  ⇒  Enable readline mouse button-2, xterm.
    #             Ps = 2 0 0 3  ⇒  Enable readline mouse button-3, xterm.
    #             Ps = 2 0 0 4  ⇒  Set bracketed paste mode, xterm.
    #             Ps = 2 0 0 5  ⇒  Enable readline character-quoting, xterm.
    #             Ps = 2 0 0 6  ⇒  Enable readline newline pasting, xterm.
    # def _CSI__(self, ps, _): pass

    # CSI Ps i  Media Copy (MC).
    #             Ps = 0  ⇒  Print screen (default).
    #             Ps = 4  ⇒  Turn off printer controller mode.
    #             Ps = 5  ⇒  Turn on printer controller mode.
    #             Ps = 1 0  ⇒  HTML screen dump, xterm.
    #             Ps = 1 1  ⇒  SVG screen dump, xterm.
    def _CSI_i_MC(self, ps, _): pass

    # CSI ? Ps i
    #           Media Copy (MC), DEC-specific.
    #             Ps = 1  ⇒  Print line containing cursor.
    #             Ps = 4  ⇒  Turn off autoprint mode.
    #             Ps = 5  ⇒  Turn on autoprint mode.
    #             Ps = 1 0  ⇒  Print composed display, ignores DECPEX.
    #             Ps = 1 1  ⇒  Print all pages.
    # def _CSI__(self, ps, _): pass

    # CSI Pm l  Reset Mode (RM).
    #             Ps = 2  ⇒  Keyboard Action Mode (KAM).
    #             Ps = 4  ⇒  Replace Mode (IRM).
    #             Ps = 1 2  ⇒  Send/receive (SRM).
    #             Ps = 2 0  ⇒  Normal Linefeed (LNM).
    #             Ps = 3 4  ⇒  Normal Cursor Visibility
    def _CSI_l_RM(self, ps, _): pass

    # CSI ? Pm l
    #           DEC Private Mode Reset (DECRST).
    #             Ps = 1  ⇒  Normal Cursor Keys (DECCKM), VT100.
    #             Ps = 2  ⇒  Designate VT52 mode (DECANM), VT100.
    #             Ps = 3  ⇒  80 Column Mode (DECCOLM), VT100.
    #             Ps = 4  ⇒  Jump (Fast) Scroll (DECSCLM), VT100.
    #             Ps = 5  ⇒  Normal Video (DECSCNM), VT100.
    #             Ps = 6  ⇒  Normal Cursor Mode (DECOM), VT100.
    #             Ps = 7  ⇒  No Auto-Wrap Mode (DECAWM), VT100.
    #             Ps = 8  ⇒  No Auto-Repeat Keys (DECARM), VT100.
    #             Ps = 9  ⇒  Don't send Mouse X & Y on button press, xterm.
    #             Ps = 1 0  ⇒  Hide toolbar (rxvt).
    #             Ps = 1 2  ⇒  Stop blinking cursor (AT&T 610).
    #             Ps = 1 3  ⇒  Disable blinking cursor (reset only via
    #           resource or menu).
    #             Ps = 1 4  ⇒  Disable XOR of blinking cursor control sequence
    #           and menu.
    #             Ps = 1 8  ⇒  Don't Print Form Feed (DECPFF), VT220.
    #             Ps = 1 9  ⇒  Limit print to scrolling region (DECPEX),
    #           VT220.
    #             Ps = 2 5  ⇒  Hide cursor (DECTCEM), VT220.
    #             Ps = 3 0  ⇒  Don't show scrollbar (rxvt).
    #             Ps = 3 5  ⇒  Disable font-shifting functions (rxvt).
    #             Ps = 4 0  ⇒  Disallow 80 ⇒  132 mode, xterm.
    #             Ps = 4 1  ⇒  No more(1) fix (see curses resource).
    #             Ps = 4 2  ⇒  Disable National Replacement Character sets
    #           (DECNRCM), VT220.
    #             Ps = 4 3  ⇒  Disable Graphic Expanded Print Mode (DECGEPM),
    #           VT340.
    #             Ps = 4 4  ⇒  Turn off margin bell, xterm.
    #             Ps = 4 4  ⇒  Disable Graphic Print Color Mode (DECGPCM),
    #           VT340.
    #             Ps = 4 5  ⇒  No Reverse-wraparound mode (XTREVWRAP), xterm.
    #             Ps = 4 5  ⇒  Disable Graphic Print Color Syntax (DECGPCS),
    #           VT340.
    #             Ps = 4 6  ⇒  Stop logging (XTLOGGING), xterm.  This is
    #           normally disabled by a compile-time option.
    #             Ps = 4 7  ⇒  Use Normal Screen Buffer, xterm.
    #             Ps = 4 7  ⇒  Disable Graphic Rotated Print Mode (DECGRPM),
    #           VT340.
    #             Ps = 6 6  ⇒  Numeric keypad mode (DECNKM), VT320.
    #             Ps = 6 7  ⇒  Backarrow key sends delete (DECBKM), VT340,
    #           VT420.  This sets the backarrowKey resource to "false".
    #             Ps = 6 9  ⇒  Disable left and right margin mode (DECLRMM),
    #           VT420 and up.
    #             Ps = 8 0  ⇒  Disable Sixel Display Mode (DECSDM), VT330,
    #           VT340, VT382.  Turns on "Sixel Scrolling".  See the section
    #           Sixel Graphics and mode 8 4 5 2 .
    #             Ps = 9 5  ⇒  Clear screen when DECCOLM is set/reset
    #           (DECNCSM), VT510 and up.
    #             Ps = 1 0 0 0  ⇒  Don't send Mouse X & Y on button press and
    #           release.  See the section Mouse Tracking.
    #             Ps = 1 0 0 1  ⇒  Don't use Hilite Mouse Tracking, xterm.
    #             Ps = 1 0 0 2  ⇒  Don't use Cell Motion Mouse Tracking,
    #           xterm.  See the section Button-event tracking.
    #             Ps = 1 0 0 3  ⇒  Don't use All Motion Mouse Tracking, xterm.
    #           See the section Any-event tracking.
    #             Ps = 1 0 0 4  ⇒  Don't send FocusIn/FocusOut events, xterm.
    #             Ps = 1 0 0 5  ⇒  Disable UTF-8 Mouse Mode, xterm.
    #             Ps = 1 0 0 6  ⇒  Disable SGR Mouse Mode, xterm.
    #             Ps = 1 0 0 7  ⇒  Disable Alternate Scroll Mode, xterm.  This
    #           corresponds to the alternateScroll resource.
    #             Ps = 1 0 1 0  ⇒  Don't scroll to bottom on tty output
    #           (rxvt).  This sets the scrollTtyOutput resource to "false".
    #             Ps = 1 0 1 1  ⇒  Don't scroll to bottom on key press (rxvt).
    #           This sets the scrollKey resource to "false".
    #             Ps = 1 0 1 5  ⇒  Disable urxvt Mouse Mode.
    #             Ps = 1 0 1 6  ⇒  Disable SGR Mouse Pixel-Mode, xterm.
    #             Ps = 1 0 3 4  ⇒  Don't interpret "meta" key, xterm.  This
    #           disables the eightBitInput resource.
    #             Ps = 1 0 3 5  ⇒  Disable special modifiers for Alt and
    #           NumLock keys, xterm.  This disables the numLock resource.
    #             Ps = 1 0 3 6  ⇒  Don't send ESC  when Meta modifies a key,
    #           xterm.  This disables the metaSendsEscape resource.
    #             Ps = 1 0 3 7  ⇒  Send VT220 Remove from the editing-keypad
    #           Delete key, xterm.
    #             Ps = 1 0 3 9  ⇒  Don't send ESC when Alt modifies a key,
    #           xterm.  This disables the altSendsEscape resource.
    #             Ps = 1 0 4 0  ⇒  Do not keep selection when not highlighted,
    #           xterm.  This disables the keepSelection resource.
    #             Ps = 1 0 4 1  ⇒  Use the PRIMARY selection, xterm.  This
    #           disables the selectToClipboard resource.
    #             Ps = 1 0 4 2  ⇒  Disable Urgency window manager hint when
    #           Control-G is received, xterm.  This disables the bellIsUrgent
    #           resource.
    #             Ps = 1 0 4 3  ⇒  Disable raising of the window when Control-
    #           G is received, xterm.  This disables the popOnBell resource.
    #             Ps = 1 0 4 5  ⇒  No Extended Reverse-wraparound mode
    #           (XTREVWRAP2), xterm.
    #             Ps = 1 0 4 6  ⇒  Disable switching to/from Alternate Screen
    #           Buffer, xterm.  This works for terminfo-based systems,
    #           updating the titeInhibit resource.  If currently using the
    #           Alternate Screen Buffer, xterm switches to the Normal Screen
    #           Buffer.
    #             Ps = 1 0 4 7  ⇒  Use Normal Screen Buffer, xterm.  Clear the
    #           screen first if in the Alternate Screen Buffer.  This may be
    #           disabled by the titeInhibit resource.
    #             Ps = 1 0 4 8  ⇒  Restore cursor as in DECRC, xterm.  This
    #           may be disabled by the titeInhibit resource.
    #             Ps = 1 0 4 9  ⇒  Use Normal Screen Buffer and restore cursor
    #           as in DECRC, xterm.  This may be disabled by the titeInhibit
    #           resource.  This combines the effects of the 1 0 4 7  and 1 0 4
    #           8  modes.  Use this with terminfo-based applications rather
    #           than the 4 7  mode.
    #             Ps = 1 0 5 0  ⇒  Reset terminfo/termcap function-key mode,
    #           xterm.
    #             Ps = 1 0 5 1  ⇒  Reset Sun function-key mode, xterm.
    #             Ps = 1 0 5 2  ⇒  Reset HP function-key mode, xterm.
    #             Ps = 1 0 5 3  ⇒  Reset SCO function-key mode, xterm.
    #             Ps = 1 0 6 0  ⇒  Reset legacy keyboard emulation, i.e,
    #           X11R6, xterm.
    #             Ps = 1 0 6 1  ⇒  Reset keyboard emulation to Sun/PC style,
    #           xterm.
    #             Ps = 2 0 0 1  ⇒  Disable readline mouse button-1, xterm.
    #             Ps = 2 0 0 2  ⇒  Disable readline mouse button-2, xterm.
    #             Ps = 2 0 0 3  ⇒  Disable readline mouse button-3, xterm.
    #             Ps = 2 0 0 4  ⇒  Reset bracketed paste mode, xterm.
    #             Ps = 2 0 0 5  ⇒  Disable readline character-quoting, xterm.
    #             Ps = 2 0 0 6  ⇒  Disable readline newline pasting, xterm.
    # def _CSI__(self, ps, _): pass

    # CSI Pm m  Character Attributes (SGR).
    #             Ps = 0  ⇒  Normal (default), VT100.
    #             Ps = 1  ⇒  Bold, VT100.
    #             Ps = 2  ⇒  Faint, decreased intensity, ECMA-48 2nd.
    #             Ps = 3  ⇒  Italicized, ECMA-48 2nd.
    #             Ps = 4  ⇒  Underlined, VT100.
    #             Ps = 5  ⇒  Blink, VT100.
    #           This appears as Bold in X11R6 xterm.
    #             Ps = 7  ⇒  Inverse, VT100.
    #             Ps = 8  ⇒  Invisible, i.e., hidden, ECMA-48 2nd, VT300.
    #             Ps = 9  ⇒  Crossed-out characters, ECMA-48 3rd.
    #             Ps = 2 1  ⇒  Doubly-underlined, ECMA-48 3rd.
    #             Ps = 2 2  ⇒  Normal (neither bold nor faint), ECMA-48 3rd.
    #             Ps = 2 3  ⇒  Not italicized, ECMA-48 3rd.
    #             Ps = 2 4  ⇒  Not underlined, ECMA-48 3rd.
    #             Ps = 2 5  ⇒  Steady (not blinking), ECMA-48 3rd.
    #             Ps = 2 7  ⇒  Positive (not inverse), ECMA-48 3rd.
    #             Ps = 2 8  ⇒  Visible, i.e., not hidden, ECMA-48 3rd, VT300.
    #             Ps = 2 9  ⇒  Not crossed-out, ECMA-48 3rd.
    #             Ps = 3 0  ⇒  Set foreground color to Black.
    #             Ps = 3 1  ⇒  Set foreground color to Red.
    #             Ps = 3 2  ⇒  Set foreground color to Green.
    #             Ps = 3 3  ⇒  Set foreground color to Yellow.
    #             Ps = 3 4  ⇒  Set foreground color to Blue.
    #             Ps = 3 5  ⇒  Set foreground color to Magenta.
    #             Ps = 3 6  ⇒  Set foreground color to Cyan.
    #             Ps = 3 7  ⇒  Set foreground color to White.
    #             Ps = 3 9  ⇒  Set foreground color to default, ECMA-48 3rd.
    #             Ps = 4 0  ⇒  Set background color to Black.
    #             Ps = 4 1  ⇒  Set background color to Red.
    #             Ps = 4 2  ⇒  Set background color to Green.
    #             Ps = 4 3  ⇒  Set background color to Yellow.
    #             Ps = 4 4  ⇒  Set background color to Blue.
    #             Ps = 4 5  ⇒  Set background color to Magenta.
    #             Ps = 4 6  ⇒  Set background color to Cyan.
    #             Ps = 4 7  ⇒  Set background color to White.
    #             Ps = 4 9  ⇒  Set background color to default, ECMA-48 3rd.
    #
    #           Some of the above note the edition of ECMA-48 which first
    #           describes a feature.  In its successive editions from 1979 to
    #           1991 (2nd 1979, 3rd 1984, 4th 1986, and 5th 1991), ECMA-48
    #           listed codes through 6 5 (skipping several toward the end of
    #           the range).  Most of the ECMA-48 codes not implemented in
    #           xterm were never implemented in a hardware terminal.  Several
    #           (such as 3 9  and 4 9 ) are either noted in ECMA-48 as
    #           implementation defined, or described in vague terms.
    #
    #           The successive editions of ECMA-48 give little attention to
    #           changes from one edition to the next, except to comment on
    #           features which have become obsolete.  ECMA-48 1st (1976) is
    #           unavailable; there is no reliable source of information which
    #           states whether "ANSI" color was defined in that edition, or
    #           later (1979).  The VT100 (1978) implemented the most commonly
    #           used non-color video attributes which are given in the 2nd
    #           edition.
    #
    #           While 8-color support is described in ECMA-48 2nd edition, the
    #           VT500 series (introduced in 1993) were the first DEC terminals
    #           implementing "ANSI" color.  The DEC terminal's use of color is
    #           known to differ from xterm; useful documentation on this
    #           series became available too late to influence xterm.
    #
    #           If 16-color support is compiled, the following aixterm
    #           controls apply.  Assume that xterm's resources are set so that
    #           the ISO color codes are the first 8 of a set of 16.  Then the
    #           aixterm colors are the bright versions of the ISO colors:
    #
    #             Ps = 9 0  ⇒  Set foreground color to Black.
    #             Ps = 9 1  ⇒  Set foreground color to Red.
    #             Ps = 9 2  ⇒  Set foreground color to Green.
    #             Ps = 9 3  ⇒  Set foreground color to Yellow.
    #             Ps = 9 4  ⇒  Set foreground color to Blue.
    #             Ps = 9 5  ⇒  Set foreground color to Magenta.
    #             Ps = 9 6  ⇒  Set foreground color to Cyan.
    #             Ps = 9 7  ⇒  Set foreground color to White.
    #             Ps = 1 0 0  ⇒  Set background color to Black.
    #             Ps = 1 0 1  ⇒  Set background color to Red.
    #             Ps = 1 0 2  ⇒  Set background color to Green.
    #             Ps = 1 0 3  ⇒  Set background color to Yellow.
    #             Ps = 1 0 4  ⇒  Set background color to Blue.
    #             Ps = 1 0 5  ⇒  Set background color to Magenta.
    #             Ps = 1 0 6  ⇒  Set background color to Cyan.
    #             Ps = 1 0 7  ⇒  Set background color to White.
    #
    #           If xterm is compiled with the 16-color support disabled, it
    #           supports the following, from rxvt:
    #             Ps = 1 0 0  ⇒  Set foreground and background color to
    #           default.
    #
    #           XTerm maintains a color palette whose entries are identified
    #           by an index beginning with zero.  If 88- or 256-color support
    #           is compiled, the following apply:
    #           o   All parameters are decimal integers.
    #           o   RGB values range from zero (0) to 255.
    #           o   The 88- and 256-color support uses subparameters described
    #               in ISO-8613-6 for indexed color.  ISO-8613-6 also mentions
    #               direct color, using a similar scheme.  xterm supports
    #               that, too.
    #           o   xterm allows either colons (standard) or semicolons
    #               (legacy) to separate the subparameters (but after the
    #               first colon, colons must be used).
    #
    #           The indexed- and direct-color features are summarized in the
    #           FAQ, which explains why semicolon is accepted as a
    #           subparameter delimiter:
    #
    #             Can I set a color by its number?
    #
    #           These ISO-8613-6 controls (marked in ECMA-48 5th edition as
    #           "reserved for future standardization") are supported by xterm:
    #             Ps = 3 8 : 2 : Pi : Pr : Pg : Pb ⇒  Set foreground color
    #           using RGB values.  If xterm is not compiled with direct-color
    #           support, it uses the closest match in its palette for the
    #           given RGB Pr/Pg/Pb.  The color space identifier Pi is ignored.
    #             Ps = 3 8 : 5 : Ps ⇒  Set foreground color to Ps, using
    #           indexed color.
    #             Ps = 4 8 : 2 : Pi : Pr : Pg : Pb ⇒  Set background color
    #           using RGB values.  If xterm is not compiled with direct-color
    #           support, it uses the closest match in its palette for the
    #           given RGB Pr/Pg/Pb.  The color space identifier Pi is ignored.
    #             Ps = 4 8 : 5 : Ps ⇒  Set background color to Ps, using
    #           indexed color.
    #
    #           This variation on ISO-8613-6 is supported for compatibility
    #           with KDE konsole:
    #             Ps = 3 8 ; 2 ; Pr ; Pg ; Pb ⇒  Set foreground color using
    #           RGB values.  If xterm is not compiled with direct-color
    #           support, it uses the closest match in its palette for the
    #           given RGB Pr/Pg/Pb.
    #             Ps = 4 8 ; 2 ; Pr ; Pg ; Pb ⇒  Set background color using
    #           RGB values.  If xterm is not compiled with direct-color
    #           support, it uses the closest match in its palette for the
    #           given RGB Pr/Pg/Pb.
    #
    #           In each case, if xterm is compiled with direct-color support,
    #           and the resource directColor is true, then rather than
    #           choosing the closest match, xterm asks the X server to
    #           directly render a given color.
    def _CSI_m_SGR(self, ps, _): pass

    # CSI > Pp ; Pv m
    # def _CSI__(self, ps, _): pass
    # CSI > Pp m
    #           Set/reset key modifier options (XTMODKEYS), xterm.  Set or
    #           reset resource-values used by xterm to decide whether to
    #           construct escape sequences holding information about the
    #           modifiers pressed with a given key.
    #
    #           The first parameter Pp identifies the resource to set/reset.
    #           The second parameter Pv is the value to assign to the
    #           resource.
    #
    #           If the second parameter is omitted, the resource is reset to
    #           its initial value.  Values 3  and 5  are reserved for keypad-
    #           keys and string-keys.
    #
    #             Pp = 0  ⇒  modifyKeyboard.
    #             Pp = 1  ⇒  modifyCursorKeys.
    #             Pp = 2  ⇒  modifyFunctionKeys.
    #             Pp = 4  ⇒  modifyOtherKeys.
    #
    #           If no parameters are given, all resources are reset to their
    #           initial values.
    # def _CSI__(self, ps, _): pass

    # CSI ? Pp m
    #           Query key modifier options (XTQMODKEYS), xterm.
    #
    #           The parameter Pp identifies the resource to query.
    #
    #             Pp = 0  ⇒  modifyKeyboard.
    #             Pp = 1  ⇒  modifyCursorKeys.
    #             Pp = 2  ⇒  modifyFunctionKeys.
    #             Pp = 4  ⇒  modifyOtherKeys.
    #
    #           XTerm's response can be used to restore this state, because it
    #           is formatted as an XTMODKEYS control, i.e.,
    #
    #             CSI > Pp m
    #
    #           where
    #
    #             Pp = 0  ⇒  modifyKeyboard.
    #             Pp = 1  ⇒  modifyCursorKeys.
    #             Pp = 2  ⇒  modifyFunctionKeys.
    #             Pp = 4  ⇒  modifyOtherKeys.

    # CSI Ps n  Device Status Report (DSR).
    #             Ps = 5  ⇒  Status Report.
    #           Result ("OK") is CSI 0 n
    #             Ps = 6  ⇒  Report Cursor Position (CPR) [row;column].
    #           Result is CSI r ; c R
    #
    #           Note: it is possible for this sequence to be sent by a
    #           function key.  For example, with the default keyboard
    #           configuration the shifted F1 key may send (with shift-,
    #           control-, alt-modifiers)
    #
    #             CSI 1 ; 2  R , or
    #             CSI 1 ; 5  R , or
    #             CSI 1 ; 6  R , etc.
    #
    #           The second parameter encodes the modifiers; values range from
    #           2 to 16.  See the section PC-Style Function Keys for the
    #           codes.  The modifyFunctionKeys and modifyKeyboard resources
    #           can change the form of the string sent from the modified F1
    #           key.
    # def _CSI_n_DSR(self, ps, _): pass

    # CSI > Ps n
    #           Disable key modifier options, xterm.  These modifiers may be
    #           enabled via the CSI > Pm m sequence.  This control sequence
    #           corresponds to a resource value of "-1", which cannot be set
    #           with the other sequence.
    #
    #           The parameter identifies the resource to be disabled:
    #
    #             Ps = 0  ⇒  modifyKeyboard.
    #             Ps = 1  ⇒  modifyCursorKeys.
    #             Ps = 2  ⇒  modifyFunctionKeys.
    #             Ps = 4  ⇒  modifyOtherKeys.
    #
    #           If the parameter is omitted, modifyFunctionKeys is disabled.
    #           When modifyFunctionKeys is disabled, xterm uses the modifier
    #           keys to make an extended sequence of function keys rather than
    #           adding a parameter to each function key to denote the
    #           modifiers.

    # CSI ? Ps n
    #           Device Status Report (DSR, DEC-specific).
    #             Ps = 6  ⇒  Report Cursor Position (DECXCPR).  The response
    #           [row;column] is returned as
    #           CSI ? r ; c R
    #           (assumes the default page, i.e., "1").
    #             Ps = 1 5  ⇒  Report Printer status.  The response is
    #           CSI ? 1 0 n  (ready).  or
    #           CSI ? 1 1 n  (not ready).
    #             Ps = 2 5  ⇒  Report UDK status.  The response is
    #           CSI ? 2 0 n  (unlocked)
    #           or
    #           CSI ? 2 1 n  (locked).
    #             Ps = 2 6  ⇒  Report Keyboard status.  The response is
    #           CSI ? 2 7 ; 1 ; 0 ; 0 n  (North American).
    #
    #           The last two parameters apply to VT300 & up (keyboard ready)
    #           and VT400 & up (LK01) respectively.
    #
    #             Ps = 5 3  ⇒  Report Locator status.  The response is CSI ? 5
    #           3 n  Locator available, if compiled-in, or CSI ? 5 0 n  No
    #           Locator, if not.
    #             Ps = 5 5  ⇒  Report Locator status.  The response is CSI ? 5
    #           3 n  Locator available, if compiled-in, or CSI ? 5 0 n  No
    #           Locator, if not.
    #             Ps = 5 6  ⇒  Report Locator type.  The response is CSI ? 5 7
    #           ; 1 n  Mouse, if compiled-in, or CSI ? 5 7 ; 0 n  Cannot
    #           identify, if not.
    #             Ps = 6 2  ⇒  Report macro space (DECMSR).  The response is
    #           CSI Pn *  { .
    #             Ps = 6 3  ⇒  Report memory checksum (DECCKSR), VT420 and up.
    #           The response is DCS Pt ! ~ x x x x ST .
    #               Pt is the request id (from an optional parameter to the
    #           request).
    #               The x's are hexadecimal digits 0-9 and A-F.
    #             Ps = 7 5  ⇒  Report data integrity.  The response is CSI ? 7
    #           0 n  (ready, no errors).
    #             Ps = 8 5  ⇒  Report multi-session configuration.  The
    #           response is CSI ? 8 3 n  (not configured for multiple-session
    #           operation).

    # CSI > Ps p
    #           Set resource value pointerMode (XTSMPOINTER), xterm.  This is
    #           used by xterm to decide whether to hide the pointer cursor as
    #           the user types.
    #
    #           Valid values for the parameter:
    #             Ps = 0  ⇒  never hide the pointer.
    #             Ps = 1  ⇒  hide if the mouse tracking mode is not enabled.
    #             Ps = 2  ⇒  always hide the pointer, except when leaving the
    #           window.
    #             Ps = 3  ⇒  always hide the pointer, even if leaving/entering
    #           the window.
    #
    #           If no parameter is given, xterm uses the default, which is 1 .

    # CSI ! p   Soft terminal reset (DECSTR), VT220 and up.

    # CSI Pl ; Pc " p
    #           Set conformance level (DECSCL), VT220 and up.
    #
    #           The first parameter selects the conformance level.  Valid
    #           values are:
    #             Pl = 6 1  ⇒  level 1, e.g., VT100.
    #             Pl = 6 2  ⇒  level 2, e.g., VT200.
    #             Pl = 6 3  ⇒  level 3, e.g., VT300.
    #             Pl = 6 4  ⇒  level 4, e.g., VT400.
    #             Pl = 6 5  ⇒  level 5, e.g., VT500.
    #
    #           The second parameter selects the C1 control transmission mode.
    #           This is an optional parameter, ignored in conformance level 1.
    #           Valid values are:
    #             Pc = 0  ⇒  8-bit controls.
    #             Pc = 1  ⇒  7-bit controls (DEC factory default).
    #             Pc = 2  ⇒  8-bit controls.
    #
    #           The 7-bit and 8-bit control modes can also be set by S7C1T and
    #           S8C1T, but DECSCL is preferred.

    # CSI Ps $ p
    #           Request ANSI mode (DECRQM).  For VT300 and up, reply DECRPM is
    #             CSI Ps; Pm $ y
    #           where Ps is the mode number as in SM/RM, and Pm is the mode
    #           value:
    #             0 - not recognized
    #             1 - set
    #             2 - reset
    #             3 - permanently set
    #             4 - permanently reset

    # CSI ? Ps $ p
    #           Request DEC private mode (DECRQM).  For VT300 and up, reply
    #           DECRPM is
    #             CSI ? Ps; Pm $ y
    #           where Ps is the mode number as in DECSET/DECSET, Pm is the
    #           mode value as in the ANSI DECRQM.
    #           Two private modes are read-only (i.e., 1 3  and 1 4 ),
    #           provided only for reporting their values using this control
    #           sequence.  They correspond to the resources cursorBlink and
    #           cursorBlinkXOR.

    # CSI # p

    # CSI Pm # p
    #           Push video attributes onto stack (XTPUSHSGR), xterm.  This is
    #           an alias for CSI # { , used to work around language
    #           limitations of C#.

    # CSI > Ps q
    #           Ps = 0  ⇒  Report xterm name and version (XTVERSION).  The
    #           response is a DSR sequence identifying the version: DCS > |
    #           text ST

    # CSI Ps q  Load LEDs (DECLL), VT100.
    #             Ps = 0  ⇒  Clear all LEDS (default).
    #             Ps = 1  ⇒  Light Num Lock.
    #             Ps = 2  ⇒  Light Caps Lock.
    #             Ps = 3  ⇒  Light Scroll Lock.
    #             Ps = 2 1  ⇒  Extinguish Num Lock.
    #             Ps = 2 2  ⇒  Extinguish Caps Lock.
    #             Ps = 2 3  ⇒  Extinguish Scroll Lock.
    def _CSI_q_DECLL(self, ps, _): pass

    # CSI Ps SP q
    #           Set cursor style (DECSCUSR), VT520.
    #             Ps = 0  ⇒  blinking block.
    #             Ps = 1  ⇒  blinking block (default).
    #             Ps = 2  ⇒  steady block.
    #             Ps = 3  ⇒  blinking underline.
    #             Ps = 4  ⇒  steady underline.
    #             Ps = 5  ⇒  blinking bar, xterm.
    #             Ps = 6  ⇒  steady bar, xterm.

    # CSI Ps " q
    #           Select character protection attribute (DECSCA), VT220.  Valid
    #           values for the parameter:
    #             Ps = 0  ⇒  DECSED and DECSEL can erase (default).
    #             Ps = 1  ⇒  DECSED and DECSEL cannot erase.
    #             Ps = 2  ⇒  DECSED and DECSEL can erase.

    # CSI # q   Pop video attributes from stack (XTPOPSGR), xterm.  This is an
    #           alias for CSI # } , used to work around language limitations
    #           of C#.

    # CSI Ps ; Ps r
    #           Set Scrolling Region [top;bottom] (default = full size of
    #           window) (DECSTBM), VT100.
    def _CSI_r_DECSTBM(self, top, bottom):
        self._scrollingRegion = (top-1, bottom)

    # CSI ? Pm r
    #           Restore DEC Private Mode Values (XTRESTORE), xterm.  The value
    #           of Ps previously saved is restored.  Ps values are the same as
    #           for DECSET.
    #
    #           Like Restore Cursor (DECRC), this uses a one-level cache.
    #           Unlike Restore Cursor, specific settings can be saved and
    #           restored independently.  Only those modes listed as parameters
    #           are restored.

    # CSI Pt ; Pl ; Pb ; Pr ; Pm $ r
    #           Change Attributes in Rectangular Area (DECCARA), VT400 and up.
    #             Pt ; Pl ; Pb ; Pr denotes the rectangle.
    #             Pm denotes the SGR attributes to change: 0, 1, 4, 5, 7.

    # CSI s     Save cursor, available only when DECLRMM is disabled (SCOSC,
    #           also ANSI.SYS).
    def _CSI_s_SCOSC(self, _, __): pass

    # CSI Pl ; Pr s
    #           Set left and right margins (DECSLRM), VT420 and up.  This is
    #           available only when DECLRMM is enabled.

    # CSI > Ps s
    #           Set/reset shift-escape options (XTSHIFTESCAPE), xterm.  This
    #           corresponds to the shiftEscape resource.
    #
    #           Valid values for the parameter:
    #             Ps = 0  ⇒  allow shift-key to override mouse protocol.
    #             Ps = 1  ⇒  conditionally allow shift-key as modifier in
    #           mouse protocol.
    #
    #           These resource values are disallowed in the control sequence:
    #             Ps = 2  ⇒  always allow shift-key as modifier in mouse
    #           protocol.
    #             Ps = 3  ⇒  never allow shift-key as modifier in mouse
    #           protocol.
    #
    #           If no parameter is given, xterm uses the default, which is 0 .

    # CSI ? Pm s
    #           Save DEC Private Mode Values (XTSAVE), xterm.  Ps values are
    #           the same as for DECSET.
    #
    #           Like Save Cursor (DECSC), this uses a one-level cache.  Unlike
    #           Save Cursor, specific settings can be saved and restored
    #           independently.  Only those modes listed as parameters are
    #           saved.

    # CSI Ps ; Ps ; Ps t
    #           Window manipulation (XTWINOPS), dtterm, extended by xterm.
    #           These controls may be disabled using the allowWindowOps
    #           resource.
    #
    #           xterm uses Extended Window Manager Hints (EWMH) to maximize
    #           the window.  Some window managers have incomplete support for
    #           EWMH.  For instance, fvwm, flwm and quartz-wm advertise
    #           support for maximizing windows horizontally or vertically, but
    #           in fact equate those to the maximize operation.
    #
    #           Valid values for the first (and any additional parameters)
    #           are:
    #             Ps = 1  ⇒  De-iconify window.
    #             Ps = 2  ⇒  Iconify window.
    #             Ps = 3 ;  x ;  y ⇒  Move window to [x, y].
    #             Ps = 4 ;  height ;  width ⇒  Resize the xterm window to
    #           given height and width in pixels.  Omitted parameters reuse
    #           the current height or width.  Zero parameters use the
    #           display's height or width.
    #             Ps = 5  ⇒  Raise the xterm window to the front of the
    #           stacking order.
    #             Ps = 6  ⇒  Lower the xterm window to the bottom of the
    #           stacking order.
    #             Ps = 7  ⇒  Refresh the xterm window.
    #             Ps = 8 ;  height ;  width ⇒  Resize the text area to given
    #           height and width in characters.  Omitted parameters reuse the
    #           current height or width.  Zero parameters use the display's
    #           height or width.
    #             Ps = 9 ;  0  ⇒  Restore maximized window.
    #             Ps = 9 ;  1  ⇒  Maximize window (i.e., resize to screen
    #           size).
    #             Ps = 9 ;  2  ⇒  Maximize window vertically.
    #             Ps = 9 ;  3  ⇒  Maximize window horizontally.
    #             Ps = 1 0 ;  0  ⇒  Undo full-screen mode.
    #             Ps = 1 0 ;  1  ⇒  Change to full-screen.
    #             Ps = 1 0 ;  2  ⇒  Toggle full-screen.
    #             Ps = 1 1  ⇒  Report xterm window state.
    #           If the xterm window is non-iconified, it returns CSI 1 t .
    #           If the xterm window is iconified, it returns CSI 2 t .
    #             Ps = 1 3  ⇒  Report xterm window position.
    #           Note: X Toolkit positions can be negative, but the reported
    #           values are unsigned, in the range 0-65535.  Negative values
    #           correspond to 32768-65535.
    #           Result is CSI 3 ; x ; y t
    #             Ps = 1 3 ;  2  ⇒  Report xterm text-area position.
    #           Result is CSI 3 ; x ; y t
    #             Ps = 1 4  ⇒  Report xterm text area size in pixels.
    #           Result is CSI  4 ;  height ;  width t
    #             Ps = 1 4 ;  2  ⇒  Report xterm window size in pixels.
    #           Normally xterm's window is larger than its text area, since it
    #           includes the frame (or decoration) applied by the window
    #           manager, as well as the area used by a scroll-bar.
    #           Result is CSI  4 ;  height ;  width t
    #             Ps = 1 5  ⇒  Report size of the screen in pixels.
    #           Result is CSI  5 ;  height ;  width t
    #             Ps = 1 6  ⇒  Report xterm character cell size in pixels.
    #           Result is CSI  6 ;  height ;  width t
    #             Ps = 1 8  ⇒  Report the size of the text area in characters.
    #           Result is CSI  8 ;  height ;  width t
    #             Ps = 1 9  ⇒  Report the size of the screen in characters.
    #           Result is CSI  9 ;  height ;  width t
    #             Ps = 2 0  ⇒  Report xterm window's icon label.
    #           Result is OSC  L  label ST
    #             Ps = 2 1  ⇒  Report xterm window's title.
    #           Result is OSC  l  label ST
    #             Ps = 2 2 ; 0  ⇒  Save xterm icon and window title on stack.
    #             Ps = 2 2 ; 1  ⇒  Save xterm icon title on stack.
    #             Ps = 2 2 ; 2  ⇒  Save xterm window title on stack.
    #             Ps = 2 3 ; 0  ⇒  Restore xterm icon and window title from
    #           stack.
    #             Ps = 2 3 ; 1  ⇒  Restore xterm icon title from stack.
    #             Ps = 2 3 ; 2  ⇒  Restore xterm window title from stack.
    #             Ps >= 2 4  ⇒  Resize to Ps lines (DECSLPP), VT340 and VT420.
    #           xterm adapts this by resizing its window.

    # CSI > Pm t
    #           This xterm control sets one or more features of the title
    #           modes (XTSMTITLE), xterm.  Each parameter enables a single
    #           feature.
    #             Ps = 0  ⇒  Set window/icon labels using hexadecimal.
    #             Ps = 1  ⇒  Query window/icon labels using hexadecimal.
    #             Ps = 2  ⇒  Set window/icon labels using UTF-8.
    #             Ps = 3  ⇒  Query window/icon labels using UTF-8.  (See
    #           discussion of Title Modes)

    # CSI Ps SP t
    #           Set warning-bell volume (DECSWBV), VT520.
    #             Ps = 0  or 1  ⇒  off.
    #             Ps = 2 , 3  or 4  ⇒  low.
    #             Ps = 5 , 6 , 7 , or 8  ⇒  high.

    # CSI Pt ; Pl ; Pb ; Pr ; Pm $ t
    #           Reverse Attributes in Rectangular Area (DECRARA), VT400 and
    #           up.
    #             Pt ; Pl ; Pb ; Pr denotes the rectangle.
    #             Pm denotes the attributes to reverse, i.e.,  1, 4, 5, 7.

    # CSI u     Restore cursor (SCORC, also ANSI.SYS).
    def _CSI_u_SCORC(self, _, __): pass

    # CSI Ps SP u
    #           Set margin-bell volume (DECSMBV), VT520.
    #             Ps = 0 , 5 , 6 , 7 , or 8  ⇒  high.
    #             Ps = 1  ⇒  off.
    #             Ps = 2 , 3  or 4  ⇒  low.

    # CSI Pt ; Pl ; Pb ; Pr ; Pp ; Pt ; Pl ; Pp $ v
    #           Copy Rectangular Area (DECCRA), VT400 and up.
    #             Pt ; Pl ; Pb ; Pr denotes the rectangle.
    #             Pp denotes the source page.
    #             Pt ; Pl denotes the target location.
    #             Pp denotes the target page.

    # CSI Ps $ w
    #           Request presentation state report (DECRQPSR), VT320 and up.
    #             Ps = 0  ⇒  error.
    #             Ps = 1  ⇒  cursor information report (DECCIR).
    #           Response is
    #             DCS 1 $ u Pt ST
    #           Refer to the VT420 programming manual, which requires six
    #           pages to document the data string Pt,
    #             Ps = 2  ⇒  tab stop report (DECTABSR).
    #           Response is
    #             DCS 2 $ u Pt ST
    #           The data string Pt is a list of the tab-stops, separated by
    #           "/" characters.

    # CSI Pt ; Pl ; Pb ; Pr ' w
    #           Enable Filter Rectangle (DECEFR), VT420 and up.
    #           Parameters are [top;left;bottom;right].
    #           Defines the coordinates of a filter rectangle and activates
    #           it.  Anytime the locator is detected outside of the filter
    #           rectangle, an outside rectangle event is generated and the
    #           rectangle is disabled.  Filter rectangles are always treated
    #           as "one-shot" events.  Any parameters that are omitted default
    #           to the current locator position.  If all parameters are
    #           omitted, any locator motion will be reported.  DECELR always
    #           cancels any previous rectangle definition.

    # CSI Ps x  Request Terminal Parameters (DECREQTPARM).
    #           if Ps is a "0" (default) or "1", and xterm is emulating VT100,
    #           the control sequence elicits a response of the same form whose
    #           parameters describe the terminal:
    #             Ps ⇒  the given Ps incremented by 2.
    #             Pn = 1  ⇐  no parity.
    #             Pn = 1  ⇐  eight bits.
    #             Pn = 1  ⇐  2 8  transmit 38.4k baud.
    #             Pn = 1  ⇐  2 8  receive 38.4k baud.
    #             Pn = 1  ⇐  clock multiplier.
    #             Pn = 0  ⇐  STP flags.
    def _CSI_x_DECREQTPARM(self, x, __): pass

    # CSI Ps * x
    #           Select Attribute Change Extent (DECSACE), VT420 and up.
    #             Ps = 0  ⇒  from start to end position, wrapped.
    #             Ps = 1  ⇒  from start to end position, wrapped.
    #             Ps = 2  ⇒  rectangle (exact).

    # CSI Pc ; Pt ; Pl ; Pb ; Pr $ x
    #           Fill Rectangular Area (DECFRA), VT420 and up.
    #             Pc is the character to use.
    #             Pt ; Pl ; Pb ; Pr denotes the rectangle.

    # CSI Ps # y
    #           Select checksum extension (XTCHECKSUM), xterm.  The bits of Ps
    #           modify the calculation of the checksum returned by DECRQCRA:
    #             0  ⇒  do not negate the result.
    #             1  ⇒  do not report the VT100 video attributes.
    #             2  ⇒  do not omit checksum for blanks.
    #             3  ⇒  omit checksum for cells not explicitly initialized.
    #             4  ⇒  do not mask cell value to 8 bits or ignore combining
    #           characters.
    #             5  ⇒  do not mask cell value to 7 bits.

    # CSI Pi ; Pg ; Pt ; Pl ; Pb ; Pr * y
    #           Request Checksum of Rectangular Area (DECRQCRA), VT420 and up.
    #           Response is
    #           DCS Pi ! ~ x x x x ST
    #             Pi is the request id.
    #             Pg is the page number.
    #             Pt ; Pl ; Pb ; Pr denotes the rectangle.
    #             The x's are hexadecimal digits 0-9 and A-F.

    # CSI Ps ; Pu ' z
    #           Enable Locator Reporting (DECELR).
    #           Valid values for the first parameter:
    #             Ps = 0  ⇒  Locator disabled (default).
    #             Ps = 1  ⇒  Locator enabled.
    #             Ps = 2  ⇒  Locator enabled for one report, then disabled.
    #           The second parameter specifies the coordinate unit for locator
    #           reports.
    #           Valid values for the second parameter:
    #             Pu = 0  or omitted ⇒  default to character cells.
    #             Pu = 1  ⇐  device physical pixels.
    #             Pu = 2  ⇐  character cells.

    # CSI Pt ; Pl ; Pb ; Pr $ z
    #           Erase Rectangular Area (DECERA), VT400 and up.
    #             Pt ; Pl ; Pb ; Pr denotes the rectangle.

    # CSI Pm ' {
    #           Select Locator Events (DECSLE).
    #           Valid values for the first (and any additional parameters)
    #           are:
    #             Ps = 0  ⇒  only respond to explicit host requests (DECRQLP).
    #           This is default.  It also cancels any filter rectangle.
    #             Ps = 1  ⇒  report button down transitions.
    #             Ps = 2  ⇒  do not report button down transitions.
    #             Ps = 3  ⇒  report button up transitions.
    #             Ps = 4  ⇒  do not report button up transitions.

    # CSI # {
    # CSI Pm # {
    #           Push video attributes onto stack (XTPUSHSGR), xterm.  The
    #           optional parameters correspond to the SGR encoding for video
    #           attributes, except for colors (which do not have a unique SGR
    #           code):
    #             Ps = 1  ⇒  Bold.
    #             Ps = 2  ⇒  Faint.
    #             Ps = 3  ⇒  Italicized.
    #             Ps = 4  ⇒  Underlined.
    #             Ps = 5  ⇒  Blink.
    #             Ps = 7  ⇒  Inverse.
    #             Ps = 8  ⇒  Invisible.
    #             Ps = 9  ⇒  Crossed-out characters.
    #             Ps = 2 1  ⇒  Doubly-underlined.
    #             Ps = 3 0  ⇒  Foreground color.
    #             Ps = 3 1  ⇒  Background color.
    #
    #           If no parameters are given, all of the video attributes are
    #           saved.  The stack is limited to 10 levels.

    # CSI Pt ; Pl ; Pb ; Pr $ {
    #           Selective Erase Rectangular Area (DECSERA), VT400 and up.
    #             Pt ; Pl ; Pb ; Pr denotes the rectangle.

    # CSI Pt ; Pl ; Pb ; Pr # |
    #           Report selected graphic rendition (XTREPORTSGR), xterm.  The
    #           response is an SGR sequence which contains the attributes
    #           which are common to all cells in a rectangle.
    #             Pt ; Pl ; Pb ; Pr denotes the rectangle.

    # CSI Ps $ |
    #           Select columns per page (DECSCPP), VT340.
    #             Ps = 0  ⇒  80 columns, default if Ps omitted.
    #             Ps = 8 0  ⇒  80 columns.
    #             Ps = 1 3 2  ⇒  132 columns.

    # CSI Ps ' |
    #           Request Locator Position (DECRQLP).
    #           Valid values for the parameter are:
    #             Ps = 0 , 1 or omitted ⇒  transmit a single DECLRP locator
    #           report.
    #
    #           If Locator Reporting has been enabled by a DECELR, xterm will
    #           respond with a DECLRP Locator Report.  This report is also
    #           generated on button up and down events if they have been
    #           enabled with a DECSLE, or when the locator is detected outside
    #           of a filter rectangle, if filter rectangles have been enabled
    #           with a DECEFR.
    #
    #             ⇐  CSI Pe ; Pb ; Pr ; Pc ; Pp &  w
    #
    #           Parameters are [event;button;row;column;page].
    #           Valid values for the event:
    #             Pe = 0  ⇐  locator unavailable - no other parameters sent.
    #             Pe = 1  ⇐  request - xterm received a DECRQLP.
    #             Pe = 2  ⇐  left button down.
    #             Pe = 3  ⇐  left button up.
    #             Pe = 4  ⇐  middle button down.
    #             Pe = 5  ⇐  middle button up.
    #             Pe = 6  ⇐  right button down.
    #             Pe = 7  ⇐  right button up.
    #             Pe = 8  ⇐  M4 button down.
    #             Pe = 9  ⇐  M4 button up.
    #             Pe = 1 0  ⇐  locator outside filter rectangle.
    #           The "button" parameter is a bitmask indicating which buttons
    #           are pressed:
    #             Pb = 0  ⇐  no buttons down.
    #             Pb & 1  ⇐  right button down.
    #             Pb & 2  ⇐  middle button down.
    #             Pb & 4  ⇐  left button down.
    #             Pb & 8  ⇐  M4 button down.
    #           The "row" and "column" parameters are the coordinates of the
    #           locator position in the xterm window, encoded as ASCII
    #           decimal.
    #           The "page" parameter is not used by xterm.

    # CSI Ps * |
    #           Select number of lines per screen (DECSNLS), VT420 and up.

    # CSI # }   Pop video attributes from stack (XTPOPSGR), xterm.  Popping
    #           restores the video-attributes which were saved using XTPUSHSGR
    #           to their previous state.

    # CSI Ps ' }
    #           Insert Ps Column(s) (default = 1) (DECIC), VT420 and up.

    # CSI Ps $ }
    #           Select active status display (DECSASD), VT320 and up.
    #             Ps = 0  ⇒  main (default)
    #             Ps = 1  ⇒  status line

    # CSI Ps ' ~
    #           Delete Ps Column(s) (default = 1) (DECDC), VT420 and up.

    # CSI Ps $ ~
    #           Select status line type (DECSSDT), VT320 and up.
    #             Ps = 0  ⇒  none
    #             Ps = 1  ⇒  indicator (default)
    #             Ps = 2  ⇒  host-writable.

    _CSI_MAP = {
        '@': _CSI___ICH,    # CSI Ps @        Insert Ps (Blank) Character(s) (default = 1) (ICH).
        # '@': _CSI___SL,   #
        'A': _CSI_A_CUU,    # CSI Ps A        Cursor Up Ps Times (default = 1) (CUU).
        # 'A': _CSI_A_SR,   #
        'B': _CSI_B_CUD,    # CSI Ps B        Cursor Down Ps Times (default = 1) (CUD).
        'C': _CSI_C_CUF,    # CSI Ps C        Cursor Forward Ps Times (default = 1) (CUF).
        'D': _CSI_D_CUB,    # CSI Ps D        Cursor Backward Ps Times (default = 1) (CUB).
        'E': _CSI_E_CNL,    # CSI Ps E        Cursor Next Line Ps Times (default = 1) (CNL).
        'F': _CSI_F_CPL,    # CSI Ps F        Cursor Preceding Line Ps Times (default = 1) (CPL).
        'G': _CSI_G_CHA,    # CSI Ps G        Cursor Character Absolute  [column] (default = [row,1]) (CHA).
        'H': _CSI_H_CUP,    # CSI Ps ; Ps H   Cursor Position [row;column] (default = [1,1]) (CUP).
        # 'I': _CSI_I_CHT,
        'J': _CSI_J_ED,     # CSI Ps J  Erase in Display (ED), VT100. [0:Below, 1:Above, 2:All, 3:SavedLines]
        'K': _CSI_K_EL,     # CSI Ps K  Erase in Line (EL), VT100.    [0:Right, 1:Left,  2:All]
        'L': _CSI_L_IL,     # CSI Ps L  Insert Ps Line(s) (default = 1) (IL).
        'M': _CSI_M_DL,     # CSI Ps M  Delete Ps Line(s) (default = 1) (DL).
        'P': _CSI_P_DCH,    # CSI Ps P  Delete Ps Character(s) (default = 1) (DCH).
        'S': _CSI_S_SU,     # CSI Ps S  Scroll up Ps lines (default = 1) (SU), VT420, ECMA-48.
        'T': _CSI_T_SD,     # CSI Ps T  Scroll down Ps lines (default = 1) (SD), VT420.
        'X': _CSI_X_ECH,    # CSI Ps X  Erase Ps Character(s) (default = 1) (ECH).
        # 'Z': _CSI_Z_CBT,
        # '^': _CSI___SD,
        # '`': _CSI___HPA,
        # 'a': _CSI_a_HPR,
        'b': _CSI_b_REP,    # CSI Ps b  Repeat the preceding graphic character Ps times (REP).
        # 'c': _CSI_c_Pri_DA,
        'd': _CSI_d_VPA,    # CSI Ps d  Line Position Absolute  [row] (default = [1,column]) (VPA).
        # 'e': _CSI_e_VPR,
        'f': _CSI_f_HVP,    # CSI Ps ; Ps f    Horizontal and Vertical Position [row;column] (default = [1,1]) (HVP).
        # 'g': _CSI_g_TBC,
        #    'h': _CSI_h_SM,
        # 'i': _CSI_i_MC,
        #    'l': _CSI_l_RM,
        # 'm': _CSI_m_SGR,
        # 'n': _CSI_n_DSR,
        # 'q': _CSI_q_DECLL,
        'r': _CSI_r_DECSTBM, # CSI Ps ; Ps r    Set Scrolling Region [top;bottom] (default = full size of window) (DECSTBM), VT100.
        # 's': _CSI_s_SCOSC,
        # 'u': _CSI_u_SCORC,
        # 'x': _CSI_x_DECREQTPARM
    }
