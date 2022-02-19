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

from TermTk.TTkCore.constant import TTkK

class KeyEvent:
    __slots__ = ('type', 'key', 'code', 'mod')
    def __init__(self, type:int, key: str, code: str, mod: int):
        self.type = type
        self.key = key
        self.mod = mod
        self.code = code
    def __str__(self):
        code = self.code.replace('\033','<ESC>')
        return f"KeyEvent: {self.key} {key2str(self.key)} {mod2str(self.mod)} {code}"

    @staticmethod
    def parse(input_key):  # from: Space           except "DEL"
        if len(input_key) == 1 and "\040" <= input_key != "\177":
            return KeyEvent(TTkK.Character, input_key, input_key, TTkK.NoModifier)
        else:
            key, mod = _translate_key(input_key)
            if key is not None:
                return KeyEvent(TTkK.SpecialKey, key, input_key, mod)
        return None

def _translate_key(key):
    if   key == "\177"      : return TTkK.Key_Backspace , TTkK.NoModifier
    elif key == "\t"        : return TTkK.Key_Tab       , TTkK.NoModifier
    elif key == "\033[Z"    : return TTkK.Key_Tab       , TTkK.ShiftModifier
    elif key == "\n"        : return TTkK.Key_Enter     , TTkK.NoModifier
    elif key == "\033[A"    : return TTkK.Key_Up        , TTkK.NoModifier
    elif key == "\033[B"    : return TTkK.Key_Down      , TTkK.NoModifier
    elif key == "\033[C"    : return TTkK.Key_Right     , TTkK.NoModifier
    elif key == "\033[D"    : return TTkK.Key_Left      , TTkK.NoModifier
    elif key == "\033[5~"   : return TTkK.Key_PageUp    , TTkK.NoModifier
    elif key == "\033[6~"   : return TTkK.Key_PageDown  , TTkK.NoModifier
    # Xterm
    elif key == "\033[F"    : return TTkK.Key_End       , TTkK.NoModifier
    elif key == "\033[H"    : return TTkK.Key_Home      , TTkK.NoModifier
    # Terminator + tmux
    elif key == "\033[4~"   : return TTkK.Key_End       , TTkK.NoModifier
    elif key == "\033[1~"   : return TTkK.Key_Home      , TTkK.NoModifier
    elif key == "\033[2~"   : return TTkK.Key_Insert    , TTkK.NoModifier
    elif key == "\033[3~"   : return TTkK.Key_Delete    , TTkK.NoModifier
    elif key == "\033"      : return TTkK.Key_Escape    , TTkK.NoModifier
    # Function Key
    elif key == "\033OP"    : return TTkK.Key_F1        , TTkK.NoModifier
    elif key == "\033OQ"    : return TTkK.Key_F2        , TTkK.NoModifier
    elif key == "\033OR"    : return TTkK.Key_F3        , TTkK.NoModifier
    elif key == "\033OS"    : return TTkK.Key_F4        , TTkK.NoModifier
    elif key == "\033[15~"  : return TTkK.Key_F5        , TTkK.NoModifier
    elif key == "\033[17~"  : return TTkK.Key_F6        , TTkK.NoModifier
    elif key == "\033[18~"  : return TTkK.Key_F7        , TTkK.NoModifier
    elif key == "\033[19~"  : return TTkK.Key_F8        , TTkK.NoModifier
    elif key == "\033[20~"  : return TTkK.Key_F9        , TTkK.NoModifier
    elif key == "\033[21~"  : return TTkK.Key_F10       , TTkK.NoModifier
    elif key == "\033[23~"  : return TTkK.Key_F11       , TTkK.NoModifier
    elif key == "\033[24~"  : return TTkK.Key_F12       , TTkK.NoModifier
    elif key == "\033[1;2P" : return TTkK.Key_F1        , TTkK.ShiftModifier
    elif key == "\033[1;2Q" : return TTkK.Key_F2        , TTkK.ShiftModifier
    elif key == "\033[1;2R" : return TTkK.Key_F3        , TTkK.ShiftModifier
    elif key == "\033[1;2S" : return TTkK.Key_F4        , TTkK.ShiftModifier
    elif key == "\033[15;2~": return TTkK.Key_F5        , TTkK.ShiftModifier
    elif key == "\033[17;2~": return TTkK.Key_F6        , TTkK.ShiftModifier
    elif key == "\033[18;2~": return TTkK.Key_F7        , TTkK.ShiftModifier
    elif key == "\033[19;2~": return TTkK.Key_F8        , TTkK.ShiftModifier
    elif key == "\033[20;2~": return TTkK.Key_F9        , TTkK.ShiftModifier
    elif key == "\033[21;2~": return TTkK.Key_F10       , TTkK.ShiftModifier
    elif key == "\033[23;2~": return TTkK.Key_F11       , TTkK.ShiftModifier
    elif key == "\033[24;2~": return TTkK.Key_F12       , TTkK.ShiftModifier
    elif key == "\033[1;5P" : return TTkK.Key_F1        , TTkK.ControlModifier
    elif key == "\033[1;5Q" : return TTkK.Key_F2        , TTkK.ControlModifier
    elif key == "\033[1;5R" : return TTkK.Key_F3        , TTkK.ControlModifier
    elif key == "\033[1;5S" : return TTkK.Key_F4        , TTkK.ControlModifier
    elif key == "\033[15;5~": return TTkK.Key_F5        , TTkK.ControlModifier
    elif key == "\033[17;5~": return TTkK.Key_F6        , TTkK.ControlModifier
    elif key == "\033[18;5~": return TTkK.Key_F7        , TTkK.ControlModifier
    elif key == "\033[19;5~": return TTkK.Key_F8        , TTkK.ControlModifier
    elif key == "\033[20;5~": return TTkK.Key_F9        , TTkK.ControlModifier
    elif key == "\033[21;5~": return TTkK.Key_F10       , TTkK.ControlModifier
    elif key == "\033[23;5~": return TTkK.Key_F11       , TTkK.ControlModifier
    elif key == "\033[24;5~": return TTkK.Key_F12       , TTkK.ControlModifier
    # elif key == "\033[1;3P" : return TTkK.Key_F1        , TTkK.AltModifier
    # elif key == "\033[1;3Q" : return TTkK.Key_F2        , TTkK.AltModifier
    elif key == "\033[1;3R" : return TTkK.Key_F3        , TTkK.AltModifier
    #elif key == "\033[1;3S" : return TTkK.Key_F4        , TTkK.AltModifier
    #elif key == "\033[15;3~": return TTkK.Key_F5        , TTkK.AltModifier
    elif key == "\033[17;3~": return TTkK.Key_F6        , TTkK.AltModifier
    #elif key == "\033[18;3~": return TTkK.Key_F7        , TTkK.AltModifier
    #elif key == "\033[19;3~": return TTkK.Key_F8        , TTkK.AltModifier
    elif key == "\033[20;3~": return TTkK.Key_F9        , TTkK.AltModifier
    #elif key == "\033[21;3~": return TTkK.Key_F10       , TTkK.AltModifier
    elif key == "\033[23;3~": return TTkK.Key_F11       , TTkK.AltModifier
    elif key == "\033[24;3~": return TTkK.Key_F12       , TTkK.AltModifier
    return None, None

    # # elif key == "\033": return TTkK.Key_Tab
    # if True: return None
    # elif key == "\033": return TTkK.Key_Backtab
    # elif key == "\033": return TTkK.Key_Backspace
    # elif key == "\033": return TTkK.Key_Return
    # elif key == "\033": return TTkK.Key_Enter
    # elif key == "\033": return TTkK.Key_Pause
    # elif key == "\033": return TTkK.Key_Print
    # elif key == "\033": return TTkK.Key_SysReq
    # elif key == "\033": return TTkK.Key_Clear
    # elif key == "\033": return TTkK.Key_Shift
    # elif key == "\033": return TTkK.Key_Control
    # elif key == "\033": return TTkK.Key_Meta
    # elif key == "\033": return TTkK.Key_Alt
    # elif key == "\033": return TTkK.Key_AltGr
    # elif key == "\033": return TTkK.Key_CapsLock
    # elif key == "\033": return TTkK.Key_NumLock
    # elif key == "\033": return TTkK.Key_ScrollLock
    # elif key == "\033": return TTkK.Key_F13
    # elif key == "\033": return TTkK.Key_F14
    # elif key == "\033": return TTkK.Key_F15
    # elif key == "\033": return TTkK.Key_F16
    # elif key == "\033": return TTkK.Key_F17
    # elif key == "\033": return TTkK.Key_F18
    # elif key == "\033": return TTkK.Key_F19
    # elif key == "\033": return TTkK.Key_F20
    # elif key == "\033": return TTkK.Key_F21
    # elif key == "\033": return TTkK.Key_F22
    # elif key == "\033": return TTkK.Key_F23
    # elif key == "\033": return TTkK.Key_F24
    # elif key == "\033": return TTkK.Key_F25
    # elif key == "\033": return TTkK.Key_F26
    # elif key == "\033": return TTkK.Key_F27
    # elif key == "\033": return TTkK.Key_F28
    # elif key == "\033": return TTkK.Key_F29
    # elif key == "\033": return TTkK.Key_F30
    # elif key == "\033": return TTkK.Key_F31
    # elif key == "\033": return TTkK.Key_F32
    # elif key == "\033": return TTkK.Key_F33
    # elif key == "\033": return TTkK.Key_F34
    # elif key == "\033": return TTkK.Key_F35
    # elif key == "\033": return TTkK.Key_Super_L
    # elif key == "\033": return TTkK.Key_Super_R
    # elif key == "\033": return TTkK.Key_Menu
    # elif key == "\033": return TTkK.Key_Hyper_L
    # elif key == "\033": return TTkK.Key_Hyper_R
    # elif key == "\033": return TTkK.Key_Help
    # elif key == "\033": return TTkK.Key_Direction_L
    # elif key == "\033": return TTkK.Key_Direction_R
    # elif key == "\033": return TTkK.Key_Space
    # elif key == "\033": return TTkK.Key_Any
    # return TTkK.NONE

