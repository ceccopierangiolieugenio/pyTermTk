import pytest
import datetime
import calendar
from unittest.mock import Mock, patch, MagicMock

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.TTkTerm.inputkey import TTkKeyEvent
from TermTk.TTkCore.TTkTerm.inputmouse import TTkMouseEvent
from TermTk.TTkWidgets.datetime_date import TTkDate, _FieldSelected, _TTkTimeWidgetState


class TestTTkDateFieldSelected:
    """Test _FieldSelected enum values."""

    def test_field_selected_values(self):
        """Test that _FieldSelected enum has expected values."""
        assert _FieldSelected.NONE == 1
        assert _FieldSelected.YEARS == 2
        assert _FieldSelected.MONTHS == 3
        assert _FieldSelected.DAYS == 4
        assert _FieldSelected.CAL == 5


class TestTTkTimeWidgetState:
    """Test _TTkTimeWidgetState dataclass."""

    def setup_method(self):
        """Set up test fixtures."""
        self.state = _TTkTimeWidgetState()

    def test_default_state(self):
        """Test default state initialization."""
        assert self.state.selected == _FieldSelected.NONE
        assert self.state.hovered == _FieldSelected.NONE
        assert self.state.digit == 0

    def test_clear_state(self):
        """Test state clearing functionality."""
        # Set some values
        self.state.selected = _FieldSelected.YEARS
        self.state.hovered = _FieldSelected.MONTHS
        self.state.digit = 2

        # Clear and verify
        self.state.clear()
        assert self.state.selected == _FieldSelected.NONE
        assert self.state.hovered == _FieldSelected.NONE
        assert self.state.digit == 0


class TestTTkDateStaticMethods:
    """Test static methods of TTkDate."""

    def test_get_field_from_pos_years(self):
        """Test field detection for years position."""
        # Years field spans positions 0-3
        assert TTkDate._getFieldFromPos(0, 0) == _FieldSelected.YEARS
        assert TTkDate._getFieldFromPos(3, 0) == _FieldSelected.YEARS

    def test_get_field_from_pos_months(self):
        """Test field detection for months position."""
        # Months field spans positions 5-6
        assert TTkDate._getFieldFromPos(5, 0) == _FieldSelected.MONTHS
        assert TTkDate._getFieldFromPos(6, 0) == _FieldSelected.MONTHS

    def test_get_field_from_pos_days(self):
        """Test field detection for days position."""
        # Days field spans positions 8-9
        assert TTkDate._getFieldFromPos(8, 0) == _FieldSelected.DAYS
        assert TTkDate._getFieldFromPos(9, 0) == _FieldSelected.DAYS

    def test_get_field_from_pos_calendar(self):
        """Test field detection for calendar button position."""
        # Calendar button spans positions 11-12
        assert TTkDate._getFieldFromPos(11, 0) == _FieldSelected.CAL
        assert TTkDate._getFieldFromPos(12, 0) == _FieldSelected.CAL

    def test_get_field_from_pos_separators(self):
        """Test field detection for separator positions."""
        # Separators should return NONE
        assert TTkDate._getFieldFromPos(4, 0) == _FieldSelected.NONE  # First separator
        assert TTkDate._getFieldFromPos(7, 0) == _FieldSelected.NONE  # Second separator
        assert TTkDate._getFieldFromPos(10, 0) == _FieldSelected.NONE # Space before calendar

    def test_get_field_from_pos_wrong_row(self):
        """Test field detection returns NONE for non-zero rows."""
        assert TTkDate._getFieldFromPos(0, 1) == _FieldSelected.NONE
        assert TTkDate._getFieldFromPos(5, -1) == _FieldSelected.NONE

    def test_get_field_from_pos_out_of_bounds(self):
        """Test field detection for out-of-bounds positions."""
        assert TTkDate._getFieldFromPos(-1, 0) == _FieldSelected.NONE
        assert TTkDate._getFieldFromPos(13, 0) == _FieldSelected.NONE


