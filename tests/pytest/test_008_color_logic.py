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

import os
import sys

import pytest

sys.path.append(os.path.join(sys.path[0], '../../libs/pyTermTk'))

from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.color import TTkColorGradient
from TermTk.TTkCore.color import TTkLinearGradient
from TermTk.TTkCore.constant import TTkK


def test_ttkcolor_fg_bg_and_fgbg_helpers_set_expected_channels():
    fg = TTkColor.fg('#010203')
    bg = TTkColor.bg('#a0b0c0')
    both = TTkColor.fgbg('#112233', '#445566')

    assert fg.fgToRGB() == (1, 2, 3)
    assert fg.bgToRGB() == (0, 0, 0)
    assert bg.bgToRGB() == (160, 176, 192)
    assert bg.fgToRGB() == (0, 0, 0)
    assert both.fgToRGB() == (17, 34, 51)
    assert both.bgToRGB() == (68, 85, 102)


def test_ttkcolor_style_modifier_flags_combine_with_or():
    style = TTkColor.BOLD + TTkColor.ITALIC + TTkColor.UNDERLINE + TTkColor.STRIKETROUGH + TTkColor.BLINKING

    assert style.bold()
    assert style.italic()
    assert style.underline()
    assert style.strikethrough()
    assert style.blinking()


def test_ttkcolor_add_prefers_rhs_channels_and_keeps_lhs_when_missing():
    lhs = TTkColor.fg('#001122') + TTkColor.bg('#334455')
    rhs_fg_only = TTkColor.fg('#aabbcc')

    mixed = lhs + rhs_fg_only

    assert mixed.fgToRGB() == (170, 187, 204)
    assert mixed.bgToRGB() == (51, 68, 85)


def test_ttkcolor_invert_foreground_background():
    color = TTkColor.fgbg('#112233', '#445566')
    inverted = color.invertFgBg()

    assert inverted.fgToRGB() == (68, 85, 102)
    assert inverted.bgToRGB() == (17, 34, 51)


def test_ttkcolor_rgb_hsl_roundtrip_stays_close():
    original = (23, 111, 207)
    hsl = TTkColor.rgb2hsl(original)
    reconstructed = TTkColor.hsl2rgb(hsl)

    assert abs(reconstructed[0] - original[0]) <= 2
    assert abs(reconstructed[1] - original[1]) <= 2
    assert abs(reconstructed[2] - original[2]) <= 2


def test_ttkcolor_link_keeps_link_type_in_colortype():
    linked = TTkColor.fg('#abcdef', link='https://example.invalid')

    assert linked.colorType() & TTkK.ColorType.Link


def test_ttkcolorgradient_copy_and_modparam_do_not_mutate_original_modifier_state():
    base = TTkColor.fg('#202020', modifier=TTkColorGradient(increment=10))
    before = base.mod(0, 0).fgToRGB()

    _derived = base.modParam(val=5, step=1)
    after = base.mod(0, 0).fgToRGB()

    assert after == before


def test_ttkcolorgradient_handles_large_coordinates_without_index_error():
    base = TTkColor.fg('#000000', modifier=TTkColorGradient(increment=1))

    result = base.mod(0, 5000)

    assert isinstance(result, TTkColor)


def test_ttkcolorgradient_handles_zero_step_without_division_error():
    base = TTkColor.fg('#101010', modifier=TTkColorGradient(increment=2))
    tweaked = base.modParam(val=1, step=0)

    result = tweaked.mod(0, 1)

    assert isinstance(result, TTkColor)


def test_ttklineargradient_zero_direction_is_safe_and_returns_base_color():
    gradient = TTkLinearGradient(direction=(0, 0), target_color=TTkColor.fgbg('#ffffff', '#ffffff'))
    base = TTkColor.fgbg('#111111', '#222222')

    result = gradient.exec(4, 3, base)

    assert result == base


def test_ttkcolor_eq_with_truthy_non_color_returns_false_not_exception():
    color = TTkColor.fg('#123456')

    assert (color == object()) is False


def test_ttkcolor_hsl2rgb_handles_out_of_range_hue_like_wrapped_angle():
    zero_hue = TTkColor.hsl2rgb((0, 100, 50))
    wrapped_hue = TTkColor.hsl2rgb((360, 100, 50))

    assert wrapped_hue == zero_hue


def test_ttkcolor_mod_link_radd_does_not_corrupt_bitflags():
    linked_bold = TTkColor.fg('#123456', link='https://example.invalid') + TTkColor.BOLD

    merged = linked_bold.__radd__(TTkColor.BOLD)

    assert merged.bold()
    assert not merged.italic()


