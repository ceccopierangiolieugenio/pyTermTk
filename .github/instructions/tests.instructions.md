---
applyTo: "tests/pytest/**/*.py,apps/*/tests/**/*.py"
description: Rules for creating or updating tests in core and app test folders with behavior-first assertions and full coverage expectations.
---
# Test Authoring Rules (Path Scoped)

These rules apply when creating or editing tests under `tests/pytest/` and `apps/*/tests/`.

## Coverage Requirements

- New or modified tests must drive the touched production code to full line and branch coverage.
- Add tests for normal, edge, and error paths.
- Do not leave uncovered branches for newly introduced logic.

## Behavior-First Assertions

- Test the expected behavior of widgets and functionality from a user/API perspective.
- Prefer public APIs, signals, and documented contracts over internal implementation details.
- Validate observable outcomes (state changes, emitted signals, rendered output, return values, raised errors).

## Anti-Pattern to Avoid

- Do not tune tests to match known bugs, undefined behavior, or accidental current implementation quirks.
- If current behavior is buggy but intentional fixes are in scope, write the test for the correct expected behavior and align code to pass it.
- If behavior is ambiguous, derive expectations from docs, demos, existing stable APIs, and widget design intent.

## Test Quality

- Keep tests deterministic and isolated; avoid timing-sensitive or flaky assertions.
- Use concise fixtures and clear test names describing the behavior under test.
- When fixing a bug, include a regression test that fails before the fix and passes after it.