class TestTTkDateInit:
    """Test TTkDate initialization."""

    def test_init_default_date(self):
        """Test initialization with default (today's) date."""
        widget = TTkDate()
        today = datetime.date.today()
        assert widget.date() == today

    def test_init_with_date(self):
        """Test initialization with specific date."""
        test_date = datetime.date(2023, 6, 15)
        widget = TTkDate(date=test_date)
        assert widget.date() == test_date

    def test_init_signal_creation(self):
        """Test that dateChanged signal is created."""
        widget = TTkDate()
        assert hasattr(widget, 'dateChanged')

    def test_init_ordinal_bounds(self):
        """Test that ordinal bounds are set correctly."""
        widget = TTkDate()
        expected_min = datetime.date(1900, 1, 1).toordinal()
        expected_max = datetime.date(2100, 12, 31).toordinal()
        assert widget._minOrdinal == expected_min
        assert widget._maxOrdinal == expected_max

    def test_init_focus_policy(self):
        """Test that focus policy is set correctly."""
        widget = TTkDate()
        assert widget.focusPolicy() & TTkK.ClickFocus
        assert widget.focusPolicy() & TTkK.TabFocus


class TestTTkDateCore:
    """Test core TTkDate functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.test_date = datetime.date(2023, 6, 15)
        self.widget = TTkDate(date=self.test_date)

    def test_date_getter(self):
        """Test date() getter method."""
        assert self.widget.date() == self.test_date

    def test_set_date_updates_internal_date(self):
        """Test setDate() updates internal date."""
        new_date = datetime.date(2024, 12, 25)
        self.widget.setDate(new_date)
        assert self.widget.date() == new_date

    @patch.object(TTkDate, 'update')
    def test_set_date_calls_update(self, mock_update):
        """Test setDate() calls update() when date changes."""
        new_date = datetime.date(2024, 1, 1)
        self.widget.setDate(new_date)
        mock_update.assert_called_once()

    def test_set_date_emits_signal(self):
        """Test setDate() emits dateChanged signal."""
        signal_received = []

        def slot(date_value):
            signal_received.append(date_value)

        self.widget.dateChanged.connect(slot)
        new_date = datetime.date(2024, 3, 10)
        self.widget.setDate(new_date)

        assert len(signal_received) == 1
        assert signal_received[0] == new_date

    def test_set_date_same_date_no_signal(self):
        """Test setDate() with same date doesn't emit signal."""
        signal_received = []

        def slot(date_value):
            signal_received.append(date_value)

        self.widget.dateChanged.connect(slot)
        self.widget.setDate(self.test_date)  # Same date

        assert len(signal_received) == 0

    def test_add_delta_positive(self):
        """Test _addDelta() with positive delta."""
        initial_ordinal = self.test_date.toordinal()
        self.widget._addDelta(10)
        expected_date = datetime.date.fromordinal(initial_ordinal + 10)
        assert self.widget.date() == expected_date

    def test_add_delta_negative(self):
        """Test _addDelta() with negative delta."""
        initial_ordinal = self.test_date.toordinal()
        self.widget._addDelta(-5)
        expected_date = datetime.date.fromordinal(initial_ordinal - 5)
        assert self.widget.date() == expected_date

    def test_add_delta_zero(self):
        """Test _addDelta() with zero delta doesn't change date."""
        initial_date = self.widget.date()
        self.widget._addDelta(0)
        assert self.widget.date() == initial_date

    def test_add_delta_min_bound(self):
        """Test _addDelta() respects minimum date bound."""
        # Set date near minimum bound
        min_date = datetime.date(1900, 1, 5)
        self.widget.setDate(min_date)

        # Try to go below minimum
        self.widget._addDelta(-10)

        # Should be clamped to minimum
        expected_min = datetime.date.fromordinal(self.widget._minOrdinal)
        assert self.widget.date() == expected_min

    def test_add_delta_max_bound(self):
        """Test _addDelta() respects maximum date bound."""
        # Set date near maximum bound
        max_date = datetime.date(2100, 12, 25)
        self.widget.setDate(max_date)

        # Try to go above maximum
        self.widget._addDelta(10)

        # Should be clamped to maximum
        expected_max = datetime.date.fromordinal(self.widget._maxOrdinal)
        assert self.widget.date() == expected_max

    def test_focus_out_event_clears_state(self):
        """Test focusOutEvent() clears widget state."""
        # Set some state
        self.widget._state.selected = _FieldSelected.YEARS
        self.widget._state.hovered = _FieldSelected.MONTHS
        self.widget._state.digit = 2

        # Focus out
        self.widget.focusOutEvent()

        # Verify state is cleared
        assert self.widget._state.selected == _FieldSelected.NONE
        assert self.widget._state.hovered == _FieldSelected.NONE
        assert self.widget._state.digit == 0