# ---------------------------------------------------------------------------
# Constructors / static helpers
# ---------------------------------------------------------------------------

def test_ttkcolor_ansi_parses_plain_rgb_without_modifier():
    color = TTkColor.ansi('\033[38;2;10;20;30m')

    assert color.fgToRGB() == (10, 20, 30)
    assert color.bold() is False


def test_ttkcolor_ansi_parses_rgb_with_bold_modifier():
    color = TTkColor.ansi('\033[1;38;2;10;20;30m')

    assert color.fgToRGB() == (10, 20, 30)
    assert color.bold() is True


def test_ttkcolor_fg_bg_fgbg_with_link_produce_link_color_type():
    linked_fg = TTkColor.fg('#010203', link='https://a.invalid')
    linked_bg = TTkColor.bg('#040506', link='https://b.invalid')
    linked_both = TTkColor.fgbg('#070809', '#0a0b0c', link='https://c.invalid')

    assert linked_fg.colorType() & TTkK.ColorType.Link
    assert linked_bg.colorType() & TTkK.ColorType.Link
    assert linked_both.colorType() & TTkK.ColorType.Link


def test_ttkcolor_fg_bg_accept_keyword_argument():
    fg = TTkColor.fg(color='#0a0b0c')
    bg = TTkColor.bg(color='#0d0e0f')

    assert fg.fgToRGB() == (10, 11, 12)
    assert bg.bgToRGB() == (13, 14, 15)


def test_ttkcolor_fgbg_without_link_is_not_link_type():
    plain = TTkColor.fgbg('#101112', '#131415')

    assert not (plain.colorType() & TTkK.ColorType.Link)


# ---------------------------------------------------------------------------
# foreground() / background() / has*
# ---------------------------------------------------------------------------

def test_ttkcolor_foreground_returns_fg_only_color_or_rst():
    color = TTkColor.fgbg('#112233', '#445566')

    fg_only = color.foreground()

    assert fg_only.fgToRGB() == (17, 34, 51)
    assert not fg_only.hasBackground()

    assert TTkColor.bg('#112233').foreground() is TTkColor.RST


def test_ttkcolor_background_returns_bg_only_color_or_rst():
    color = TTkColor.fgbg('#112233', '#445566')

    bg_only = color.background()

    assert bg_only.bgToRGB() == (68, 85, 102)
    assert not bg_only.hasForeground()

    assert TTkColor.fg('#112233').background() is TTkColor.RST


def test_ttkcolor_has_foreground_background_flags():
    assert TTkColor.fg('#010203').hasForeground()
    assert not TTkColor.fg('#010203').hasBackground()
    assert TTkColor.bg('#040506').hasBackground()
    assert not TTkColor.bg('#040506').hasForeground()


# ---------------------------------------------------------------------------
# Base TTkColor style probes are all False
# ---------------------------------------------------------------------------

def test_ttkcolor_base_modifier_probes_are_false_for_plain_color():
    color = TTkColor.fg('#abcdef')

    assert color.bold() is False
    assert color.italic() is False
    assert color.underline() is False
    assert color.strikethrough() is False
    assert color.blinking() is False


def test_ttkcolor_colortype_reports_fg_bg_and_modifier_bits():
    fg_only = TTkColor.fg('#010203')
    bg_only = TTkColor.bg('#040506')
    with_mod = TTkColor.fg('#070809', modifier=TTkColorGradient(increment=1))

    assert fg_only.colorType() & TTkK.ColorType.Foreground
    assert not (fg_only.colorType() & TTkK.ColorType.Background)

    assert bg_only.colorType() & TTkK.ColorType.Background
    assert not (bg_only.colorType() & TTkK.ColorType.Foreground)

    assert with_mod.colorType() & TTkK.ColorType.ColorModifier


def test_ttkcolor_without_modifiers_strips_modifier_state():
    styled = TTkColor.fgbg('#112233', '#445566') + TTkColor.BOLD + TTkColor.ITALIC

    stripped = styled.withoutModifiers()

    assert stripped.fgToRGB() == (17, 34, 51)
    assert stripped.bgToRGB() == (68, 85, 102)
    assert stripped.bold() is False
    assert stripped.italic() is False


def test_ttkcolor_base_without_modifiers_returns_self():
    plain = TTkColor.fg('#abcdef')

    assert plain.withoutModifiers() is plain


# ---------------------------------------------------------------------------
# RGB <-> HSL conversion paths
# ---------------------------------------------------------------------------

