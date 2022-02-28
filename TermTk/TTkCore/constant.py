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


class TTkConstant:
    """Class container of all the constants used in :mod:`~TermTk`"""

    NONE = 0x0000

    # Color Depth
    DEP_2: int = 0x02
    DEP_4: int = 0x04
    DEP_8: int = 0x08
    DEP_24: int = 0x18

    # Color Type
    class ColorType:
        Foreground = 0x01
        Background = 0x02
        Modifier = 0x03

    Foreground = ColorType.Foreground
    Background = ColorType.Background
    Modifier = ColorType.Modifier

    # Focus Policies
    NoFocus = 0x0000
    ClickFocus = 0x0001
    WheelFocus = 0x0002
    TabFocus = 0x0004

    # positions
    NONE = 0x0000
    TOP = 0x0001
    BOTTOM = 0x0002
    LEFT = 0x0004
    RIGHT = 0x0008
    CENTER = 0x0010

    # SelectionMode
    NoSelection = 0x00
    SingleSelection = 0x01
    MultiSelection = 0x02
    ExtendedSelection = 0x03
    ContiguousSelection = 0x04

    # Graph types
    FILLED = 0x0001
    LINE = 0x0002

    # Mouse Events
    MOUSE_EVENT = 0x01
    KEY_EVENT = 0x02
    SCREEN_EVENT = 0x04
    QUIT_EVENT = 0x08
    TIME_EVENT = 0x10

    HORIZONTAL = 0x01
    VERTICAL = 0x02

    class ScrollBarPolicy:
        ScrollBarAsNeeded = 0x00
        ScrollBarAlwaysOff = 0x01
        ScrollBarAlwaysOn = 0x02

    ScrollBarAsNeeded = ScrollBarPolicy.ScrollBarAsNeeded
    ScrollBarAlwaysOff = ScrollBarPolicy.ScrollBarAlwaysOff
    ScrollBarAlwaysOn = ScrollBarPolicy.ScrollBarAlwaysOn

    class CheckState:
        Unchecked = 0x00
        PartiallyChecked = 0x01
        Checked = 0x02

    Unchecked = CheckState.Unchecked
    PartiallyChecked = CheckState.PartiallyChecked
    Checked = CheckState.Checked

    class InsertPolicy:
        NoInsert = 0x00  # The string will not be inserted into the combobox.
        InsertAtTop = (
            0x01  # The string will be inserted as the first item in the combobox.
        )
        # InsertAtCurrent      = 0x02   # The current item will be replaced by the string.
        InsertAtBottom = (
            0x03  # The string will be inserted after the last item in the combobox.
        )
        # InsertAfterCurrent   = 0x04   # The string is inserted after the current item in the combobox.
        # InsertBeforeCurrent  = 0x05   # The string is inserted before the current item in the combobox.
        # InsertAlphabetically = 0x06   # The string is inserted in the alphabetic order in the combobox.

    class ChildIndicatorPolicy:
        ShowIndicator = 0x00  # The controls for expanding and collapsing will be shown for this item even if there are no children.
        DontShowIndicator = 0x01  # The controls for expanding and collapsing will never be shown even if there are children. If the node is forced open the user will not be able to expand or collapse the item.
        DontShowIndicatorWhenChildless = 0x02  # The controls for expanding and collapsing will be shown if the item contains children.

    ShowIndicator = ChildIndicatorPolicy.ShowIndicator
    DontShowIndicator = ChildIndicatorPolicy.DontShowIndicator
    DontShowIndicatorWhenChildless = ChildIndicatorPolicy.DontShowIndicatorWhenChildless

    class SortOrder:
        AscendingOrder = 0x00
        DescendingOrder = 0x01

    AscendingOrder = SortOrder.AscendingOrder
    DescendingOrder = SortOrder.DescendingOrder

    NoInsert = InsertPolicy.NoInsert
    InsertAtTop = InsertPolicy.InsertAtTop
    # InsertAtCurrent      = InsertPolicy.InsertAtCurrent
    InsertAtBottom = InsertPolicy.InsertAtBottom
    # InsertAfterCurrent   = InsertPolicy.InsertAfterCurrent
    # InsertBeforeCurrent  = InsertPolicy.InsertBeforeCurrent
    # InsertAlphabetically = InsertPolicy.InsertAlphabetically

    # Keys
    NoButton = 0x00000000  # The button state does not refer to any button (see QMouseEvent::button()).
    AllButtons = 0x07FFFFFF  # This value corresponds to a mask of all possible mouse buttons. Use to set the 'acceptedButtons' property of a MouseArea to accept ALL mouse buttons.
    LeftButton = 0x00000001  # The left button is pressed, or an event refers to the left button. (The left button may be the right button on left-handed mice.)
    RightButton = 0x00000002  # The right button.
    MidButton = 0x00000004  # The middle button.
    MiddleButton = MidButton  # The middle button.
    Wheel = 0x00000008

    # Events
    NoEvent = 0x00000000
    Press = 0x00010000
    Release = 0x00020000
    Drag = 0x00040000
    Move = 0x00080000
    WHEEL_Up = 0x00100000  # Wheel Up
    WHEEL_Down = 0x00200000  # Wheel Down

    # Cursors
    Cursor_Blinking_Block = 0x0001
    Cursor_Blinking_Block_Also = 0x0002
    Cursor_Steady_Block = 0x0003
    Cursor_Blinking_Underline = 0x0004
    Cursor_Steady_Underline = 0x0005
    Cursor_Blinking_Bar = 0x0006
    Cursor_Steady_Bar = 0x0007

    # Input types
    Input_Text = 0x01
    Input_Number = 0x02
    Input_Password = 0x04

    # Alignment
    class Alignment:
        """This class type is used to describe alignment.

        .. autosummary::
          NONE
          LEFT_ALIGN
          RIGHT_ALIGN
          CENTER_ALIGN
          JUSTIFY
        """

        NONE = 0x0000
        """ No Alignment"""
        LEFT_ALIGN = 0x0001
        """ Aligns with the left edge."""
        RIGHT_ALIGN = 0x0002
        """ Aligns with the right edge."""
        CENTER_ALIGN = 0x0004
        """ Centers horizontally in the available space."""
        JUSTIFY = 0x0008
        """ Justifies the text in the available space."""

    LEFT_ALIGN = Alignment.LEFT_ALIGN
    RIGHT_ALIGN = Alignment.RIGHT_ALIGN
    CENTER_ALIGN = Alignment.CENTER_ALIGN
    JUSTIFY = Alignment.JUSTIFY

    class FileMode:
        AnyFile = 0  # The name of a file, whether it exists or not.
        # ExistingFile   = 1 #The name of a single existing file.
        Directory = 2  # The name of a directory. Both files and directories are displayed. However, the native Windows file dialog does not support displaying files in the directory chooser.
        # ExistingFiles  = 3 #The names of zero or more existing files.

    # AnyFile       = FileMode.AnyFile
    # ExistingFile  = FileMode.ExistingFile
    # Directory     = FileMode.Directory
    # ExistingFiles = FileMode.ExistingFiles

    # LayoutItem Types
    class LayoutItemTypes:
        """Types used internally in :mod:`~TermTk.TTkLayouts`"""

        LayoutItem = 0x01
        """Item Type Layout"""
        WidgetItem = 0x02
        """Item Type Widget"""

    LayoutItem = LayoutItemTypes.LayoutItem
    WidgetItem = LayoutItemTypes.WidgetItem

    Character = 0x0001
    SpecialKey = 0x0002

    NoModifier = 0x00000000  # No modifier key is pressed.
    ShiftModifier = 0x02000000  # A Shift key on the keyboard is pressed.
    ControlModifier = 0x04000000  # A Ctrl key on the keyboard is pressed.
    AltModifier = 0x08000000  # An Alt key on the keyboard is pressed.
    MetaModifier = 0x10000000  # A Meta key on the keyboard is pressed.
    KeypadModifier = 0x20000000  # A keypad button is pressed.
    GroupSwitchModifier = 0x40000000  # X11 only (unless activated on Windows by a command line argument). A Mode_switch key on the keyboard is pressed.

    Key_Escape = 0x01000000
    Key_Tab = 0x01000001
    Key_Backtab = 0x01000002
    Key_Backspace = 0x01000003
    Key_Return = 0x01000004
    Key_Enter = 0x01000005  # Typically located on the keypad.
    Key_Insert = 0x01000006
    Key_Delete = 0x01000007
    Key_Pause = 0x01000008  # The Pause/Break key (Note: Not related to pausing media)
    Key_Print = 0x01000009
    Key_SysReq = 0x0100000A
    Key_Clear = 0x0100000B
    Key_Home = 0x01000010
    Key_End = 0x01000011
    Key_Left = 0x01000012
    Key_Up = 0x01000013
    Key_Right = 0x01000014
    Key_Down = 0x01000015
    Key_PageUp = 0x01000016
    Key_PageDown = 0x01000017
    Key_Shift = 0x01000020
    Key_Control = 0x01000021  # On macOS, this corresponds to the Command keys.
    Key_Meta = 0x01000022  # On macOS, this corresponds to the Control keys. On Windows keyboards, this key is mapped to the Windows key.
    Key_Alt = 0x01000023
    Key_AltGr = 0x01001103  # On Windows, when the KeyDown event for this key is sent, the Ctrl+Alt modifiers are also set.
    Key_CapsLock = 0x01000024
    Key_NumLock = 0x01000025
    Key_ScrollLock = 0x01000026
    Key_F1 = 0x01000030
    Key_F2 = 0x01000031
    Key_F3 = 0x01000032
    Key_F4 = 0x01000033
    Key_F5 = 0x01000034
    Key_F6 = 0x01000035
    Key_F7 = 0x01000036
    Key_F8 = 0x01000037
    Key_F9 = 0x01000038
    Key_F10 = 0x01000039
    Key_F11 = 0x0100003A
    Key_F12 = 0x0100003B
    Key_F13 = 0x0100003C
    Key_F14 = 0x0100003D
    Key_F15 = 0x0100003E
    Key_F16 = 0x0100003F
    Key_F17 = 0x01000040
    Key_F18 = 0x01000041
    Key_F19 = 0x01000042
    Key_F20 = 0x01000043
    Key_F21 = 0x01000044
    Key_F22 = 0x01000045
    Key_F23 = 0x01000046
    Key_F24 = 0x01000047
    Key_F25 = 0x01000048
    Key_F26 = 0x01000049
    Key_F27 = 0x0100004A
    Key_F28 = 0x0100004B
    Key_F29 = 0x0100004C
    Key_F30 = 0x0100004D
    Key_F31 = 0x0100004E
    Key_F32 = 0x0100004F
    Key_F33 = 0x01000050
    Key_F34 = 0x01000051
    Key_F35 = 0x01000052
    Key_Super_L = 0x01000053
    Key_Super_R = 0x01000054
    Key_Menu = 0x01000055
    Key_Hyper_L = 0x01000056
    Key_Hyper_R = 0x01000057
    Key_Help = 0x01000058
    Key_Direction_L = 0x01000059
    Key_Direction_R = 0x01000060
    Key_Space = 0x20
    Key_Any = Key_Space
    Key_Exclam = 0x21
    Key_QuoteDbl = 0x22
    Key_NumberSign = 0x23
    Key_Dollar = 0x24
    Key_Percent = 0x25
    Key_Ampersand = 0x26
    Key_Apostrophe = 0x27
    Key_ParenLeft = 0x28
    Key_ParenRight = 0x29
    Key_Asterisk = 0x2A
    Key_Plus = 0x2B
    Key_Comma = 0x2C
    Key_Minus = 0x2D
    Key_Period = 0x2E
    Key_Slash = 0x2F
    Key_0 = 0x30
    Key_1 = 0x31
    Key_2 = 0x32
    Key_3 = 0x33
    Key_4 = 0x34
    Key_5 = 0x35
    Key_6 = 0x36
    Key_7 = 0x37
    Key_8 = 0x38
    Key_9 = 0x39
    Key_Colon = 0x3A
    Key_Semicolon = 0x3B
    Key_Less = 0x3C
    Key_Equal = 0x3D
    Key_Greater = 0x3E
    Key_Question = 0x3F
    Key_At = 0x40
    Key_A = 0x41
    Key_B = 0x42
    Key_C = 0x43
    Key_D = 0x44
    Key_E = 0x45
    Key_F = 0x46
    Key_G = 0x47
    Key_H = 0x48
    Key_I = 0x49
    Key_J = 0x4A
    Key_K = 0x4B
    Key_L = 0x4C
    Key_M = 0x4D
    Key_N = 0x4E
    Key_O = 0x4F
    Key_P = 0x50
    Key_Q = 0x51
    Key_R = 0x52
    Key_S = 0x53
    Key_T = 0x54
    Key_U = 0x55
    Key_V = 0x56
    Key_W = 0x57
    Key_X = 0x58
    Key_Y = 0x59
    Key_Z = 0x5A
    Key_BracketLeft = 0x5B
    Key_Backslash = 0x5C
    Key_BracketRight = 0x5D
    Key_AsciiCircum = 0x5E
    Key_Underscore = 0x5F
    Key_QuoteLeft = 0x60
    Key_BraceLeft = 0x7B
    Key_Bar = 0x7C
    Key_BraceRight = 0x7D
    Key_AsciiTilde = 0x7E
    Key_nobreakspace = 0x0A0
    Key_exclamdown = 0x0A1
    Key_cent = 0x0A2
    Key_sterling = 0x0A3
    Key_currency = 0x0A4
    Key_yen = 0x0A5
    Key_brokenbar = 0x0A6
    Key_section = 0x0A7
    Key_diaeresis = 0x0A8
    Key_copyright = 0x0A9
    Key_ordfeminine = 0x0AA
    Key_guillemotleft = 0x0AB
    Key_notsign = 0x0AC
    Key_hyphen = 0x0AD
    Key_registered = 0x0AE
    Key_macron = 0x0AF
    Key_degree = 0x0B0
    Key_plusminus = 0x0B1
    Key_twosuperior = 0x0B2
    Key_threesuperior = 0x0B3
    Key_acute = 0x0B4
    Key_mu = 0x0B5
    Key_paragraph = 0x0B6
    Key_periodcentered = 0x0B7
    Key_cedilla = 0x0B8
    Key_onesuperior = 0x0B9
    Key_masculine = 0x0BA
    Key_guillemotright = 0x0BB
    Key_onequarter = 0x0BC
    Key_onehalf = 0x0BD
    Key_threequarters = 0x0BE
    Key_questiondown = 0x0BF
    Key_Agrave = 0x0C0
    Key_Aacute = 0x0C1
    Key_Acircumflex = 0x0C2
    Key_Atilde = 0x0C3
    Key_Adiaeresis = 0x0C4
    Key_Aring = 0x0C5
    Key_AE = 0x0C6
    Key_Ccedilla = 0x0C7
    Key_Egrave = 0x0C8
    Key_Eacute = 0x0C9
    Key_Ecircumflex = 0x0CA
    Key_Ediaeresis = 0x0CB
    Key_Igrave = 0x0CC
    Key_Iacute = 0x0CD
    Key_Icircumflex = 0x0CE
    Key_Idiaeresis = 0x0CF
    Key_ETH = 0x0D0
    Key_Ntilde = 0x0D1
    Key_Ograve = 0x0D2
    Key_Oacute = 0x0D3
    Key_Ocircumflex = 0x0D4
    Key_Otilde = 0x0D5
    Key_Odiaeresis = 0x0D6
    Key_multiply = 0x0D7
    Key_Ooblique = 0x0D8
    Key_Ugrave = 0x0D9
    Key_Uacute = 0x0DA
    Key_Ucircumflex = 0x0DB
    Key_Udiaeresis = 0x0DC
    Key_Yacute = 0x0DD
    Key_THORN = 0x0DE
    Key_ssharp = 0x0DF
    Key_division = 0x0F7
    Key_ydiaeresis = 0x0FF
    Key_Multi_key = 0x01001120
    Key_Codeinput = 0x01001137
    Key_SingleCandidate = 0x0100113C
    Key_MultipleCandidate = 0x0100113D
    Key_PreviousCandidate = 0x0100113E
    Key_Mode_switch = 0x0100117E
    Key_Kanji = 0x01001121
    Key_Muhenkan = 0x01001122
    Key_Henkan = 0x01001123
    Key_Romaji = 0x01001124
    Key_Hiragana = 0x01001125
    Key_Katakana = 0x01001126
    Key_Hiragana_Katakana = 0x01001127
    Key_Zenkaku = 0x01001128
    Key_Hankaku = 0x01001129
    Key_Zenkaku_Hankaku = 0x0100112A
    Key_Touroku = 0x0100112B
    Key_Massyo = 0x0100112C
    Key_Kana_Lock = 0x0100112D
    Key_Kana_Shift = 0x0100112E
    Key_Eisu_Shift = 0x0100112F
    Key_Eisu_toggle = 0x01001130
    Key_Hangul = 0x01001131
    Key_Hangul_Start = 0x01001132
    Key_Hangul_End = 0x01001133
    Key_Hangul_Hanja = 0x01001134
    Key_Hangul_Jamo = 0x01001135
    Key_Hangul_Romaja = 0x01001136
    Key_Hangul_Jeonja = 0x01001138
    Key_Hangul_Banja = 0x01001139
    Key_Hangul_PreHanja = 0x0100113A
    Key_Hangul_PostHanja = 0x0100113B
    Key_Hangul_Special = 0x0100113F
    Key_Dead_Grave = 0x01001250
    Key_Dead_Acute = 0x01001251
    Key_Dead_Circumflex = 0x01001252
    Key_Dead_Tilde = 0x01001253
    Key_Dead_Macron = 0x01001254
    Key_Dead_Breve = 0x01001255
    Key_Dead_Abovedot = 0x01001256
    Key_Dead_Diaeresis = 0x01001257
    Key_Dead_Abovering = 0x01001258
    Key_Dead_Doubleacute = 0x01001259
    Key_Dead_Caron = 0x0100125A
    Key_Dead_Cedilla = 0x0100125B
    Key_Dead_Ogonek = 0x0100125C
    Key_Dead_Iota = 0x0100125D
    Key_Dead_Voiced_Sound = 0x0100125E
    Key_Dead_Semivoiced_Sound = 0x0100125F
    Key_Dead_Belowdot = 0x01001260
    Key_Dead_Hook = 0x01001261
    Key_Dead_Horn = 0x01001262
    Key_Dead_Stroke = 0x01001263
    Key_Dead_Abovecomma = 0x01001264
    Key_Dead_Abovereversedcomma = 0x01001265
    Key_Dead_Doublegrave = 0x01001266
    Key_Dead_Belowring = 0x01001267
    Key_Dead_Belowmacron = 0x01001268
    Key_Dead_Belowcircumflex = 0x01001269
    Key_Dead_Belowtilde = 0x0100126A
    Key_Dead_Belowbreve = 0x0100126B
    Key_Dead_Belowdiaeresis = 0x0100126C
    Key_Dead_Invertedbreve = 0x0100126D
    Key_Dead_Belowcomma = 0x0100126E
    Key_Dead_Currency = 0x0100126F
    Key_Dead_a = 0x01001280
    Key_Dead_A = 0x01001281
    Key_Dead_e = 0x01001282
    Key_Dead_E = 0x01001283
    Key_Dead_i = 0x01001284
    Key_Dead_I = 0x01001285
    Key_Dead_o = 0x01001286
    Key_Dead_O = 0x01001287
    Key_Dead_u = 0x01001288
    Key_Dead_U = 0x01001289
    Key_Dead_Small_Schwa = 0x0100128A
    Key_Dead_Capital_Schwa = 0x0100128B
    Key_Dead_Greek = 0x0100128C
    Key_Dead_Lowline = 0x01001290
    Key_Dead_Aboveverticalline = 0x01001291
    Key_Dead_Belowverticalline = 0x01001292
    Key_Dead_Longsolidusoverlay = 0x01001293
    Key_Back = 0x01000061
    Key_Forward = 0x01000062
    Key_Stop = 0x01000063
    Key_Refresh = 0x01000064
    Key_VolumeDown = 0x01000070
    Key_VolumeMute = 0x01000071
    Key_VolumeUp = 0x01000072
    Key_BassBoost = 0x01000073
    Key_BassUp = 0x01000074
    Key_BassDown = 0x01000075
    Key_TrebleUp = 0x01000076
    Key_TrebleDown = 0x01000077
    Key_MediaPlay = 0x01000080  # A key setting the state of the media player to play
    Key_MediaStop = 0x01000081  # A key setting the state of the media player to stop
    Key_MediaPrevious = 0x01000082
    Key_MediaNext = 0x01000083
    Key_MediaRecord = 0x01000084
    Key_MediaPause = 0x01000085  # A key setting the state of the media player to pause (Note: not the pause/break key)
    Key_MediaTogglePlayPause = 0x01000086  # A key to toggle the play/pause state in the media player (rather than setting an absolute state)
    Key_HomePage = 0x01000090
    Key_Favorites = 0x01000091
    Key_Search = 0x01000092
    Key_Standby = 0x01000093
    Key_OpenUrl = 0x01000094
    Key_LaunchMail = 0x010000A0
    Key_LaunchMedia = 0x010000A1
    Key_Launch0 = 0x010000A2  # On X11 this key is mapped to "My Computer" (XF86XK_MyComputer) key for legacy reasons.
    Key_Launch1 = 0x010000A3  # On X11 this key is mapped to "Calculator" (XF86XK_Calculator) key for legacy reasons.
    Key_Launch2 = 0x010000A4  # On X11 this key is mapped to XF86XK_Launch0 key for legacy reasons.
    Key_Launch3 = 0x010000A5  # On X11 this key is mapped to XF86XK_Launch1 key for legacy reasons.
    Key_Launch4 = 0x010000A6  # On X11 this key is mapped to XF86XK_Launch2 key for legacy reasons.
    Key_Launch5 = 0x010000A7  # On X11 this key is mapped to XF86XK_Launch3 key for legacy reasons.
    Key_Launch6 = 0x010000A8  # On X11 this key is mapped to XF86XK_Launch4 key for legacy reasons.
    Key_Launch7 = 0x010000A9  # On X11 this key is mapped to XF86XK_Launch5 key for legacy reasons.
    Key_Launch8 = 0x010000AA  # On X11 this key is mapped to XF86XK_Launch6 key for legacy reasons.
    Key_Launch9 = 0x010000AB  # On X11 this key is mapped to XF86XK_Launch7 key for legacy reasons.
    Key_LaunchA = 0x010000AC  # On X11 this key is mapped to XF86XK_Launch8 key for legacy reasons.
    Key_LaunchB = 0x010000AD  # On X11 this key is mapped to XF86XK_Launch9 key for legacy reasons.
    Key_LaunchC = 0x010000AE  # On X11 this key is mapped to XF86XK_LaunchA key for legacy reasons.
    Key_LaunchD = 0x010000AF  # On X11 this key is mapped to XF86XK_LaunchB key for legacy reasons.
    Key_LaunchE = 0x010000B0  # On X11 this key is mapped to XF86XK_LaunchC key for legacy reasons.
    Key_LaunchF = 0x010000B1  # On X11 this key is mapped to XF86XK_LaunchD key for legacy reasons.
    Key_LaunchG = 0x0100010E  # On X11 this key is mapped to XF86XK_LaunchE key for legacy reasons.
    Key_LaunchH = 0x0100010F  # On X11 this key is mapped to XF86XK_LaunchF key for legacy reasons.
    Key_MonBrightnessUp = 0x010000B2
    Key_MonBrightnessDown = 0x010000B3
    Key_KeyboardLightOnOff = 0x010000B4
    Key_KeyboardBrightnessUp = 0x010000B5
    Key_KeyboardBrightnessDown = 0x010000B6
    Key_PowerOff = 0x010000B7
    Key_WakeUp = 0x010000B8
    Key_Eject = 0x010000B9
    Key_ScreenSaver = 0x010000BA
    Key_WWW = 0x010000BB
    Key_Memo = 0x010000BC
    Key_LightBulb = 0x010000BD
    Key_Shop = 0x010000BE
    Key_History = 0x010000BF
    Key_AddFavorite = 0x010000C0
    Key_HotLinks = 0x010000C1
    Key_BrightnessAdjust = 0x010000C2
    Key_Finance = 0x010000C3
    Key_Community = 0x010000C4
    Key_AudioRewind = 0x010000C5
    Key_BackForward = 0x010000C6
    Key_ApplicationLeft = 0x010000C7
    Key_ApplicationRight = 0x010000C8
    Key_Book = 0x010000C9
    Key_CD = 0x010000CA
    Key_Calculator = 0x010000CB  # On X11 this key is not mapped for legacy reasons. Use Qt::Key_Launch1 instead.
    Key_ToDoList = 0x010000CC
    Key_ClearGrab = 0x010000CD
    Key_Close = 0x010000CE
    Key_Copy = 0x010000CF
    Key_Cut = 0x010000D0
    Key_Display = 0x010000D1
    Key_DOS = 0x010000D2
    Key_Documents = 0x010000D3
    Key_Excel = 0x010000D4
    Key_Explorer = 0x010000D5
    Key_Game = 0x010000D6
    Key_Go = 0x010000D7
    Key_iTouch = 0x010000D8
    Key_LogOff = 0x010000D9
    Key_Market = 0x010000DA
    Key_Meeting = 0x010000DB
    Key_MenuKB = 0x010000DC
    Key_MenuPB = 0x010000DD
    Key_MySites = 0x010000DE
    Key_News = 0x010000DF
    Key_OfficeHome = 0x010000E0
    Key_Option = 0x010000E1
    Key_Paste = 0x010000E2
    Key_Phone = 0x010000E3
    Key_Calendar = 0x010000E4
    Key_Reply = 0x010000E5
    Key_Reload = 0x010000E6
    Key_RotateWindows = 0x010000E7
    Key_RotationPB = 0x010000E8
    Key_RotationKB = 0x010000E9
    Key_Save = 0x010000EA
    Key_Send = 0x010000EB
    Key_Spell = 0x010000EC
    Key_SplitScreen = 0x010000ED
    Key_Support = 0x010000EE
    Key_TaskPane = 0x010000EF
    Key_Terminal = 0x010000F0
    Key_Tools = 0x010000F1
    Key_Travel = 0x010000F2
    Key_Video = 0x010000F3
    Key_Word = 0x010000F4
    Key_Xfer = 0x010000F5
    Key_ZoomIn = 0x010000F6
    Key_ZoomOut = 0x010000F7
    Key_Away = 0x010000F8
    Key_Messenger = 0x010000F9
    Key_WebCam = 0x010000FA
    Key_MailForward = 0x010000FB
    Key_Pictures = 0x010000FC
    Key_Music = 0x010000FD
    Key_Battery = 0x010000FE
    Key_Bluetooth = 0x010000FF
    Key_WLAN = 0x01000100
    Key_UWB = 0x01000101
    Key_AudioForward = 0x01000102
    Key_AudioRepeat = 0x01000103
    Key_AudioRandomPlay = 0x01000104
    Key_Subtitle = 0x01000105
    Key_AudioCycleTrack = 0x01000106
    Key_Time = 0x01000107
    Key_Hibernate = 0x01000108
    Key_View = 0x01000109
    Key_TopMenu = 0x0100010A
    Key_PowerDown = 0x0100010B
    Key_Suspend = 0x0100010C
    Key_ContrastAdjust = 0x0100010D
    Key_TouchpadToggle = 0x01000110
    Key_TouchpadOn = 0x01000111
    Key_TouchpadOff = 0x01000112
    Key_MicMute = 0x01000113
    Key_Red = 0x01000114
    Key_Green = 0x01000115
    Key_Yellow = 0x01000116
    Key_Blue = 0x01000117
    Key_ChannelUp = 0x01000118
    Key_ChannelDown = 0x01000119
    Key_Guide = 0x0100011A
    Key_Info = 0x0100011B
    Key_Settings = 0x0100011C
    Key_MicVolumeUp = 0x0100011D
    Key_MicVolumeDown = 0x0100011E
    Key_New = 0x01000120
    Key_Open = 0x01000121
    Key_Find = 0x01000122
    Key_Undo = 0x01000123
    Key_Redo = 0x01000124
    Key_MediaLast = 0x0100FFFF
    Key_unknown = 0x01FFFFFF
    Key_Call = 0x01100004  # A key to answer or initiate a call (see Qt::Key_ToggleCallHangup for a key to toggle current call state)
    Key_Camera = 0x01100020  # A key to activate the camera shutter. On Windows Runtime, the environment variable QT_QPA_ENABLE_CAMERA_KEYS must be set to receive the event.
    Key_CameraFocus = 0x01100021  # A key to focus the camera. On Windows Runtime, the environment variable QT_QPA_ENABLE_CAMERA_KEYS must be set to receive the event.
    Key_Context1 = 0x01100000
    Key_Context2 = 0x01100001
    Key_Context3 = 0x01100002
    Key_Context4 = 0x01100003
    Key_Flip = 0x01100006
    Key_Hangup = 0x01100005  # A key to end an ongoing call (see Qt::Key_ToggleCallHangup for a key to toggle current call state)
    Key_No = 0x01010002
    Key_Select = 0x01010000
    Key_Yes = 0x01010001
    Key_ToggleCallHangup = 0x01100007  # A key to toggle the current call state (ie. either answer, or hangup) depending on current call state
    Key_VoiceDial = 0x01100008
    Key_LastNumberRedial = 0x01100009
    Key_Execute = 0x01020003
    Key_Printer = 0x01020002
    Key_Play = 0x01020005
    Key_Sleep = 0x01020004
    Key_Zoom = 0x01020006
    Key_Exit = 0x0102000A
    Key_Cancel = 0x01020001


# Alias to TTkConstant
class TTkK(TTkConstant):
    pass
