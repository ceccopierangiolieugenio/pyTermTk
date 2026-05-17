#!/usr/bin/env python
# MIT License
#
# Test demonstrating the fake_canvas fixture helper.

import pytest
import TermTk as ttk


def test_fake_canvas_fixture_default_size(fake_canvas):
    """Test that fake_canvas creates canvas with default dimensions."""
    canvas = fake_canvas()
    width, height = canvas.size()
    assert width == 10, f"Expected default width 10, got {width}"
    assert height == 5, f"Expected default height 5, got {height}"


def test_fake_canvas_fixture_custom_size(fake_canvas):
    """Test that fake_canvas respects custom width and height parameters."""
    canvas = fake_canvas(25, 12)
    width, height = canvas.size()
    assert width == 25, f"Expected width 25, got {width}"
    assert height == 12, f"Expected height 12, got {height}"


def test_fake_canvas_fixture_returns_ttk_canvas(fake_canvas):
    """Test that fake_canvas returns a real TTkCanvas instance."""
    canvas = fake_canvas()
    assert isinstance(canvas, ttk.TTkCanvas), f"Expected TTkCanvas instance, got {type(canvas)}"
    assert hasattr(canvas, 'size'), "TTkCanvas should have a size() method"