class TestTTkDateMouseEvents:
    """Test mouse event handling."""

    def setup_method(self):
        """Set up test fixtures."""
        self.widget = TTkDate(date=datetime.date(2023, 6, 15))

    @patch.object(TTkDate, 'update')
    def test_mouse_press_event_selects_field(self, mock_update):
        """Test mousePressEvent() selects correct field."""
        evt = TTkMouseEvent(0, 0, TTkMouseEvent.Press, TTkMouseEvent.LeftButton, TTkK.NoModifier, 1, '')
        result = self.widget.mousePressEvent(evt)

        assert result is True
        assert self.widget._state.selected == _FieldSelected.YEARS
        mock_update.assert_called_once()

    def test_mouse_press_event_clears_state(self):
        """Test mousePressEvent() clears existing state."""
        # Set some state first
        self.widget._state.hovered = _FieldSelected.DAYS
        self.widget._state.digit = 3

        evt = TTkMouseEvent(5, 0, TTkMouseEvent.Press, TTkMouseEvent.LeftButton, TTkK.NoModifier, 1, '')
        self.widget.mousePressEvent(evt)

        assert self.widget._state.selected == _FieldSelected.MONTHS
        assert self.widget._state.digit == 0

    @patch.object(TTkDate, '_showForm')
    def test_mouse_press_calendar_shows_form(self, mock_show_form):
        """Test clicking calendar button shows form."""
        evt = TTkMouseEvent(11, 0, TTkMouseEvent.Press, TTkMouseEvent.LeftButton, TTkK.NoModifier, 1, '')
        self.widget.mousePressEvent(evt)

        assert self.widget._state.selected == _FieldSelected.CAL
        mock_show_form.assert_called_once()

    @patch.object(TTkDate, 'update')
    def test_mouse_move_event_sets_hover(self, mock_update):
        """Test mouseMoveEvent() sets hover state."""
        evt = TTkMouseEvent(8, 0, TTkK.Move, TTkK.NoButton, TTkK.NoModifier, 1, '')
        result = self.widget.mouseMoveEvent(evt)

        assert result is True
        assert self.widget._state.hovered == _FieldSelected.DAYS
        mock_update.assert_called_once()


