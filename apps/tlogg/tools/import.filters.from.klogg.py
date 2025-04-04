#!/usr/bin/env python3
#  This is just a helper, don't rely on this script too much
#  Usage:
#       cat ~/.config/klogg/klogg.conf | tools/import.filters.from.klogg.py

import re
import fileinput

# I am trying o match things like:
#   sets\1\HighlighterSet\highlighters\1\fore_colour=#ff000000
#   sets\1\HighlighterSet\highlighters\1\ignore_case=false
#   sets\1\HighlighterSet\highlighters\1\match_only=false

rr = re.compile('^sets\\\(\d*)\\\HighlighterSet\\\highlighters\\\(\d*)\\\([^=]*)=(.*)$')

sets = {}

for line in fileinput.input():
    # print(line.rstrip())
    if m:=rr.match(line.rstrip()):
        set = m.group(1)
        num = m.group(2)
        name  = m.group(3)
        value = m.group(4)
        if set not in sets:
            sets[set] = {}
        if num not in sets[set]:
            sets[set][num] = {}
        sets[set][num][name] = value

for s in sets:
    print(f"\nset {s}:")
    for n in sets[s]:
        f = sets[s][n]
        # print (f)
        print (f"- pattern: '{f['regexp']}'")
        print (f"  ignorecase: {f['ignore_case']}")
        print (f"  fg: '#{f['fore_colour'][3:]}'")
        print (f"  bg: '#{f['back_colour'][3:]}'")