def test_ttkcolor_rgb2hsl_for_grayscale_returns_zero_hue_zero_sat():
    h, s, _ = TTkColor.rgb2hsl((127, 127, 127))

    assert h == 0
    assert s == 0


def test_ttkcolor_rgb2hsl_branches_for_each_max_channel():
    h_r, _, _ = TTkColor.rgb2hsl((200, 50, 50))
    h_g, _, _ = TTkColor.rgb2hsl((50, 200, 50))
    h_b, _, _ = TTkColor.rgb2hsl((50, 50, 200))

    assert 0 <= h_r < 60 or h_r >= 300  # red hue
    assert 90 < h_g < 150
    assert 210 < h_b < 270


def test_ttkcolor_hsl2rgb_covers_each_hue_range():
    # one sample per branch, sanity-check primary channel dominance
    assert TTkColor.hsl2rgb((30, 100, 50))[0] > 0     # 0-60
    assert TTkColor.hsl2rgb((90, 100, 50))[1] > 0     # 60-120
    assert TTkColor.hsl2rgb((150, 100, 50))[1] > 0    # 120-180
    assert TTkColor.hsl2rgb((210, 100, 50))[2] > 0    # 180-240
    assert TTkColor.hsl2rgb((270, 100, 50))[2] > 0    # 240-300
    assert TTkColor.hsl2rgb((330, 100, 50))[0] > 0    # 300-360


# ---------------------------------------------------------------------------
# Hex / RGB inspection
# ---------------------------------------------------------------------------

def test_ttkcolor_get_hex_for_fg_and_bg():
    color = TTkColor.fgbg('#0a0b0c', '#0d0e0f')

    assert color.getHex(TTkK.ColorType.Foreground) == '#0a0b0c'
    assert color.getHex(TTkK.ColorType.Background) == '#0d0e0f'


def test_ttkcolor_fg_bg_to_rgb_default_to_black_when_unset():
    assert TTkColor.bg('#010203').fgToRGB() == (0, 0, 0)
    assert TTkColor.fg('#010203').bgToRGB() == (0, 0, 0)


# ---------------------------------------------------------------------------
# str caching / ansi output
# ---------------------------------------------------------------------------

def test_ttkcolor_str_is_cached_and_stable():
    color = TTkColor.fg('#010203')

    a = str(color)
    b = str(color)

    assert a == b
    assert a != ''


def test_ttkcolor_mod_str_includes_modifier_bytes():
    plain = str(TTkColor.fg('#010203'))
    bold = str(TTkColor.fg('#010203') + TTkColor.BOLD)

    assert bold != plain


def test_ttkcolor_mod_link_str_includes_link_escape():
    linked = TTkColor.fg('#010203', link='https://example.invalid')

    rendered = str(linked)

    assert 'example.invalid' in rendered


# ---------------------------------------------------------------------------
# Operators: __or__ / __add__ / __sub__ / __rsub__
# ---------------------------------------------------------------------------

def test_ttkcolor_or_with_self_returns_self():
    color = TTkColor.fg('#010203')

    assert (color | color) is color


def test_ttkcolor_or_combines_two_colors():
    fg = TTkColor.fg('#010203')
    bg = TTkColor.bg('#040506')

    merged = fg | bg

    assert merged.fgToRGB() == (1, 2, 3)
    assert merged.bgToRGB() == (4, 5, 6)


def test_ttkcolor_add_with_rst_returns_rst():
    color = TTkColor.fg('#010203')

    assert (color + TTkColor.RST) is TTkColor.RST


def test_ttkcolor_sub_emits_clean_ansi_when_channel_appears():
    prev = TTkColor.RST
    curr = TTkColor.fg('#010203')

    diff = curr - prev

    assert isinstance(diff, str)
    assert diff != ''


def test_ttkcolor_sub_emits_full_str_when_no_None_transition():
    a = TTkColor.fg('#010203')
    b = TTkColor.fg('#0a0b0c')

    diff = b - a

    assert diff == str(b)


def test_ttkcolor_sub_emits_clean_ansi_when_bg_appears_from_none():
    fg_only = TTkColor.fg('#010203')
    both = TTkColor.fgbg('#040506', '#070809')

    # `fg_only - both` flips bg from a value back to None → triggers reset path
    diff = fg_only - both

    assert isinstance(diff, str)
    assert diff != str(fg_only)


# ---------------------------------------------------------------------------
# _TTkColor_mod operators
# ---------------------------------------------------------------------------

def test_ttkcolor_mod_eq_against_plain_color_compares_mod_to_zero():
    plain = TTkColor.fg('#010203')
    same_with_no_mod = plain + TTkColor.RST  # collapsed via clean path

    assert (TTkColor.fg('#010203') + TTkColor.BOLD) != plain
    assert same_with_no_mod == plain or same_with_no_mod == TTkColor.RST