class TestTTkDateKeyEvents:
    """Test keyboard event handling."""

    def setup_method(self):
        """Set up test fixtures."""
        self.widget = TTkDate(date=datetime.date(2023, 6, 15))

    def test_tab_navigation_forward(self):
        """Test forward Tab navigation through fields."""
        # Start with NONE, tab to YEARS
        self.widget._state.selected = _FieldSelected.NONE
        evt = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Tab, "", TTkK.NoModifier)
        result = self.widget.keyEvent(evt)
        assert result is True
        assert self.widget._state.selected == _FieldSelected.YEARS

        # From YEARS to MONTHS
        evt = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Tab, "", TTkK.NoModifier)
        result = self.widget.keyEvent(evt)
        assert result is True
        assert self.widget._state.selected == _FieldSelected.MONTHS

        # From MONTHS to DAYS
        evt = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Tab, "", TTkK.NoModifier)
        result = self.widget.keyEvent(evt)
        assert result is True
        assert self.widget._state.selected == _FieldSelected.DAYS

        # From DAYS to CAL
        evt = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Tab, "", TTkK.NoModifier)
        result = self.widget.keyEvent(evt)
        assert result is True
        assert self.widget._state.selected == _FieldSelected.CAL

        # From CAL should return False
        evt = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Tab, "", TTkK.NoModifier)
        result = self.widget.keyEvent(evt)
        assert result is False

    def test_tab_navigation_backward(self):
        """Test backward Tab navigation (Shift+Tab)."""
        # Start with NONE, shift+tab to CAL
        self.widget._state.selected = _FieldSelected.NONE
        evt = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Tab, "", TTkK.ShiftModifier)
        result = self.widget.keyEvent(evt)
        assert result is True
        assert self.widget._state.selected == _FieldSelected.CAL

        # From CAL to DAYS
        evt = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Tab, "", TTkK.ShiftModifier)
        result = self.widget.keyEvent(evt)
        assert result is True
        assert self.widget._state.selected == _FieldSelected.DAYS

        # From DAYS to MONTHS
        evt = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Tab, "", TTkK.ShiftModifier)
        result = self.widget.keyEvent(evt)
        assert result is True
        assert self.widget._state.selected == _FieldSelected.MONTHS

        # From MONTHS to YEARS
        evt = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Tab, "", TTkK.ShiftModifier)
        result = self.widget.keyEvent(evt)
        assert result is True
        assert self.widget._state.selected == _FieldSelected.YEARS

        # From YEARS should return False
        evt = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Tab, "", TTkK.ShiftModifier)
        result = self.widget.keyEvent(evt)
        assert result is False

    def test_arrow_navigation_right(self):
        """Test right arrow navigation."""
        self.widget._state.selected = _FieldSelected.YEARS
        evt = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Right, "", TTkK.NoModifier)
        result = self.widget.keyEvent(evt)
        assert result is True
        assert self.widget._state.selected == _FieldSelected.MONTHS

    def test_arrow_navigation_left(self):
        """Test left arrow navigation."""
        self.widget._state.selected = _FieldSelected.MONTHS
        evt = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Left, "", TTkK.NoModifier)
        result = self.widget.keyEvent(evt)
        assert result is True
        assert self.widget._state.selected == _FieldSelected.YEARS

    @patch.object(TTkDate, '_showForm')
    def test_calendar_field_special_keys_show_form(self, mock_show_form):
        """Test special keys in calendar field show form."""
        self.widget._state.selected = _FieldSelected.CAL

        for key in (TTkK.Key_Up, TTkK.Key_Down, TTkK.Key_Enter):
            mock_show_form.reset_mock()
            evt = TTkKeyEvent(TTkK.SpecialKey, key, "", TTkK.NoModifier)
            result = self.widget.keyEvent(evt)
            assert result is True
            mock_show_form.assert_called_once()

    def test_up_arrow_increment_years(self):
        """Test up arrow increments years."""
        initial_date = self.widget.date()
        self.widget._state.selected = _FieldSelected.YEARS

        evt = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Up, "", TTkK.NoModifier)
        result = self.widget.keyEvent(evt)

        assert result is True
        new_date = self.widget.date()
        # Year increment should add 365 or 366 days depending on leap year
        days_in_year = 366 if calendar.isleap(initial_date.year) else 365
        expected_ordinal = initial_date.toordinal() + days_in_year
        assert new_date.toordinal() == expected_ordinal

    def test_up_arrow_increment_months(self):
        """Test up arrow increments months (adds ~30 days)."""
        initial_date = self.widget.date()
        self.widget._state.selected = _FieldSelected.MONTHS

        evt = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Up, "", TTkK.NoModifier)
        result = self.widget.keyEvent(evt)

        assert result is True
        new_date = self.widget.date()
        expected_ordinal = initial_date.toordinal() + 30
        assert new_date.toordinal() == expected_ordinal

    def test_up_arrow_increment_days(self):
        """Test up arrow increments days."""
        initial_date = self.widget.date()
        self.widget._state.selected = _FieldSelected.DAYS

        evt = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Up, "", TTkK.NoModifier)
        result = self.widget.keyEvent(evt)

        assert result is True
        new_date = self.widget.date()
        expected_ordinal = initial_date.toordinal() + 1
        assert new_date.toordinal() == expected_ordinal

    def test_down_arrow_decrement_years(self):
        """Test down arrow decrements years."""
        initial_date = self.widget.date()
        self.widget._state.selected = _FieldSelected.YEARS

        evt = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Down, "", TTkK.NoModifier)
        result = self.widget.keyEvent(evt)

        assert result is True
        new_date = self.widget.date()
        days_in_year = 366 if calendar.isleap(initial_date.year) else 365
        expected_ordinal = initial_date.toordinal() - days_in_year
        assert new_date.toordinal() == expected_ordinal

    def test_delete_clears_years(self):
        """Test Delete key clears years field."""
        self.widget._state.selected = _FieldSelected.YEARS

        evt = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Delete, "", TTkK.NoModifier)
        result = self.widget.keyEvent(evt)

        assert result is True
        assert self.widget.date().year == 1900

    def test_delete_clears_months(self):
        """Test Delete key clears months field."""
        self.widget._state.selected = _FieldSelected.MONTHS

        evt = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Delete, "", TTkK.NoModifier)
        result = self.widget.keyEvent(evt)

        assert result is True
        assert self.widget.date().month == 1

    def test_delete_clears_days(self):
        """Test Delete key clears days field."""
        self.widget._state.selected = _FieldSelected.DAYS

        evt = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Delete, "", TTkK.NoModifier)
        result = self.widget.keyEvent(evt)

        assert result is True
        assert self.widget.date().day == 1

    def test_backspace_clears_fields(self):
        """Test Backspace key clears fields same as Delete."""
        self.widget._state.selected = _FieldSelected.YEARS

        evt = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Backspace, "", TTkK.NoModifier)
        result = self.widget.keyEvent(evt)

        assert result is True
        assert self.widget.date().year == 1900

    def test_enter_deselects_field(self):
        """Test Enter key deselects current field."""
        self.widget._state.selected = _FieldSelected.YEARS

        evt = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Enter, "", TTkK.NoModifier)
        result = self.widget.keyEvent(evt)

        assert result is True
        assert self.widget._state.selected == _FieldSelected.NONE

    def test_digit_input_years_first_digit(self):
        """Test entering first digit in years field."""
        self.widget._state.selected = _FieldSelected.YEARS
        self.widget._state.digit = 0

        evt = TTkKeyEvent(TTkK.Character, "2", "", TTkK.NoModifier)
        result = self.widget.keyEvent(evt)

        assert result is True
        assert self.widget.date().year == 2000  # 2 * 10^3
        assert self.widget._state.digit == 1

    def test_digit_input_years_four_digits(self):
        """Test entering all four digits in years field."""
        self.widget._state.selected = _FieldSelected.YEARS
        self.widget._state.digit = 0

        # Enter 2024
        for i, digit in enumerate("2024"):
            evt = TTkKeyEvent(TTkK.Character, digit, "", TTkK.NoModifier)
            self.widget.keyEvent(evt)
            assert self.widget._state.digit == (i + 1) % 4

        assert self.widget.date().year == 2024

    def test_digit_input_years_bounds(self):
        """Test years digit input respects bounds (1900-2100)."""
        self.widget._state.selected = _FieldSelected.YEARS
        self.widget._state.digit = 0

        # Try to enter 1899 (below minimum)
        for digit in "1899":
            evt = TTkKeyEvent(TTkK.Character, digit, "", TTkK.NoModifier)
            self.widget.keyEvent(evt)

        assert self.widget.date().year == 1999  # Should be clamped to minimum

        # Reset and try 2101 (above maximum)
        self.widget._state.digit = 0
        for digit in "2101":
            evt = TTkKeyEvent(TTkK.Character, digit, "", TTkK.NoModifier)
            self.widget.keyEvent(evt)

        assert self.widget.date().year == 2100  # Should be clamped to maximum

    def test_digit_input_months_first_digit(self):
        """Test entering first digit in months field."""
        self.widget._state.selected = _FieldSelected.MONTHS
        self.widget._state.digit = 0

        evt = TTkKeyEvent(TTkK.Character, "1", "", TTkK.NoModifier)
        result = self.widget.keyEvent(evt)

        assert result is True
        assert self.widget.date().month == 1
        assert self.widget._state.digit == 1

    def test_digit_input_months_two_digits(self):
        """Test entering two digits in months field."""
        self.widget._state.selected = _FieldSelected.MONTHS
        self.widget._state.digit = 0

        # Enter 12
        evt = TTkKeyEvent(TTkK.Character, "1", "", TTkK.NoModifier)
        self.widget.keyEvent(evt)
        evt = TTkKeyEvent(TTkK.Character, "2", "", TTkK.NoModifier)
        self.widget.keyEvent(evt)

        assert self.widget.date().month == 12
        assert self.widget._state.digit == 0  # Should wrap to 0

    def test_digit_input_months_bounds(self):
        """Test months digit input respects bounds (1-12)."""
        self.widget._state.selected = _FieldSelected.MONTHS
        self.widget._state.digit = 1  # Second digit

        # Try to enter 13 (month 1 + digit 3 = 13, should clamp to 12)
        self.widget.setDate(datetime.date(2023, 1, 15))  # Set month to 1
        evt = TTkKeyEvent(TTkK.Character, "3", "", TTkK.NoModifier)
        self.widget.keyEvent(evt)

        assert self.widget.date().month == 12  # Should be clamped

    def test_digit_input_days_bounds(self):
        """Test days digit input respects month-specific bounds."""
        # Test February in non-leap year
        self.widget.setDate(datetime.date(2023, 2, 1))  # February 2023 (28 days)
        self.widget._state.selected = _FieldSelected.DAYS
        self.widget._state.digit = 0  # Second digit

        # Try to enter 29 (day 2 + digit 9 = 29, should clamp to 28)
        evt = TTkKeyEvent(TTkK.Character, "2", "", TTkK.NoModifier)
        self.widget.keyEvent(evt)
        evt = TTkKeyEvent(TTkK.Character, "9", "", TTkK.NoModifier)
        self.widget.keyEvent(evt)

        assert self.widget.date().day == 28  # Should be clamped to February limit

    def test_digit_input_days_leap_year(self):
        """Test days input in leap year February."""
        # Test February in leap year
        self.widget.setDate(datetime.date(2024, 2, 1))  # February 2024 (leap year, 29 days)
        self.widget._state.selected = _FieldSelected.DAYS
        self.widget._state.digit = 0  # Second digit

        # Enter 29
        evt = TTkKeyEvent(TTkK.Character, "2", "", TTkK.NoModifier)
        self.widget.keyEvent(evt)
        evt = TTkKeyEvent(TTkK.Character, "9", "", TTkK.NoModifier)
        self.widget.keyEvent(evt)

        assert self.widget.date().day == 29  # Should be allowed in leap year

    @patch.object(TTkDate, '_showForm')
    def test_character_input_calendar_field_shows_form(self, mock_show_form):
        """Test character input in calendar field shows form."""
        self.widget._state.selected = _FieldSelected.CAL

        evt = TTkKeyEvent(TTkK.Character, "x", "", TTkK.NoModifier)
        result = self.widget.keyEvent(evt)

        assert result is True
        mock_show_form.assert_called_once()

    def test_special_key_resets_digit(self):
        """Test that special keys reset the digit counter."""
        self.widget._state.selected = _FieldSelected.YEARS
        self.widget._state.digit = 3

        evt = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Up, "", TTkK.NoModifier)
        self.widget.keyEvent(evt)

        assert self.widget._state.digit == 0

    def test_unknown_special_key_returns_false(self):
        """Test unknown special keys return False."""
        self.widget._state.selected = _FieldSelected.YEARS

        evt = TTkKeyEvent(TTkK.SpecialKey, 9999, "", TTkK.NoModifier)  # Unknown key
        result = self.widget.keyEvent(evt)

        assert result is False

    def test_non_digit_character_returns_true(self):
        """Test non-digit character input returns True but doesn't change date."""
        self.widget._state.selected = _FieldSelected.YEARS
        initial_date = self.widget.date()

        evt = TTkKeyEvent(TTkK.Character, "a", "", TTkK.NoModifier)
        result = self.widget.keyEvent(evt)

        assert result is True
        assert self.widget.date() == initial_date


