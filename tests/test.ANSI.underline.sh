#!/usr/bin/env bash

set -euo pipefail

# ANSI SGR helpers
UL=$'\e[4m'       # underline on
NO_UL=$'\e[24m'   # underline off
RESET=$'\e[0m'    # reset all attributes
BOLD=$'\e[1m'
RED=$'\e[31m'
GREEN=$'\e[32m'
YELLOW=$'\e[33m'
CYAN=$'\e[36m'
EL0=$'\e[K'       # erase from cursor to end of line

move_to_col() {
	printf '\r\e[%dG' "$1"
}

hr() {
	printf '%s\n' '------------------------------------------------------------'
}

section() {
	printf '%b\n' "${BOLD}${CYAN}$1${RESET}"
}

pass_hint() {
	printf '%b\n' "${GREEN}Expected:${RESET} $1"
}

fail_hint() {
	printf '%b\n' "${YELLOW}Watch for:${RESET} $1"
}

printf '%b\n' "${BOLD}Terminal Underline Feature Test${RESET}"
printf 'Shell: %s\n' "${SHELL:-unknown}"
printf 'TERM : %s\n' "${TERM:-unknown}"
hr

section '1) Basic underline on/off'
printf 'Normal -> %bunderlined%b -> normal\n' "${UL}" "${NO_UL}"
pass_hint 'Only the word "underlined" is underlined.'
fail_hint 'Underline leaking into text after NO_UL.'
hr

section '2) Reset behavior (SGR 0)'
printf '%bUNDERLINED then RESET%b then plain text\n' "${UL}" "${RESET}"
pass_hint 'Text after RESET is not underlined.'
fail_hint 'Attributes persisting after RESET.'
hr

section '3) Mixed attributes'
printf '%b%bBold+Underline%b still bold only%b plain\n' "${BOLD}" "${UL}" "${NO_UL}" "${RESET}"
pass_hint 'Underline ends at NO_UL while bold remains until RESET.'
fail_hint 'NO_UL disabling unrelated attributes (like bold).'
hr

section '4) Color + underline'
printf '%b%bRed underlined text%b and red not-underlined%b plain\n' "${RED}" "${UL}" "${NO_UL}" "${RESET}"
pass_hint 'Color continues after NO_UL; underline does not.'
fail_hint 'Underline reset clearing color unexpectedly.'
hr

section '5) Wrap test (bleed detection)'
printf 'This line is designed to be long enough to wrap in a narrow terminal window. '
printf '%bUNDERLINE_START%b ' "${UL}" "${NO_UL}"
printf 'If your emulator has a bug, underline may continue on the next visual line.\n'
pass_hint 'Only UNDERLINE_START is underlined, even when wrapped.'
fail_hint 'Underline bleeding into next wrapped segment or next line.'
hr

section '5b) Target repro: underline + erase-to-EOL'
printf 'Case A (intentional-bad order): '
printf '%bUNDERLINED TITLE' "${UL}"
printf '%b' "${EL0}"
printf '%b\n' "${NO_UL}"
pass_hint 'If your terminal applies attributes to erased cells, the rest of this line will be underlined.'
fail_hint 'No underline to EOL here means your emulator likely does not reproduce the bug.'

printf 'Case B (safe order): '
printf '%bUNDERLINED TITLE%b' "${UL}" "${NO_UL}"
printf '%b\n' "${EL0}"
pass_hint 'Underline should stop at TITLE, with no underline to line end.'
fail_hint 'Underline to EOL here indicates a stronger attribute-state bug.'
hr

section '5c) Target repro: status-line style redraw'
printf 'A tool that redraws a line with CR + clear can accidentally keep underline active.\n'
printf 'Watch the first row while it updates...\n'
for i in {1..8}; do
	printf '\r'
	printf 'Status: '
	if (( i % 2 == 0 )); then
		printf '%bRUNNING%b ' "${UL}" "${NO_UL}"
		printf '%bRUNNING%b' "${UL}" "${NO_UL}"
	else
		printf 'RUNNING ' "${UL}" "${NO_UL}"
		printf '%bRUNNING' "${UL}"
		printf '%b' "${EL0}"
		printf '%b' "${NO_UL}"
	fi
	printf ' tick=%d    ' "$i"
	sleep 0.50
done
printf '\n'
pass_hint 'Even ticks usually look fine; odd ticks may show underline to EOL on affected emulators.'
fail_hint 'Unexpected trailing underline after redraw operations.'
hr

section '6) Newline boundary'
printf '%bLine A underlined%b\n' "${UL}" "${NO_UL}"
printf 'Line B should be plain\n'
pass_hint 'Line B is not underlined.'
fail_hint 'Underline carrying over across newline.'
hr

section '7) Stress pattern'
for i in {1..10}; do
	printf 'Row %02d: normal | %bUL%b | normal | %bUL%b | normal\n' "$i" "${UL}" "${NO_UL}" "${UL}" "${NO_UL}"
done
pass_hint 'Underline appears only inside UL markers on every row.'
fail_hint 'Random attribute drift after repeated toggles.'
hr

printf '%b\n' "${BOLD}Done.${RESET}"
printf 'Tip: Resize terminal narrower and re-run to test wrapping edge cases.\n'