def test_ttkcolor_mod_or_with_self_returns_self():
    bold = TTkColor.BOLD

    assert (bold | bold) is bold


def test_ttkcolor_mod_or_combines_with_other_modifiers():
    merged = TTkColor.BOLD | TTkColor.ITALIC

    assert merged.bold()
    assert merged.italic()


def test_ttkcolor_mod_add_with_rst_returns_rst():
    bold = TTkColor.BOLD

    assert (bold + TTkColor.RST) is TTkColor.RST


def test_ttkcolor_mod_radd_combines_with_plain_color():
    # `_TTkColor_mod.__radd__` is reachable directly; combining BOLD with a
    # plain fg color must preserve both the bold flag and the color.
    bold = TTkColor.BOLD
    plain = TTkColor.fg('#010203')

    combined = bold.__radd__(plain)

    assert combined.bold()
    assert combined.fgToRGB() == (1, 2, 3)


def test_ttkcolor_mod_sub_detects_modifier_change():
    a = TTkColor.fg('#010203') + TTkColor.BOLD
    b = TTkColor.fg('#010203')  # no bold

    diff = a - b

    assert isinstance(diff, str)
    assert diff != ''


def test_ttkcolor_mod_sub_same_returns_str_self():
    a = TTkColor.fg('#010203') + TTkColor.BOLD
    b = TTkColor.fg('#010203') + TTkColor.BOLD

    diff = a - b

    assert diff == str(a)


def test_ttkcolor_mod_rsub_produces_clean_reset_string():
    mod = TTkColor.fg('#010203') + TTkColor.BOLD
    plain = TTkColor.fg('#040506')

    diff = mod.__rsub__(plain)

    assert isinstance(diff, str)


def test_ttkcolor_mod_copy_preserves_state():
    src = TTkColor.fg('#010203') + TTkColor.BOLD + TTkColor.ITALIC

    dup = src.copy()

    assert dup.fgToRGB() == src.fgToRGB()
    assert dup.bold() == src.bold()
    assert dup.italic() == src.italic()
    assert dup is not src


def test_ttkcolor_mod_copy_propagates_colormod():
    grad = TTkColorGradient(increment=2)
    src = TTkColor.fg('#010203', modifier=grad) + TTkColor.BOLD

    dup = src.copy()

    assert dup._colorMod is not None
    assert dup.bold()


# ---------------------------------------------------------------------------
# _TTkColor_mod_link operators
# ---------------------------------------------------------------------------

def test_ttkcolor_link_eq_with_non_link_is_false():
    linked = TTkColor.fg('#010203', link='https://x.invalid')
    plain = TTkColor.fg('#010203')

    assert linked != plain


def test_ttkcolor_link_or_with_self_returns_self():
    linked = TTkColor.fg('#010203', link='https://x.invalid')

    assert (linked | linked) is linked


def test_ttkcolor_link_or_keeps_link():
    linked = TTkColor.fg('#010203', link='https://x.invalid')
    other = TTkColor.bg('#040506')

    merged = linked | other

    assert 'x.invalid' in str(merged)


def test_ttkcolor_link_add_with_rst_returns_rst():
    linked = TTkColor.fg('#010203', link='https://x.invalid')

    assert (linked + TTkColor.RST) is TTkColor.RST


def test_ttkcolor_link_sub_detects_link_change():
    a = TTkColor.fg('#010203', link='https://x.invalid')
    b = TTkColor.fg('#010203', link='https://y.invalid')

    diff = a - b

    assert isinstance(diff, str)


def test_ttkcolor_link_sub_same_returns_empty_string():
    a = TTkColor.fg('#010203', link='https://x.invalid')
    b = TTkColor.fg('#010203', link='https://x.invalid')

    diff = a - b

    assert diff == ''


def test_ttkcolor_link_rsub_for_plain_and_mod_other():
    linked = TTkColor.fg('#010203', link='https://x.invalid')
    plain = TTkColor.fg('#040506')
    bold_mod = TTkColor.fg('#040506') + TTkColor.BOLD

    diff_plain = linked.__rsub__(plain)
    diff_mod = linked.__rsub__(bold_mod)

    assert isinstance(diff_plain, str)
    assert isinstance(diff_mod, str)


def test_ttkcolor_link_copy_preserves_link_and_mod():
    src = TTkColor.fg('#010203', link='https://x.invalid') + TTkColor.BOLD

    dup = src.copy()

    assert dup.bold() == src.bold()
    assert dup.fgToRGB() == src.fgToRGB()
    assert 'x.invalid' in str(dup)