class TestTTkDateWheelEvents:
    """Test wheel event handling."""

    def setup_method(self):
        """Set up test fixtures."""
        self.widget = TTkDate(date=datetime.date(2023, 6, 15))

    def test_wheel_up_years_field(self):
        """Test wheel up in years field increments year."""
        initial_date = self.widget.date()

        evt = TTkMouseEvent(0, 0, TTkK.Wheel, TTkK.WHEEL_Up, TTkK.NoModifier, 1, '')
        result = self.widget.wheelEvent(evt)

        assert result is True
        new_date = self.widget.date()
        days_in_year = 366 if calendar.isleap(initial_date.year) else 365
        expected_ordinal = initial_date.toordinal() + days_in_year
        assert new_date.toordinal() == expected_ordinal

    def test_wheel_down_months_field(self):
        """Test wheel down in months field decrements month."""
        initial_date = self.widget.date()

        evt = TTkMouseEvent(5, 0, TTkK.Wheel, TTkK.WHEEL_Down, TTkK.NoModifier, 1, '')
        result = self.widget.wheelEvent(evt)

        assert result is True
        new_date = self.widget.date()
        expected_ordinal = initial_date.toordinal() - 30
        assert new_date.toordinal() == expected_ordinal

    def test_wheel_resets_digit(self):
        """Test wheel events reset digit counter."""
        self.widget._state.digit = 3

        evt = TTkMouseEvent(0, 0, TTkK.Wheel, TTkK.WHEEL_Up, TTkK.NoModifier, 1, '')
        self.widget.wheelEvent(evt)

        assert self.widget._state.digit == 0

    def test_wheel_outside_fields_no_effect(self):
        """Test wheel events outside fields have no effect."""
        initial_date = self.widget.date()

        # Wheel on separator position
        evt = TTkMouseEvent(4, 0, TTkK.Wheel, TTkK.WHEEL_Up, TTkK.NoModifier, 1, '')
        result = self.widget.wheelEvent(evt)

        assert result is True
        assert self.widget.date() == initial_date