def mod2str(k):
    if k == TTkK.NoModifier          : return "NoModifier"
    if k == TTkK.ShiftModifier       : return "ShiftModifier"
    if k == TTkK.ControlModifier     : return "ControlModifier"
    if k == TTkK.AltModifier         : return "AltModifier"
    if k == TTkK.MetaModifier        : return "MetaModifier"
    if k == TTkK.KeypadModifier      : return "KeypadModifier"
    if k == TTkK.GroupSwitchModifier : return "GroupSwitchModifier"
    return "NONE!!!"

def key2str(k):
    if k == TTkK.Key_Escape                   : return "Key_Escape"
    if k == TTkK.Key_Tab                      : return "Key_Tab"
    if k == TTkK.Key_Backtab                  : return "Key_Backtab"
    if k == TTkK.Key_Backspace                : return "Key_Backspace"
    if k == TTkK.Key_Return                   : return "Key_Return"
    if k == TTkK.Key_Enter                    : return "Key_Enter"
    if k == TTkK.Key_Insert                   : return "Key_Insert"
    if k == TTkK.Key_Delete                   : return "Key_Delete"
    if k == TTkK.Key_Pause                    : return "Key_Pause"
    if k == TTkK.Key_Print                    : return "Key_Print"
    if k == TTkK.Key_SysReq                   : return "Key_SysReq"
    if k == TTkK.Key_Clear                    : return "Key_Clear"
    if k == TTkK.Key_Home                     : return "Key_Home"
    if k == TTkK.Key_End                      : return "Key_End"
    if k == TTkK.Key_Left                     : return "Key_Left"
    if k == TTkK.Key_Up                       : return "Key_Up"
    if k == TTkK.Key_Right                    : return "Key_Right"
    if k == TTkK.Key_Down                     : return "Key_Down"
    if k == TTkK.Key_PageUp                   : return "Key_PageUp"
    if k == TTkK.Key_PageDown                 : return "Key_PageDown"
    if k == TTkK.Key_Shift                    : return "Key_Shift"
    if k == TTkK.Key_Control                  : return "Key_Control"
    if k == TTkK.Key_Meta                     : return "Key_Meta"
    if k == TTkK.Key_Alt                      : return "Key_Alt"
    if k == TTkK.Key_AltGr                    : return "Key_AltGr"
    if k == TTkK.Key_CapsLock                 : return "Key_CapsLock"
    if k == TTkK.Key_NumLock                  : return "Key_NumLock"
    if k == TTkK.Key_ScrollLock               : return "Key_ScrollLock"
    if k == TTkK.Key_F1                       : return "Key_F1"
    if k == TTkK.Key_F2                       : return "Key_F2"
    if k == TTkK.Key_F3                       : return "Key_F3"
    if k == TTkK.Key_F4                       : return "Key_F4"
    if k == TTkK.Key_F5                       : return "Key_F5"
    if k == TTkK.Key_F6                       : return "Key_F6"
    if k == TTkK.Key_F7                       : return "Key_F7"
    if k == TTkK.Key_F8                       : return "Key_F8"
    if k == TTkK.Key_F9                       : return "Key_F9"
    if k == TTkK.Key_F10                      : return "Key_F10"
    if k == TTkK.Key_F11                      : return "Key_F11"
    if k == TTkK.Key_F12                      : return "Key_F12"
    if k == TTkK.Key_F13                      : return "Key_F13"
    if k == TTkK.Key_F14                      : return "Key_F14"
    if k == TTkK.Key_F15                      : return "Key_F15"
    if k == TTkK.Key_F16                      : return "Key_F16"
    if k == TTkK.Key_F17                      : return "Key_F17"
    if k == TTkK.Key_F18                      : return "Key_F18"
    if k == TTkK.Key_F19                      : return "Key_F19"
    if k == TTkK.Key_F20                      : return "Key_F20"
    if k == TTkK.Key_F21                      : return "Key_F21"
    if k == TTkK.Key_F22                      : return "Key_F22"
    if k == TTkK.Key_F23                      : return "Key_F23"
    if k == TTkK.Key_F24                      : return "Key_F24"
    if k == TTkK.Key_F25                      : return "Key_F25"
    if k == TTkK.Key_F26                      : return "Key_F26"
    if k == TTkK.Key_F27                      : return "Key_F27"
    if k == TTkK.Key_F28                      : return "Key_F28"
    if k == TTkK.Key_F29                      : return "Key_F29"
    if k == TTkK.Key_F30                      : return "Key_F30"
    if k == TTkK.Key_F31                      : return "Key_F31"
    if k == TTkK.Key_F32                      : return "Key_F32"
    if k == TTkK.Key_F33                      : return "Key_F33"
    if k == TTkK.Key_F34                      : return "Key_F34"
    if k == TTkK.Key_F35                      : return "Key_F35"
    if k == TTkK.Key_Super_L                  : return "Key_Super_L"
    if k == TTkK.Key_Super_R                  : return "Key_Super_R"
    if k == TTkK.Key_Menu                     : return "Key_Menu"
    if k == TTkK.Key_Hyper_L                  : return "Key_Hyper_L"
    if k == TTkK.Key_Hyper_R                  : return "Key_Hyper_R"
    if k == TTkK.Key_Help                     : return "Key_Help"
    if k == TTkK.Key_Direction_L              : return "Key_Direction_L"
    if k == TTkK.Key_Direction_R              : return "Key_Direction_R"
    if k == TTkK.Key_Space                    : return "Key_Space"
    if k == TTkK.Key_Any                      : return "Key_Any"
    if k == TTkK.Key_Space                    : return "Key_Space"
    if k == TTkK.Key_Exclam                   : return "Key_Exclam"
    if k == TTkK.Key_QuoteDbl                 : return "Key_QuoteDbl"
    if k == TTkK.Key_NumberSign               : return "Key_NumberSign"
    if k == TTkK.Key_Dollar                   : return "Key_Dollar"
    if k == TTkK.Key_Percent                  : return "Key_Percent"
    if k == TTkK.Key_Ampersand                : return "Key_Ampersand"
    if k == TTkK.Key_Apostrophe               : return "Key_Apostrophe"
    if k == TTkK.Key_ParenLeft                : return "Key_ParenLeft"
    if k == TTkK.Key_ParenRight               : return "Key_ParenRight"
    if k == TTkK.Key_Asterisk                 : return "Key_Asterisk"
    if k == TTkK.Key_Plus                     : return "Key_Plus"
    if k == TTkK.Key_Comma                    : return "Key_Comma"
    if k == TTkK.Key_Minus                    : return "Key_Minus"
    if k == TTkK.Key_Period                   : return "Key_Period"
    if k == TTkK.Key_Slash                    : return "Key_Slash"
    if k == TTkK.Key_0                        : return "Key_0"
    if k == TTkK.Key_1                        : return "Key_1"
    if k == TTkK.Key_2                        : return "Key_2"
    if k == TTkK.Key_3                        : return "Key_3"
    if k == TTkK.Key_4                        : return "Key_4"
    if k == TTkK.Key_5                        : return "Key_5"
    if k == TTkK.Key_6                        : return "Key_6"
    if k == TTkK.Key_7                        : return "Key_7"
    if k == TTkK.Key_8                        : return "Key_8"
    if k == TTkK.Key_9                        : return "Key_9"
    if k == TTkK.Key_Colon                    : return "Key_Colon"
    if k == TTkK.Key_Semicolon                : return "Key_Semicolon"
    if k == TTkK.Key_Less                     : return "Key_Less"
    if k == TTkK.Key_Equal                    : return "Key_Equal"
    if k == TTkK.Key_Greater                  : return "Key_Greater"
    if k == TTkK.Key_Question                 : return "Key_Question"
    if k == TTkK.Key_At                       : return "Key_At"
    if k == TTkK.Key_A                        : return "Key_A"
    if k == TTkK.Key_B                        : return "Key_B"
    if k == TTkK.Key_C                        : return "Key_C"
    if k == TTkK.Key_D                        : return "Key_D"
    if k == TTkK.Key_E                        : return "Key_E"
    if k == TTkK.Key_F                        : return "Key_F"
    if k == TTkK.Key_G                        : return "Key_G"
    if k == TTkK.Key_H                        : return "Key_H"
    if k == TTkK.Key_I                        : return "Key_I"
    if k == TTkK.Key_J                        : return "Key_J"
    if k == TTkK.Key_K                        : return "Key_K"
    if k == TTkK.Key_L                        : return "Key_L"
    if k == TTkK.Key_M                        : return "Key_M"
    if k == TTkK.Key_N                        : return "Key_N"
    if k == TTkK.Key_O                        : return "Key_O"
    if k == TTkK.Key_P                        : return "Key_P"
    if k == TTkK.Key_Q                        : return "Key_Q"
    if k == TTkK.Key_R                        : return "Key_R"
    if k == TTkK.Key_S                        : return "Key_S"
    if k == TTkK.Key_T                        : return "Key_T"
    if k == TTkK.Key_U                        : return "Key_U"
    if k == TTkK.Key_V                        : return "Key_V"
    if k == TTkK.Key_W                        : return "Key_W"
    if k == TTkK.Key_X                        : return "Key_X"
    if k == TTkK.Key_Y                        : return "Key_Y"
    if k == TTkK.Key_Z                        : return "Key_Z"
    if k == TTkK.Key_BracketLeft              : return "Key_BracketLeft"
    if k == TTkK.Key_Backslash                : return "Key_Backslash"
    if k == TTkK.Key_BracketRight             : return "Key_BracketRight"
    if k == TTkK.Key_AsciiCircum              : return "Key_AsciiCircum"
    if k == TTkK.Key_Underscore               : return "Key_Underscore"
    if k == TTkK.Key_QuoteLeft                : return "Key_QuoteLeft"
    if k == TTkK.Key_BraceLeft                : return "Key_BraceLeft"
    if k == TTkK.Key_Bar                      : return "Key_Bar"
    if k == TTkK.Key_BraceRight               : return "Key_BraceRight"
    if k == TTkK.Key_AsciiTilde               : return "Key_AsciiTilde"
    if k == TTkK.Key_nobreakspace             : return "Key_nobreakspace"
    if k == TTkK.Key_exclamdown               : return "Key_exclamdown"
    if k == TTkK.Key_cent                     : return "Key_cent"
    if k == TTkK.Key_sterling                 : return "Key_sterling"
    if k == TTkK.Key_currency                 : return "Key_currency"
    if k == TTkK.Key_yen                      : return "Key_yen"
    if k == TTkK.Key_brokenbar                : return "Key_brokenbar"
    if k == TTkK.Key_section                  : return "Key_section"
    if k == TTkK.Key_diaeresis                : return "Key_diaeresis"
    if k == TTkK.Key_copyright                : return "Key_copyright"
    if k == TTkK.Key_ordfeminine              : return "Key_ordfeminine"
    if k == TTkK.Key_guillemotleft            : return "Key_guillemotleft"
    if k == TTkK.Key_notsign                  : return "Key_notsign"
    if k == TTkK.Key_hyphen                   : return "Key_hyphen"
    if k == TTkK.Key_registered               : return "Key_registered"
    if k == TTkK.Key_macron                   : return "Key_macron"
    if k == TTkK.Key_degree                   : return "Key_degree"
    if k == TTkK.Key_plusminus                : return "Key_plusminus"
    if k == TTkK.Key_twosuperior              : return "Key_twosuperior"
    if k == TTkK.Key_threesuperior            : return "Key_threesuperior"
    if k == TTkK.Key_acute                    : return "Key_acute"
    if k == TTkK.Key_mu                       : return "Key_mu"
    if k == TTkK.Key_paragraph                : return "Key_paragraph"
    if k == TTkK.Key_periodcentered           : return "Key_periodcentered"
    if k == TTkK.Key_cedilla                  : return "Key_cedilla"
    if k == TTkK.Key_onesuperior              : return "Key_onesuperior"
    if k == TTkK.Key_masculine                : return "Key_masculine"
    if k == TTkK.Key_guillemotright           : return "Key_guillemotright"
    if k == TTkK.Key_onequarter               : return "Key_onequarter"
    if k == TTkK.Key_onehalf                  : return "Key_onehalf"
    if k == TTkK.Key_threequarters            : return "Key_threequarters"
    if k == TTkK.Key_questiondown             : return "Key_questiondown"
    if k == TTkK.Key_Agrave                   : return "Key_Agrave"
    if k == TTkK.Key_Aacute                   : return "Key_Aacute"
    if k == TTkK.Key_Acircumflex              : return "Key_Acircumflex"
    if k == TTkK.Key_Atilde                   : return "Key_Atilde"
    if k == TTkK.Key_Adiaeresis               : return "Key_Adiaeresis"
    if k == TTkK.Key_Aring                    : return "Key_Aring"
    if k == TTkK.Key_AE                       : return "Key_AE"
    if k == TTkK.Key_Ccedilla                 : return "Key_Ccedilla"
    if k == TTkK.Key_Egrave                   : return "Key_Egrave"
    if k == TTkK.Key_Eacute                   : return "Key_Eacute"
    if k == TTkK.Key_Ecircumflex              : return "Key_Ecircumflex"
    if k == TTkK.Key_Ediaeresis               : return "Key_Ediaeresis"
    if k == TTkK.Key_Igrave                   : return "Key_Igrave"
    if k == TTkK.Key_Iacute                   : return "Key_Iacute"
    if k == TTkK.Key_Icircumflex              : return "Key_Icircumflex"
    if k == TTkK.Key_Idiaeresis               : return "Key_Idiaeresis"
    if k == TTkK.Key_ETH                      : return "Key_ETH"
    if k == TTkK.Key_Ntilde                   : return "Key_Ntilde"
    if k == TTkK.Key_Ograve                   : return "Key_Ograve"
    if k == TTkK.Key_Oacute                   : return "Key_Oacute"
    if k == TTkK.Key_Ocircumflex              : return "Key_Ocircumflex"
    if k == TTkK.Key_Otilde                   : return "Key_Otilde"
    if k == TTkK.Key_Odiaeresis               : return "Key_Odiaeresis"
    if k == TTkK.Key_multiply                 : return "Key_multiply"
    if k == TTkK.Key_Ooblique                 : return "Key_Ooblique"
    if k == TTkK.Key_Ugrave                   : return "Key_Ugrave"
    if k == TTkK.Key_Uacute                   : return "Key_Uacute"
    if k == TTkK.Key_Ucircumflex              : return "Key_Ucircumflex"
    if k == TTkK.Key_Udiaeresis               : return "Key_Udiaeresis"
    if k == TTkK.Key_Yacute                   : return "Key_Yacute"
    if k == TTkK.Key_THORN                    : return "Key_THORN"
    if k == TTkK.Key_ssharp                   : return "Key_ssharp"
    if k == TTkK.Key_division                 : return "Key_division"
    if k == TTkK.Key_ydiaeresis               : return "Key_ydiaeresis"
    if k == TTkK.Key_Multi_key                : return "Key_Multi_key"
    if k == TTkK.Key_Codeinput                : return "Key_Codeinput"
    if k == TTkK.Key_SingleCandidate          : return "Key_SingleCandidate"
    if k == TTkK.Key_MultipleCandidate        : return "Key_MultipleCandidate"
    if k == TTkK.Key_PreviousCandidate        : return "Key_PreviousCandidate"
    if k == TTkK.Key_Mode_switch              : return "Key_Mode_switch"
    if k == TTkK.Key_Kanji                    : return "Key_Kanji"
    if k == TTkK.Key_Muhenkan                 : return "Key_Muhenkan"
    if k == TTkK.Key_Henkan                   : return "Key_Henkan"
    if k == TTkK.Key_Romaji                   : return "Key_Romaji"
    if k == TTkK.Key_Hiragana                 : return "Key_Hiragana"
    if k == TTkK.Key_Katakana                 : return "Key_Katakana"
    if k == TTkK.Key_Hiragana_Katakana        : return "Key_Hiragana_Katakana"
    if k == TTkK.Key_Zenkaku                  : return "Key_Zenkaku"
    if k == TTkK.Key_Hankaku                  : return "Key_Hankaku"
    if k == TTkK.Key_Zenkaku_Hankaku          : return "Key_Zenkaku_Hankaku"
    if k == TTkK.Key_Touroku                  : return "Key_Touroku"
    if k == TTkK.Key_Massyo                   : return "Key_Massyo"
    if k == TTkK.Key_Kana_Lock                : return "Key_Kana_Lock"
    if k == TTkK.Key_Kana_Shift               : return "Key_Kana_Shift"
    if k == TTkK.Key_Eisu_Shift               : return "Key_Eisu_Shift"
    if k == TTkK.Key_Eisu_toggle              : return "Key_Eisu_toggle"
    if k == TTkK.Key_Hangul                   : return "Key_Hangul"
    if k == TTkK.Key_Hangul_Start             : return "Key_Hangul_Start"
    if k == TTkK.Key_Hangul_End               : return "Key_Hangul_End"
    if k == TTkK.Key_Hangul_Hanja             : return "Key_Hangul_Hanja"
    if k == TTkK.Key_Hangul_Jamo              : return "Key_Hangul_Jamo"
    if k == TTkK.Key_Hangul_Romaja            : return "Key_Hangul_Romaja"
    if k == TTkK.Key_Hangul_Jeonja            : return "Key_Hangul_Jeonja"
    if k == TTkK.Key_Hangul_Banja             : return "Key_Hangul_Banja"
    if k == TTkK.Key_Hangul_PreHanja          : return "Key_Hangul_PreHanja"
    if k == TTkK.Key_Hangul_PostHanja         : return "Key_Hangul_PostHanja"
    if k == TTkK.Key_Hangul_Special           : return "Key_Hangul_Special"
    if k == TTkK.Key_Dead_Grave               : return "Key_Dead_Grave"
    if k == TTkK.Key_Dead_Acute               : return "Key_Dead_Acute"
    if k == TTkK.Key_Dead_Circumflex          : return "Key_Dead_Circumflex"
    if k == TTkK.Key_Dead_Tilde               : return "Key_Dead_Tilde"
    if k == TTkK.Key_Dead_Macron              : return "Key_Dead_Macron"
    if k == TTkK.Key_Dead_Breve               : return "Key_Dead_Breve"
    if k == TTkK.Key_Dead_Abovedot            : return "Key_Dead_Abovedot"
    if k == TTkK.Key_Dead_Diaeresis           : return "Key_Dead_Diaeresis"
    if k == TTkK.Key_Dead_Abovering           : return "Key_Dead_Abovering"
    if k == TTkK.Key_Dead_Doubleacute         : return "Key_Dead_Doubleacute"
    if k == TTkK.Key_Dead_Caron               : return "Key_Dead_Caron"
    if k == TTkK.Key_Dead_Cedilla             : return "Key_Dead_Cedilla"
    if k == TTkK.Key_Dead_Ogonek              : return "Key_Dead_Ogonek"
    if k == TTkK.Key_Dead_Iota                : return "Key_Dead_Iota"
    if k == TTkK.Key_Dead_Voiced_Sound        : return "Key_Dead_Voiced_Sound"
    if k == TTkK.Key_Dead_Semivoiced_Sound    : return "Key_Dead_Semivoiced_Sound"
    if k == TTkK.Key_Dead_Belowdot            : return "Key_Dead_Belowdot"
    if k == TTkK.Key_Dead_Hook                : return "Key_Dead_Hook"
    if k == TTkK.Key_Dead_Horn                : return "Key_Dead_Horn"
    if k == TTkK.Key_Dead_Stroke              : return "Key_Dead_Stroke"
    if k == TTkK.Key_Dead_Abovecomma          : return "Key_Dead_Abovecomma"
    if k == TTkK.Key_Dead_Abovereversedcomma  : return "Key_Dead_Abovereversedcomma"
    if k == TTkK.Key_Dead_Doublegrave         : return "Key_Dead_Doublegrave"
    if k == TTkK.Key_Dead_Belowring           : return "Key_Dead_Belowring"
    if k == TTkK.Key_Dead_Belowmacron         : return "Key_Dead_Belowmacron"
    if k == TTkK.Key_Dead_Belowcircumflex     : return "Key_Dead_Belowcircumflex"
    if k == TTkK.Key_Dead_Belowtilde          : return "Key_Dead_Belowtilde"
    if k == TTkK.Key_Dead_Belowbreve          : return "Key_Dead_Belowbreve"
    if k == TTkK.Key_Dead_Belowdiaeresis      : return "Key_Dead_Belowdiaeresis"
    if k == TTkK.Key_Dead_Invertedbreve       : return "Key_Dead_Invertedbreve"
    if k == TTkK.Key_Dead_Belowcomma          : return "Key_Dead_Belowcomma"
    if k == TTkK.Key_Dead_Currency            : return "Key_Dead_Currency"
    if k == TTkK.Key_Dead_a                   : return "Key_Dead_a"
    if k == TTkK.Key_Dead_A                   : return "Key_Dead_A"
    if k == TTkK.Key_Dead_e                   : return "Key_Dead_e"
    if k == TTkK.Key_Dead_E                   : return "Key_Dead_E"
    if k == TTkK.Key_Dead_i                   : return "Key_Dead_i"
    if k == TTkK.Key_Dead_I                   : return "Key_Dead_I"
    if k == TTkK.Key_Dead_o                   : return "Key_Dead_o"
    if k == TTkK.Key_Dead_O                   : return "Key_Dead_O"
    if k == TTkK.Key_Dead_u                   : return "Key_Dead_u"
    if k == TTkK.Key_Dead_U                   : return "Key_Dead_U"
    if k == TTkK.Key_Dead_Small_Schwa         : return "Key_Dead_Small_Schwa"
    if k == TTkK.Key_Dead_Capital_Schwa       : return "Key_Dead_Capital_Schwa"
    if k == TTkK.Key_Dead_Greek               : return "Key_Dead_Greek"
    if k == TTkK.Key_Dead_Lowline             : return "Key_Dead_Lowline"
    if k == TTkK.Key_Dead_Aboveverticalline   : return "Key_Dead_Aboveverticalline"
    if k == TTkK.Key_Dead_Belowverticalline   : return "Key_Dead_Belowverticalline"
    if k == TTkK.Key_Dead_Longsolidusoverlay  : return "Key_Dead_Longsolidusoverlay"
    if k == TTkK.Key_Back                     : return "Key_Back"
    if k == TTkK.Key_Forward                  : return "Key_Forward"
    if k == TTkK.Key_Stop                     : return "Key_Stop"
    if k == TTkK.Key_Refresh                  : return "Key_Refresh"
    if k == TTkK.Key_VolumeDown               : return "Key_VolumeDown"
    if k == TTkK.Key_VolumeMute               : return "Key_VolumeMute"
    if k == TTkK.Key_VolumeUp                 : return "Key_VolumeUp"
    if k == TTkK.Key_BassBoost                : return "Key_BassBoost"
    if k == TTkK.Key_BassUp                   : return "Key_BassUp"
    if k == TTkK.Key_BassDown                 : return "Key_BassDown"
    if k == TTkK.Key_TrebleUp                 : return "Key_TrebleUp"
    if k == TTkK.Key_TrebleDown               : return "Key_TrebleDown"
    if k == TTkK.Key_MediaPlay                : return "Key_MediaPlay"
    if k == TTkK.Key_MediaStop                : return "Key_MediaStop"
    if k == TTkK.Key_MediaPrevious            : return "Key_MediaPrevious"
    if k == TTkK.Key_MediaNext                : return "Key_MediaNext"
    if k == TTkK.Key_MediaRecord              : return "Key_MediaRecord"
    if k == TTkK.Key_MediaPause               : return "Key_MediaPause"
    if k == TTkK.Key_MediaTogglePlayPause     : return "Key_MediaTogglePlayPause"
    if k == TTkK.Key_HomePage                 : return "Key_HomePage"
    if k == TTkK.Key_Favorites                : return "Key_Favorites"
    if k == TTkK.Key_Search                   : return "Key_Search"
    if k == TTkK.Key_Standby                  : return "Key_Standby"
    if k == TTkK.Key_OpenUrl                  : return "Key_OpenUrl"
    if k == TTkK.Key_LaunchMail               : return "Key_LaunchMail"
    if k == TTkK.Key_LaunchMedia              : return "Key_LaunchMedia"
    if k == TTkK.Key_Launch0                  : return "Key_Launch0"
    if k == TTkK.Key_Launch1                  : return "Key_Launch1"
    if k == TTkK.Key_Launch2                  : return "Key_Launch2"
    if k == TTkK.Key_Launch3                  : return "Key_Launch3"
    if k == TTkK.Key_Launch4                  : return "Key_Launch4"
    if k == TTkK.Key_Launch5                  : return "Key_Launch5"
    if k == TTkK.Key_Launch6                  : return "Key_Launch6"
    if k == TTkK.Key_Launch7                  : return "Key_Launch7"
    if k == TTkK.Key_Launch8                  : return "Key_Launch8"
    if k == TTkK.Key_Launch9                  : return "Key_Launch9"
    if k == TTkK.Key_LaunchA                  : return "Key_LaunchA"
    if k == TTkK.Key_LaunchB                  : return "Key_LaunchB"
    if k == TTkK.Key_LaunchC                  : return "Key_LaunchC"
    if k == TTkK.Key_LaunchD                  : return "Key_LaunchD"
    if k == TTkK.Key_LaunchE                  : return "Key_LaunchE"
    if k == TTkK.Key_LaunchF                  : return "Key_LaunchF"
    if k == TTkK.Key_LaunchG                  : return "Key_LaunchG"
    if k == TTkK.Key_LaunchH                  : return "Key_LaunchH"
    if k == TTkK.Key_MonBrightnessUp          : return "Key_MonBrightnessUp"
    if k == TTkK.Key_MonBrightnessDown        : return "Key_MonBrightnessDown"
    if k == TTkK.Key_KeyboardLightOnOff       : return "Key_KeyboardLightOnOff"
    if k == TTkK.Key_KeyboardBrightnessUp     : return "Key_KeyboardBrightnessUp"
    if k == TTkK.Key_KeyboardBrightnessDown   : return "Key_KeyboardBrightnessDown"
    if k == TTkK.Key_PowerOff                 : return "Key_PowerOff"
    if k == TTkK.Key_WakeUp                   : return "Key_WakeUp"
    if k == TTkK.Key_Eject                    : return "Key_Eject"
    if k == TTkK.Key_ScreenSaver              : return "Key_ScreenSaver"
    if k == TTkK.Key_WWW                      : return "Key_WWW"
    if k == TTkK.Key_Memo                     : return "Key_Memo"
    if k == TTkK.Key_LightBulb                : return "Key_LightBulb"
    if k == TTkK.Key_Shop                     : return "Key_Shop"
    if k == TTkK.Key_History                  : return "Key_History"
    if k == TTkK.Key_AddFavorite              : return "Key_AddFavorite"
    if k == TTkK.Key_HotLinks                 : return "Key_HotLinks"
    if k == TTkK.Key_BrightnessAdjust         : return "Key_BrightnessAdjust"
    if k == TTkK.Key_Finance                  : return "Key_Finance"
    if k == TTkK.Key_Community                : return "Key_Community"
    if k == TTkK.Key_AudioRewind              : return "Key_AudioRewind"
    if k == TTkK.Key_BackForward              : return "Key_BackForward"
    if k == TTkK.Key_ApplicationLeft          : return "Key_ApplicationLeft"
    if k == TTkK.Key_ApplicationRight         : return "Key_ApplicationRight"
    if k == TTkK.Key_Book                     : return "Key_Book"
    if k == TTkK.Key_CD                       : return "Key_CD"
    if k == TTkK.Key_Calculator               : return "Key_Calculator"
    if k == TTkK.Key_ToDoList                 : return "Key_ToDoList"
    if k == TTkK.Key_ClearGrab                : return "Key_ClearGrab"
    if k == TTkK.Key_Close                    : return "Key_Close"
    if k == TTkK.Key_Copy                     : return "Key_Copy"
    if k == TTkK.Key_Cut                      : return "Key_Cut"
    if k == TTkK.Key_Display                  : return "Key_Display"
    if k == TTkK.Key_DOS                      : return "Key_DOS"
    if k == TTkK.Key_Documents                : return "Key_Documents"
    if k == TTkK.Key_Excel                    : return "Key_Excel"
    if k == TTkK.Key_Explorer                 : return "Key_Explorer"
    if k == TTkK.Key_Game                     : return "Key_Game"
    if k == TTkK.Key_Go                       : return "Key_Go"
    if k == TTkK.Key_iTouch                   : return "Key_iTouch"
    if k == TTkK.Key_LogOff                   : return "Key_LogOff"
    if k == TTkK.Key_Market                   : return "Key_Market"
    if k == TTkK.Key_Meeting                  : return "Key_Meeting"
    if k == TTkK.Key_MenuKB                   : return "Key_MenuKB"
    if k == TTkK.Key_MenuPB                   : return "Key_MenuPB"
    if k == TTkK.Key_MySites                  : return "Key_MySites"
    if k == TTkK.Key_News                     : return "Key_News"
    if k == TTkK.Key_OfficeHome               : return "Key_OfficeHome"
    if k == TTkK.Key_Option                   : return "Key_Option"
    if k == TTkK.Key_Paste                    : return "Key_Paste"
    if k == TTkK.Key_Phone                    : return "Key_Phone"
    if k == TTkK.Key_Calendar                 : return "Key_Calendar"
    if k == TTkK.Key_Reply                    : return "Key_Reply"
    if k == TTkK.Key_Reload                   : return "Key_Reload"
    if k == TTkK.Key_RotateWindows            : return "Key_RotateWindows"
    if k == TTkK.Key_RotationPB               : return "Key_RotationPB"
    if k == TTkK.Key_RotationKB               : return "Key_RotationKB"
    if k == TTkK.Key_Save                     : return "Key_Save"
    if k == TTkK.Key_Send                     : return "Key_Send"
    if k == TTkK.Key_Spell                    : return "Key_Spell"
    if k == TTkK.Key_SplitScreen              : return "Key_SplitScreen"
    if k == TTkK.Key_Support                  : return "Key_Support"
    if k == TTkK.Key_TaskPane                 : return "Key_TaskPane"
    if k == TTkK.Key_Terminal                 : return "Key_Terminal"
    if k == TTkK.Key_Tools                    : return "Key_Tools"
    if k == TTkK.Key_Travel                   : return "Key_Travel"
    if k == TTkK.Key_Video                    : return "Key_Video"
    if k == TTkK.Key_Word                     : return "Key_Word"
    if k == TTkK.Key_Xfer                     : return "Key_Xfer"
    if k == TTkK.Key_ZoomIn                   : return "Key_ZoomIn"
    if k == TTkK.Key_ZoomOut                  : return "Key_ZoomOut"
    if k == TTkK.Key_Away                     : return "Key_Away"
    if k == TTkK.Key_Messenger                : return "Key_Messenger"
    if k == TTkK.Key_WebCam                   : return "Key_WebCam"
    if k == TTkK.Key_MailForward              : return "Key_MailForward"
    if k == TTkK.Key_Pictures                 : return "Key_Pictures"
    if k == TTkK.Key_Music                    : return "Key_Music"
    if k == TTkK.Key_Battery                  : return "Key_Battery"
    if k == TTkK.Key_Bluetooth                : return "Key_Bluetooth"
    if k == TTkK.Key_WLAN                     : return "Key_WLAN"
    if k == TTkK.Key_UWB                      : return "Key_UWB"
    if k == TTkK.Key_AudioForward             : return "Key_AudioForward"
    if k == TTkK.Key_AudioRepeat              : return "Key_AudioRepeat"
    if k == TTkK.Key_AudioRandomPlay          : return "Key_AudioRandomPlay"
    if k == TTkK.Key_Subtitle                 : return "Key_Subtitle"
    if k == TTkK.Key_AudioCycleTrack          : return "Key_AudioCycleTrack"
    if k == TTkK.Key_Time                     : return "Key_Time"
    if k == TTkK.Key_Hibernate                : return "Key_Hibernate"
    if k == TTkK.Key_View                     : return "Key_View"
    if k == TTkK.Key_TopMenu                  : return "Key_TopMenu"
    if k == TTkK.Key_PowerDown                : return "Key_PowerDown"
    if k == TTkK.Key_Suspend                  : return "Key_Suspend"
    if k == TTkK.Key_ContrastAdjust           : return "Key_ContrastAdjust"
    if k == TTkK.Key_TouchpadToggle           : return "Key_TouchpadToggle"
    if k == TTkK.Key_TouchpadOn               : return "Key_TouchpadOn"
    if k == TTkK.Key_TouchpadOff              : return "Key_TouchpadOff"
    if k == TTkK.Key_MicMute                  : return "Key_MicMute"
    if k == TTkK.Key_Red                      : return "Key_Red"
    if k == TTkK.Key_Green                    : return "Key_Green"
    if k == TTkK.Key_Yellow                   : return "Key_Yellow"
    if k == TTkK.Key_Blue                     : return "Key_Blue"
    if k == TTkK.Key_ChannelUp                : return "Key_ChannelUp"
    if k == TTkK.Key_ChannelDown              : return "Key_ChannelDown"
    if k == TTkK.Key_Guide                    : return "Key_Guide"
    if k == TTkK.Key_Info                     : return "Key_Info"
    if k == TTkK.Key_Settings                 : return "Key_Settings"
    if k == TTkK.Key_MicVolumeUp              : return "Key_MicVolumeUp"
    if k == TTkK.Key_MicVolumeDown            : return "Key_MicVolumeDown"
    if k == TTkK.Key_New                      : return "Key_New"
    if k == TTkK.Key_Open                     : return "Key_Open"
    if k == TTkK.Key_Find                     : return "Key_Find"
    if k == TTkK.Key_Undo                     : return "Key_Undo"
    if k == TTkK.Key_Redo                     : return "Key_Redo"
    if k == TTkK.Key_MediaLast                : return "Key_MediaLast"
    if k == TTkK.Key_unknown                  : return "Key_unknown"
    if k == TTkK.Key_Call                     : return "Key_Call"
    if k == TTkK.Key_Camera                   : return "Key_Camera"
    if k == TTkK.Key_CameraFocus              : return "Key_CameraFocus"
    if k == TTkK.Key_Context1                 : return "Key_Context1"
    if k == TTkK.Key_Context2                 : return "Key_Context2"
    if k == TTkK.Key_Context3                 : return "Key_Context3"
    if k == TTkK.Key_Context4                 : return "Key_Context4"
    if k == TTkK.Key_Flip                     : return "Key_Flip"
    if k == TTkK.Key_Hangup                   : return "Key_Hangup"
    if k == TTkK.Key_No                       : return "Key_No"
    if k == TTkK.Key_Select                   : return "Key_Select"
    if k == TTkK.Key_Yes                      : return "Key_Yes"
    if k == TTkK.Key_ToggleCallHangup         : return "Key_ToggleCallHangup"
    if k == TTkK.Key_VoiceDial                : return "Key_VoiceDial"
    if k == TTkK.Key_LastNumberRedial         : return "Key_LastNumberRedial"
    if k == TTkK.Key_Execute                  : return "Key_Execute"
    if k == TTkK.Key_Printer                  : return "Key_Printer"
    if k == TTkK.Key_Play                     : return "Key_Play"
    if k == TTkK.Key_Sleep                    : return "Key_Sleep"
    if k == TTkK.Key_Zoom                     : return "Key_Zoom"
    if k == TTkK.Key_Exit                     : return "Key_Exit"
    if k == TTkK.Key_Cancel                   : return "Key_Cancel"
    return "NONE!!!"