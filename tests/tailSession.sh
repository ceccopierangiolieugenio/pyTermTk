#!/usr/bin/env bash

esc=$(printf '\033')

_RST_=${esc}'[0m'  # resets color and format

# Regular Colors
Black=${esc}'[38;5;0m'
Red=${esc}'[38;5;1m'
Green=${esc}'[38;5;2m'
Yellow=${esc}'[38;5;3m'
Blue=${esc}'[38;5;4m'
Magenta=${esc}'[38;5;5m'
Cyan=${esc}'[38;5;6m'
White=${esc}'[38;5;7m'

# Background
On_Black=${esc}'[48;5;0m'
On_Red=${esc}'[48;5;1m'
On_Green=${esc}'[48;5;2m'
On_Yellow=${esc}'[48;5;3m'
On_Blue=${esc}'[48;5;4m'
On_Magenta=${esc}'[48;5;5m'
On_Cyan=${esc}'[48;5;6m'
On_White=${esc}'[48;5;7m'

while read -r line; do
    echo "$line" |
    sed "s,/home.*/TermTk/,TermTk/," |
    sed "s,^\(INFO:\),${Green}\1${_RST_}," |
    sed "s,^\(ERROR:\),${Red}\1${_RST_}," |
    sed "s,^\(DEBUG:\),${Blue}\1${_RST_},"
done < <(tail -F session.log)