def test_ttkcolor_link_copy_propagates_colormod():
    grad = TTkColorGradient(increment=2)
    src = TTkColor.fg('#010203', link='https://x.invalid', modifier=grad)

    dup = src.copy()

    assert dup._colorMod is not None
    assert 'x.invalid' in str(dup)


# ---------------------------------------------------------------------------
# TTkColorGradient
# ---------------------------------------------------------------------------

def test_ttkcolorgradient_independent_fg_bg_increments_when_increment_kw_absent():
    grad = TTkColorGradient(fgincrement=5, bgincrement=-5)
    base = TTkColor.fgbg('#202020', '#404040', modifier=grad)

    shifted = base.mod(0, 1)

    # fg should be brighter (+5), bg should be darker (-5)
    assert shifted.fgToRGB()[0] > base.fgToRGB()[0]
    assert shifted.bgToRGB()[0] < base.bgToRGB()[0]


def test_ttkcolorgradient_cached_value_returned_on_repeated_lookup():
    grad = TTkColorGradient(increment=3)
    base = TTkColor.fg('#404040', modifier=grad)

    first = base.mod(0, 1)
    second = base.mod(0, 1)

    assert first is second


def test_ttkcolorgradient_horizontal_orientation_uses_x_axis():
    grad = TTkColorGradient(increment=5, orientation=TTkK.HORIZONTAL)
    base = TTkColor.fg('#202020', modifier=grad)

    horizontal_step = base.mod(2, 0)
    no_step = base.mod(0, 0)

    assert horizontal_step.fgToRGB() != no_step.fgToRGB()


# ---------------------------------------------------------------------------
# TTkLinearGradient
# ---------------------------------------------------------------------------

def test_ttklineargradient_returns_base_color_before_origin():
    gradient = TTkLinearGradient(
        base_pos=(10, 10), direction=(5, 0),
        target_color=TTkColor.fgbg('#ffffff', '#ffffff'))
    base = TTkColor.fgbg('#000000', '#000000')

    # x=0 is upstream of base_pos along direction → beta<=0
    assert gradient.exec(0, 10, base) is base


def test_ttklineargradient_returns_target_color_past_unit_distance():
    target = TTkColor.fgbg('#ffffff', '#ffffff')
    gradient = TTkLinearGradient(
        base_pos=(0, 0), direction=(1, 0),
        target_color=target)
    base = TTkColor.fgbg('#000000', '#000000')

    # x=10 well past direction length (squared=1) → beta>>1
    assert gradient.exec(10, 0, base) is target


def test_ttklineargradient_interpolates_between_base_and_target():
    target = TTkColor.fgbg('#ffffff', '#ffffff')
    gradient = TTkLinearGradient(
        base_pos=(0, 0), direction=(10, 0),
        target_color=target)
    base = TTkColor.fgbg('#000000', '#000000')

    midpoint = gradient.exec(5, 0, base)

    fr, fg, fb = midpoint.fgToRGB()
    assert 100 < fr < 200
    assert 100 < fg < 200
    assert 100 < fb < 200


def test_ttklineargradient_skips_channel_when_missing_on_either_side():
    # target has fg only, base has bg only → neither channel interpolation
    # condition can be satisfied
    target = TTkColor.fg('#ffffff')
    gradient = TTkLinearGradient(
        base_pos=(0, 0), direction=(10, 0),
        target_color=target)
    base = TTkColor.bg('#000000')

    midpoint = gradient.exec(5, 0, base)

    assert midpoint.bgToRGB() == (0, 0, 0)
    assert midpoint.fgToRGB() == (0, 0, 0)


# ---------------------------------------------------------------------------
# TTkAlternateColor
# ---------------------------------------------------------------------------

def test_ttkalternatecolor_returns_alternate_on_odd_rows():
    from TermTk.TTkCore.color import TTkAlternateColor
    alt = TTkColor.fg('#abcdef')
    mod = TTkAlternateColor(alternateColor=alt)
    base = TTkColor.fg('#010203', modifier=mod)

    odd = base.mod(0, 1)

    assert odd is alt


def test_ttkalternatecolor_returns_base_copy_on_even_rows():
    from TermTk.TTkCore.color import TTkAlternateColor
    alt = TTkColor.fg('#abcdef')
    mod = TTkAlternateColor(alternateColor=alt)
    base = TTkColor.fg('#010203', modifier=mod)

    even = base.mod(0, 0)

    assert even.fgToRGB() == (1, 2, 3)
    assert even is not alt