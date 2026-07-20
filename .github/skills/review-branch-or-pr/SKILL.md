---
name: review-branch-or-pr
description: "Use when: reviewing a pull request, PR, branch, diff, or code changes for bugs, regressions, risky behavior, missing tests, or merge issues. Review the changes in a specific branch or PR against its base branch and report findings first with severity and file references."
---

# Branch Or PR Review

## Overview
This skill performs a code review of the changes introduced by a specific branch or pull request.

The review should compare the target branch or PR against its base, inspect the changed files and diff, and then report concrete findings in code-review format.

## When to Use
- The user asks for a PR review
- The user asks for a branch review
- The user asks to review code changes before merge
- The user asks for bugs, regressions, or missing tests in a diff

## Review Standard
Default to a code review mindset:
- Prioritize correctness, regressions, and behavior changes
- Look for missing validation, broken assumptions, unsafe refactors, and compatibility risks
- Check whether tests cover the changed behavior when that is reasonably expected
- Keep summaries brief and place findings first

Do not default to style-only comments unless they hide a functional or maintainability risk.

## Workflow

### Step 1: Identify the Review Target
Determine whether the user wants to review:
- the current branch
- a named branch
- a specific PR number
- a PR URL

If the user does not specify a target and a current branch can be determined from git context, use that. Otherwise, ask the user to specify the branch or PR to review.

If the base branch is not specified, infer it from repository context when possible. Otherwise use the repository default branch.

If neither the base branch nor the repository default branch can be determined, stop and ask the user: "What is the base branch to compare against?" Do not proceed with a review against an assumed base.

## Step 2: Collect the Comparison Surface
Gather the smallest useful comparison surface first:
1. Identify the base branch and review target
2. Compute the merge base when reviewing a branch
3. List changed files before reading large diffs
4. Inspect the patch for the most relevant files

If the changed file count exceeds ~50 files or the diff exceeds ~2000 lines, explicitly state the scope limitation, focus review on the highest-risk files identified in Step 3, and note in Open Questions that a full review was not performed.

Prefer repository-aware tools when available. Otherwise use git locally.

Useful commands:
```bash
git status --short
git branch --show-current
git diff --name-only <base>...<target>
git diff --stat <base>...<target>
git diff <base>...<target> -- <path>
```

For PR review, prefer metadata that reveals:
- the PR base branch
- the PR head branch
- the changed files
- the patch or combined diff

## Step 3: Review the Deciding Code Paths
Review the files that actually control behavior, not just call sites or registrations.

Prioritize:
1. Logic that computes or mutates state
2. Validation and boundary handling
3. Error handling and fallback behavior
4. Tests added or omitted for behavior changes
5. Public API or data model changes

If a changed file is mostly wiring, step once to the code that directly decides behavior.

## Step 4: Form Findings
A valid finding should include:
1. The concrete risk or bug
2. Why it happens from the diff
3. The user-visible or maintenance impact
4. A precise file reference

Good findings are specific and falsifiable. Avoid vague comments like "this might be cleaner".

Focus on issues such as:
- broken control flow
- incorrect assumptions after refactors
- missing guard clauses
- inconsistent state updates
- incomplete rename or migration work
- missing or weak tests for the changed behavior
- branch-specific merge hazards

## Step 5: Validate When Needed
When a likely defect depends on behavior that can be checked cheaply, run a narrow validation:
- the most relevant unit test
- a targeted lint or typecheck
- a focused command that falsifies the concern

Do not broaden into full-suite validation unless the review risk justifies it.

## Response Format
Present findings first, ordered by severity.

Use this structure:

```text
Findings
1. [severity] Short title
   Why it is a problem, impact, and file reference.

Open Questions
- Any assumptions that could not be verified.

Change Summary
- Very brief overview of what changed.
```

If there are no findings, say so explicitly and mention residual risks or testing gaps.

## Severity Guide
- high: likely bug, regression, data loss, crash, or broken workflow
- medium: correctness risk, edge-case breakage, incomplete handling, or test gap around important behavior
- low: minor maintainability concern with plausible future risk

## Example Prompts
- "Review this PR for regressions."
- "Do a code review of branch `feature/search-refactor`."
- "Review the changes in PR #42 against main."
- "Check whether this branch is safe to merge."

## Important Rules
- Start from the diff, not from broad repository exploration
- Review the target against its actual base branch
- Findings must come before summary
- Prefer concrete bugs and regressions over style suggestions
- Run focused validation when it can confirm or disconfirm a concern cheaply