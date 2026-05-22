---
name: test-first-fix
description: "Use when: implementing bug fixes or features with RED-GREEN-REFACTOR. Priority order: get user approval before implementation, then apply minimal changes, then run regression checks."
---

# Test-First Fix Workflow

## Overview
This skill implements the RED-GREEN-REFACTOR workflow for bug fixes and features in pyTermTk:
1. **RED**: Write and run a failing test
2. **Approval**: Get user approval on the specific code change to resolve the issue
3. **GREEN**: Implement minimal fix to make test pass
4. **Verify**: Run broader tests to ensure no regressions

## When to Use
- Fixing bugs in existing widgets or core functionality
- Implementing new features with clear test requirements
- Making changes that need verification before merging

## Workflow

### Step 1: RED Phase (Write Failing Test)
1. Determine what behavior needs to be tested
2. Create test file in `tests/pytest/` or `apps/*/tests/`
3. Write test that **fails** with current code
4. Run test and confirm failure with clear error message
5. Share the failing output with user

Example:
```python
def test_textedit_follow_mode():
    """TextEdit should follow cursor in follow mode"""
    widget = TTkTextEdit(followMode=True)
    widget.setText("Line 1\nLine 2\nLine 3")
    widget.setCursorPosition(2, 0)
    assert widget.viewportTopLine() == 2  # Should scroll to show cursor
```

### Step 2: Approval Gate
**STOP** — Do not proceed without explicit user approval.

Ask user:
- "The test fails because [reason]. I'll fix it by [approach]. Approve?"
- Wait for explicit approval before coding the fix

This prevents wasted work if the approach is wrong.

### Step 3: GREEN Phase (Minimal Fix)
1. Implement the **smallest code change** that makes the test pass
2. Prefer simple solutions over comprehensive ones
3. Run the failing test → should now pass
4. Confirm no other changes needed

### Step 4: Verify (No Regressions)
1. Run tests in the same module/category
2. Run full test suite if risky changes: `pytest tests/pytest/`
3. Check for flake8 issues: `make test`
4. Confirm all tests pass

## Important Rules
- ❌ Never write test and implementation in same step
- ❌ Never implement before user approval
- ✅ Always ask for approval after RED phase
- ✅ Always verify no regressions after GREEN phase
- ✅ Prefer minimal changes (don't refactor unless needed)

## Example Session
```
USER: Fix the TextEdit cursor position bug

AGENT (RED PHASE):
  Created test at tests/pytest/widgets/textedit/test_cursor_bug.py
  Test fails: AssertionError: expected 5, got 3
  
  Root cause: setCursorPosition() doesn't update internal position correctly
  
  Fix approach: Modify _cursorPos update in setCursorPosition()
  
  Approve?

USER: Yes, go ahead

AGENT (GREEN PHASE):
  [Implements fix]
  Test now passes ✓
  
AGENT (VERIFY PHASE):
  Running surrounding tests...
  ✓ 47 tests passed
  ✓ 0 tests failed
  
Done! Fix is ready.
```