class TestTTkDateShowForm:
    """Test calendar form functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.widget = TTkDate(date=datetime.date(2023, 6, 15))

    @patch('TermTk.TTkCore.helper.TTkHelper.overlay')
    @patch('TermTk.TTkWidgets.datetime_date.TTkResizableFrame')
    @patch('TermTk.TTkWidgets.datetime_date.TTkDateForm')
    def test_show_form_date_selection_callback(self, mock_date_form, mock_frame, mock_overlay):
        """Test _showForm() date selection callback functionality."""
        # Setup mocks
        mock_frame_instance = MagicMock()
        mock_form_instance = MagicMock()
        mock_frame.return_value = mock_frame_instance
        mock_date_form.return_value = mock_form_instance

        # Mock the signal connection
        mock_date_changed_signal = MagicMock()
        mock_form_instance.dateChanged = mock_date_changed_signal

        self.widget._showForm()

        # Verify signal connection was attempted
        mock_date_changed_signal.connect.assert_called_once()

        # Get the connected slot function
        connected_slot = mock_date_changed_signal.connect.call_args[0][0]

        # Test the slot behavior
        test_date = datetime.date(2024, 1, 1)
        with patch.object(self.widget, 'setDate') as mock_set_date, \
             patch.object(self.widget, 'setFocus') as mock_set_focus:

            connected_slot(test_date)

            # Verify the slot clears the signal, closes frame, sets date, and focuses widget
            mock_date_changed_signal.clear.assert_called_once()
            mock_frame_instance.close.assert_called_once()
            mock_set_date.assert_called_once_with(test_date)
            mock_set_focus.assert_called_once()


class TestTTkDateIntegration:
    """Integration tests for TTkDate widget."""

    def setup_method(self):
        """Set up test fixtures."""
        self.widget = TTkDate(date=datetime.date(2023, 6, 15))

    def test_complete_date_entry_workflow(self):
        """Test complete date entry workflow."""
        # Start with field selection
        self.widget._state.selected = _FieldSelected.YEARS

        # Enter year 2024
        for digit in "2024":
            evt = TTkKeyEvent(TTkK.Character, digit, "", TTkK.NoModifier)
            self.widget.keyEvent(evt)

        # Navigate to months
        evt = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Tab, "", TTkK.NoModifier)
        self.widget.keyEvent(evt)

        # Enter month 12
        for digit in "12":
            evt = TTkKeyEvent(TTkK.Character, digit, "", TTkK.NoModifier)
            self.widget.keyEvent(evt)

        # Navigate to days
        evt = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Tab, "", TTkK.NoModifier)
        self.widget.keyEvent(evt)

        # Enter day 25
        for digit in "25":
            evt = TTkKeyEvent(TTkK.Character, digit, "", TTkK.NoModifier)
            self.widget.keyEvent(evt)

        # Verify final date
        assert self.widget.date() == datetime.date(2024, 12, 25)

    def test_boundary_conditions_leap_year(self):
        """Test boundary conditions with leap year."""
        # Set to leap year
        leap_date = datetime.date(2024, 2, 29)
        self.widget.setDate(leap_date)

        # Verify leap year date is accepted
        assert self.widget.date() == leap_date

        # Test incrementing/decrementing around leap day
        self.widget._state.selected = _FieldSelected.DAYS

        # Decrement day
        evt = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Down, "", TTkK.NoModifier)
        self.widget.keyEvent(evt)
        assert self.widget.date() == datetime.date(2024, 2, 28)

        # Increment back
        evt = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Up, "", TTkK.NoModifier)
        self.widget.keyEvent(evt)
        assert self.widget.date() == datetime.date(2024, 2, 29)

    @patch.object(TTkDate, 'update')
    def test_state_changes_trigger_updates(self, mock_update):
        """Test that state changes trigger UI updates."""
        # Navigation should trigger update
        evt = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Tab, "", TTkK.NoModifier)
        self.widget.keyEvent(evt)
        mock_update.assert_called()

        mock_update.reset_mock()

        # Date changes should trigger update
        evt = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Up, "", TTkK.NoModifier)
        self.widget.keyEvent(evt)
        mock_update.assert_called()

    def test_signal_emission_on_date_changes(self):
        """Test signal emission on various date changes."""
        signals_received = []

        def slot(date_value):
            signals_received.append(date_value)

        self.widget.dateChanged.connect(slot)

        # Test programmatic date change
        new_date = datetime.date(2025, 1, 1)
        self.widget.setDate(new_date)
        assert len(signals_received) == 1
        assert signals_received[0] == new_date

        # Test keyboard-induced date change
        self.widget._state.selected = _FieldSelected.DAYS
        evt = TTkKeyEvent(TTkK.SpecialKey, TTkK.Key_Up, "", TTkK.NoModifier)
        self.widget.keyEvent(evt)
        assert len(signals_received) == 2
        assert signals_received[1] == datetime.date(2025, 1, 2)