import pytest
import datetime
from unittest.mock import Mock, patch

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.TTkTerm.inputkey import TTkKeyEvent
from TermTk.TTkWidgets.datetime_time import TTkTime, _FieldSelected


class TestTTkTimeKeyEvent:

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.time_widget = TTkTime(time=datetime.time(12, 30, 45))

    def test_tab_navigation_forward(self):
        """Test forward Tab navigation through fields."""
        # Start with NONE, tab to HOURS
        self.time_widget._state.selected = _FieldSelected.NONE
        evt = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Tab, "", TTkK.NoModifier)
        result = self.time_widget.keyEvent(evt)
        assert result is True
        assert self.time_widget._state.selected == _FieldSelected.HOURS

        # From HOURS to MINUTES
        evt = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Tab, "", TTkK.NoModifier)
        result = self.time_widget.keyEvent(evt)
        assert result is True
        assert self.time_widget._state.selected == _FieldSelected.MINUTES

        # From MINUTES to SECONDS
        evt = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Tab, "", TTkK.NoModifier)
        result = self.time_widget.keyEvent(evt)
        assert result is True
        assert self.time_widget._state.selected == _FieldSelected.SECONDS

        # From SECONDS should return False (end of navigation)
        evt = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Tab, "", TTkK.NoModifier)
        result = self.time_widget.keyEvent(evt)
        assert result is False

    def test_tab_navigation_backward(self):
        """Test backward Tab navigation (Shift+Tab) through fields."""
        # Start with NONE, shift+tab to SECONDS
        self.time_widget._state.selected = _FieldSelected.NONE
        evt = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Tab, "", TTkK.ShiftModifier)
        result = self.time_widget.keyEvent(evt)
        assert result is True
        assert self.time_widget._state.selected == _FieldSelected.SECONDS

        # From SECONDS to MINUTES
        evt = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Tab, "", TTkK.ShiftModifier)
        result = self.time_widget.keyEvent(evt)
        assert result is True
        assert self.time_widget._state.selected == _FieldSelected.MINUTES

        # From MINUTES to HOURS
        evt = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Tab, "", TTkK.ShiftModifier)
        result = self.time_widget.keyEvent(evt)
        assert result is True
        assert self.time_widget._state.selected == _FieldSelected.HOURS

        # From HOURS should return False
        evt = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Tab, "", TTkK.ShiftModifier)
        result = self.time_widget.keyEvent(evt)
        assert result is False

    def test_arrow_key_navigation_right(self):
        """Test right arrow navigation through fields."""
        self.time_widget._state.selected = _FieldSelected.HOURS
        evt = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Right, "", TTkK.NoModifier)
        result = self.time_widget.keyEvent(evt)
        assert result is True
        assert self.time_widget._state.selected == _FieldSelected.MINUTES

    def test_arrow_key_navigation_left(self):
        """Test left arrow navigation through fields."""
        self.time_widget._state.selected = _FieldSelected.MINUTES
        evt = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Left, "", TTkK.NoModifier)
        result = self.time_widget.keyEvent(evt)
        assert result is True
        assert self.time_widget._state.selected == _FieldSelected.HOURS

    def test_up_arrow_increment_hours(self):
        """Test up arrow increments hours field."""
        self.time_widget._state.selected = _FieldSelected.HOURS
        initial_time = self.time_widget.time()

        evt = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Up, "", TTkK.NoModifier)
        result = self.time_widget.keyEvent(evt)

        assert result is True
        new_time = self.time_widget.time()
        expected_hour = (initial_time.hour + 1) % 24
        assert new_time.hour == expected_hour

    def test_up_arrow_increment_minutes(self):
        """Test up arrow increments minutes field."""
        self.time_widget._state.selected = _FieldSelected.MINUTES
        initial_time = self.time_widget.time()

        evt = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Up, "", TTkK.NoModifier)
        result = self.time_widget.keyEvent(evt)

        assert result is True
        new_time = self.time_widget.time()
        # Minutes increment by 1, wrapping at 60
        expected_minutes = (initial_time.minute + 1) % 60
        assert new_time.minute == expected_minutes

    def test_up_arrow_increment_seconds(self):
        """Test up arrow increments seconds field."""
        self.time_widget._state.selected = _FieldSelected.SECONDS
        initial_time = self.time_widget.time()

        evt = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Up, "", TTkK.NoModifier)
        result = self.time_widget.keyEvent(evt)

        assert result is True
        new_time = self.time_widget.time()
        expected_seconds = (initial_time.second + 1) % 60
        assert new_time.second == expected_seconds

    def test_down_arrow_decrement_hours(self):
        """Test down arrow decrements hours field."""
        self.time_widget._state.selected = _FieldSelected.HOURS
        initial_time = self.time_widget.time()

        evt = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Down, "", TTkK.NoModifier)
        result = self.time_widget.keyEvent(evt)

        assert result is True
        new_time = self.time_widget.time()
        expected_hour = (initial_time.hour - 1) % 24
        assert new_time.hour == expected_hour

    def test_down_arrow_decrement_minutes(self):
        """Test down arrow decrements minutes field."""
        self.time_widget._state.selected = _FieldSelected.MINUTES
        initial_time = self.time_widget.time()

        evt = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Down, "", TTkK.NoModifier)
        result = self.time_widget.keyEvent(evt)

        assert result is True
        new_time = self.time_widget.time()
        expected_minutes = (initial_time.minute - 1) % 60
        assert new_time.minute == expected_minutes

    def test_down_arrow_decrement_seconds(self):
        """Test down arrow decrements seconds field."""
        self.time_widget._state.selected = _FieldSelected.SECONDS
        initial_time = self.time_widget.time()

        evt = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Down, "", TTkK.NoModifier)
        result = self.time_widget.keyEvent(evt)

        assert result is True
        new_time = self.time_widget.time()
        expected_seconds = (initial_time.second - 1) % 60
        assert new_time.second == expected_seconds

    def test_digit_input_hours_first_digit(self):
        """Test entering first digit in hours field."""
        self.time_widget._state.selected = _FieldSelected.HOURS
        self.time_widget._state.secondDigit = False

        evt = TTkKeyEvent(TTkK.Character, "2", "", TTkK.NoModifier)
        result = self.time_widget.keyEvent(evt)

        assert result is True
        assert self.time_widget.time().hour == 2
        assert self.time_widget._state.secondDigit is True

    def test_digit_input_hours_second_digit(self):
        """Test entering second digit in hours field."""
        self.time_widget.setTime(datetime.time(2, 30, 45))
        self.time_widget._state.selected = _FieldSelected.HOURS
        self.time_widget._state.secondDigit = True

        evt = TTkKeyEvent(TTkK.Character, "3", "", TTkK.NoModifier)
        result = self.time_widget.keyEvent(evt)

        assert result is True
        assert self.time_widget.time().hour == 23
        assert self.time_widget._state.secondDigit is False

    def test_digit_input_hours_max_validation(self):
        """Test hours field validates maximum value (23)."""
        self.time_widget._state.selected = _FieldSelected.HOURS
        self.time_widget._state.secondDigit = True
        self.time_widget.setTime(datetime.time(2, 30, 45))

        evt = TTkKeyEvent(TTkK.Character, "9", "", TTkK.NoModifier)
        result = self.time_widget.keyEvent(evt)

        assert result is True
        # Should be clamped to 23
        assert self.time_widget.time().hour == 23

    def test_digit_input_minutes_first_digit(self):
        """Test entering first digit in minutes field."""
        self.time_widget._state.selected = _FieldSelected.MINUTES
        self.time_widget._state.secondDigit = False

        evt = TTkKeyEvent(TTkK.Character, "5", "", TTkK.NoModifier)
        result = self.time_widget.keyEvent(evt)

        assert result is True
        assert self.time_widget.time().minute == 5
        assert self.time_widget._state.secondDigit is True

    def test_digit_input_minutes_second_digit(self):
        """Test entering second digit in minutes field."""
        self.time_widget.setTime(datetime.time(12, 5, 45))
        self.time_widget._state.selected = _FieldSelected.MINUTES
        self.time_widget._state.secondDigit = True

        evt = TTkKeyEvent(TTkK.Character, "7", "", TTkK.NoModifier)
        result = self.time_widget.keyEvent(evt)

        assert result is True
        assert self.time_widget.time().minute == 57
        assert self.time_widget._state.secondDigit is False

    def test_digit_input_minutes_validation(self):
        """Test minutes field validates maximum value (59)."""
        self.time_widget._state.selected = _FieldSelected.MINUTES
        self.time_widget._state.secondDigit = True
        self.time_widget.setTime(datetime.time(12, 6, 45))

        evt = TTkKeyEvent(TTkK.Character, "9", "", TTkK.NoModifier)
        result = self.time_widget.keyEvent(evt)

        assert result is True
        # Should be clamped to 59
        assert self.time_widget.time().minute == 59

    def test_digit_input_seconds_first_digit(self):
        """Test entering first digit in seconds field."""
        self.time_widget._state.selected = _FieldSelected.SECONDS
        self.time_widget._state.secondDigit = False

        evt = TTkKeyEvent(TTkK.Character, "3", "", TTkK.NoModifier)
        result = self.time_widget.keyEvent(evt)

        assert result is True
        assert self.time_widget.time().second == 3
        assert self.time_widget._state.secondDigit is True

    def test_digit_input_seconds_second_digit(self):
        """Test entering second digit in seconds field."""
        self.time_widget.setTime(datetime.time(12, 30, 4))
        self.time_widget._state.selected = _FieldSelected.SECONDS
        self.time_widget._state.secondDigit = True

        evt = TTkKeyEvent(TTkK.Character, "2", "", TTkK.NoModifier)
        result = self.time_widget.keyEvent(evt)

        assert result is True
        assert self.time_widget.time().second == 42
        assert self.time_widget._state.secondDigit is False

    def test_digit_input_seconds_validation(self):
        """Test seconds field validates maximum value (59)."""
        self.time_widget._state.selected = _FieldSelected.SECONDS
        self.time_widget._state.secondDigit = True
        self.time_widget.setTime(datetime.time(12, 30, 6))

        evt = TTkKeyEvent(TTkK.Character, "9", "", TTkK.NoModifier)
        result = self.time_widget.keyEvent(evt)

        assert result is True
        # Should be clamped to 59
        assert self.time_widget.time().second == 59

    def test_delete_key_clears_hours(self):
        """Test Delete key clears hours field."""
        self.time_widget._state.selected = _FieldSelected.HOURS

        evt = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Delete, "", TTkK.NoModifier)
        result = self.time_widget.keyEvent(evt)

        assert result is True
        assert self.time_widget.time().hour == 0

    def test_delete_key_clears_minutes(self):
        """Test Delete key clears minutes field."""
        self.time_widget._state.selected = _FieldSelected.MINUTES

        evt = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Delete, "", TTkK.NoModifier)
        result = self.time_widget.keyEvent(evt)

        assert result is True
        assert self.time_widget.time().minute == 0

    def test_delete_key_clears_seconds(self):
        """Test Delete key clears seconds field."""
        self.time_widget._state.selected = _FieldSelected.SECONDS

        evt = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Delete, "", TTkK.NoModifier)
        result = self.time_widget.keyEvent(evt)

        assert result is True
        assert self.time_widget.time().second == 0

    def test_backspace_key_clears_hours(self):
        """Test Backspace key clears hours field."""
        self.time_widget._state.selected = _FieldSelected.HOURS

        evt = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Backspace, "", TTkK.NoModifier)
        result = self.time_widget.keyEvent(evt)

        assert result is True
        assert self.time_widget.time().hour == 0

    def test_backspace_key_clears_minutes(self):
        """Test Backspace key clears minutes field."""
        self.time_widget._state.selected = _FieldSelected.MINUTES

        evt = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Backspace, "", TTkK.NoModifier)
        result = self.time_widget.keyEvent(evt)

        assert result is True
        assert self.time_widget.time().minute == 0

    def test_backspace_key_clears_seconds(self):
        """Test Backspace key clears seconds field."""
        self.time_widget._state.selected = _FieldSelected.SECONDS

        evt = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Backspace, "", TTkK.NoModifier)
        result = self.time_widget.keyEvent(evt)

        assert result is True
        assert self.time_widget.time().second == 0

    def test_enter_key_deselects_field(self):
        """Test Enter key deselects current field."""
        self.time_widget._state.selected = _FieldSelected.HOURS

        evt = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Enter, "", TTkK.NoModifier)
        result = self.time_widget.keyEvent(evt)

        assert result is True
        assert self.time_widget._state.selected == _FieldSelected.NONE

    def test_time_overflow_hours_23_to_0(self):
        """Test hour overflow (23:59:59 + 1 hour -> 0:59:59)."""
        self.time_widget.setTime(datetime.time(23, 59, 59))
        self.time_widget._state.selected = _FieldSelected.HOURS

        evt = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Up, "", TTkK.NoModifier)
        result = self.time_widget.keyEvent(evt)

        assert result is True
        # Should wrap to 0:59:59 (next day boundary)
        assert self.time_widget.time().hour == 23
        assert self.time_widget.time().minute == 59
        assert self.time_widget.time().second == 59

    def test_time_underflow_hours_0_to_23(self):
        """Test hour underflow (0:0:0 - 1 hour -> 23:0:0)."""
        self.time_widget.setTime(datetime.time(0, 0, 0))
        self.time_widget._state.selected = _FieldSelected.HOURS

        evt = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Down, "", TTkK.NoModifier)
        result = self.time_widget.keyEvent(evt)

        assert result is True
        # Should wrap to 23:0:0 (previous day boundary)
        assert self.time_widget.time().hour == 0
        assert self.time_widget.time().minute == 0
        assert self.time_widget.time().second == 0

    def test_time_overflow_minutes_59_to_0(self):
        """Test minute overflow (12:59:30 + 1 minute -> 13:0:30)."""
        self.time_widget.setTime(datetime.time(12, 59, 30))
        self.time_widget._state.selected = _FieldSelected.MINUTES

        evt = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Up, "", TTkK.NoModifier)
        result = self.time_widget.keyEvent(evt)

        assert result is True
        # Should increment hour and reset minutes
        assert self.time_widget.time().hour == 13
        assert self.time_widget.time().minute == 0
        assert self.time_widget.time().second == 30

    def test_time_overflow_seconds_59_to_0(self):
        """Test second overflow (12:30:59 + 1 second -> 12:31:0)."""
        self.time_widget.setTime(datetime.time(12, 30, 59))
        self.time_widget._state.selected = _FieldSelected.SECONDS

        evt = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Up, "", TTkK.NoModifier)
        result = self.time_widget.keyEvent(evt)

        assert result is True
        # Should increment minute and reset seconds
        assert self.time_widget.time().hour == 12
        assert self.time_widget.time().minute == 31
        assert self.time_widget.time().second == 0

    # def test_no_field_selected_up_down_returns_false(self):
    #     """Test up/down keys return False when no field is selected."""
    #     self.time_widget._state.selected = _FieldSelected.NONE

    #     evt_up = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Up, "", TTkK.NoModifier)
    #     result_up = self.time_widget.keyEvent(evt_up)
    #     assert result_up is False

    #     evt_down = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Down, "", TTkK.NoModifier)
    #     result_down = self.time_widget.keyEvent(evt_down)
    #     assert result_down is False

    def test_non_digit_character_returns_true(self):
        """Test non-digit character input returns True but doesn't change time."""
        self.time_widget._state.selected = _FieldSelected.HOURS
        initial_time = self.time_widget.time()

        evt = TTkKeyEvent(TTkK.Character, "a", "", TTkK.NoModifier)
        result = self.time_widget.keyEvent(evt)

        assert result is True
        assert self.time_widget.time() == initial_time

    def test_digit_input_no_field_selected(self):
        """Test digit input when no field is selected returns True but no change."""
        self.time_widget._state.selected = _FieldSelected.NONE
        initial_time = self.time_widget.time()

        evt = TTkKeyEvent(TTkK.Character, "5", "", TTkK.NoModifier)
        result = self.time_widget.keyEvent(evt)

        assert result is True
        assert self.time_widget.time() == initial_time

    @patch.object(TTkTime, 'update')
    def test_update_called_on_navigation(self, mock_update):
        """Test that update is called during navigation."""
        self.time_widget._state.selected = _FieldSelected.NONE

        evt = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Tab, "", TTkK.NoModifier)
        self.time_widget.keyEvent(evt)

        mock_update.assert_called()

    @patch.object(TTkTime, 'update')
    def test_update_called_on_time_change(self, mock_update):
        """Test that update is called when time changes."""
        self.time_widget._state.selected = _FieldSelected.HOURS

        evt = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Up, "", TTkK.NoModifier)
        self.time_widget.keyEvent(evt)

        mock_update.assert_called()

    def test_second_digit_reset_on_special_keys(self):
        """Test that secondDigit is reset when special keys are pressed."""
        self.time_widget._state.secondDigit = True
        self.time_widget._state.selected = _FieldSelected.HOURS

        evt = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Up, "", TTkK.NoModifier)
        self.time_widget.keyEvent(evt)

        assert self.time_widget._state.secondDigit is False

    def test_second_digit_toggle_on_digit_input(self):
        """Test that secondDigit toggles correctly on digit input."""
        self.time_widget._state.selected = _FieldSelected.HOURS
        self.time_widget._state.secondDigit = False

        # First digit input
        evt = TTkKeyEvent(TTkK.Character, "1", "", TTkK.NoModifier)
        self.time_widget.keyEvent(evt)
        assert self.time_widget._state.secondDigit is True

        # Second digit input
        evt = TTkKeyEvent(TTkK.Character, "5", "", TTkK.NoModifier)
        self.time_widget.keyEvent(evt)
        assert self.time_widget._state.secondDigit is False

    def test_unknown_special_key_returns_false(self):
        """Test unknown special keys return False."""
        self.time_widget._state.selected = _FieldSelected.HOURS

        evt = TTkKeyEvent(TTkK.SpecialKey, 9999, "", TTkK.NoModifier)  # Unknown key
        result = self.time_widget.keyEvent(evt)

        assert result is False

    def test_time_changed_signal_emission(self):
        """Test that timeChanged signal is emitted when time changes."""
        signal_received = []

        def slot(time_value):
            signal_received.append(time_value)

        self.time_widget.timeChanged.connect(slot)
        self.time_widget._state.selected = _FieldSelected.HOURS

        evt = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Up, "", TTkK.NoModifier)
        self.time_widget.keyEvent(evt)

        assert len(signal_received) == 1
        assert isinstance(signal_received[0], datetime.time)

    def test_boundary_digit_input_hours(self):
        """Test digit input at hours boundaries."""
        # Test hour 24 gets clamped to 23
        self.time_widget._state.selected = _FieldSelected.HOURS
        self.time_widget._state.secondDigit = True
        self.time_widget.setTime(datetime.time(2, 30, 45))

        evt = TTkKeyEvent(TTkK.Character, "4", "", TTkK.NoModifier)
        result = self.time_widget.keyEvent(evt)

        assert result is True
        assert self.time_widget.time().hour == 23  # Should be clamped

    def test_boundary_digit_input_minutes(self):
        """Test digit input at minutes boundaries."""
        # Test minute 60 gets clamped to 59
        self.time_widget._state.selected = _FieldSelected.MINUTES
        self.time_widget._state.secondDigit = True
        self.time_widget.setTime(datetime.time(12, 6, 45))

        evt = TTkKeyEvent(TTkK.Character, "0", "", TTkK.NoModifier)
        result = self.time_widget.keyEvent(evt)

        assert result is True
        assert self.time_widget.time().minute == 59  # Should be clamped

    def test_boundary_digit_input_seconds(self):
        """Test digit input at seconds boundaries."""
        # Test second 60 gets clamped to 59
        self.time_widget._state.selected = _FieldSelected.SECONDS
        self.time_widget._state.secondDigit = True
        self.time_widget.setTime(datetime.time(12, 30, 6))

        evt = TTkKeyEvent(TTkK.Character, "0", "", TTkK.NoModifier)
        result = self.time_widget.keyEvent(evt)

        assert result is True
        assert self.time_widget.time().second == 59  # Should be clamped