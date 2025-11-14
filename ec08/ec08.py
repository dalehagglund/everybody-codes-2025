import sys
import re
from functools import partial, reduce
from dataclasses import dataclass
from collections import defaultdict, deque, Counter
from bisect import bisect_left, bisect_right
import pytest
from itertools import pairwise, count
from typing import NamedTuple
import functools
from itertools import combinations

def star(f): lambda t: f(*t)

def read_input(fname):
    with open(fname) as f:
        pins = list(map(int, f.readlines()[0].strip().split(",")))
    return pins
    

def part1(input):
    nails = input
    npins = 32
    total = 0 
    for i, j in pairwise(nails):
        print(f"... {i, j = }")
        if ((i - 1) + (npins/2)) % npins == (j - 1):
            total += 1
    return total
    
class modrange:
    def __init__(self, start, stop, modulus):
        self.start = start
        self.stop = stop
        self.modulus = modulus
        
        if stop < start:
            self._left = range(self.start, self.modulus)
            self._right = range(0, self.stop + 1)
        else:
            self._left = range(self.start, self.stop + 1)
            self._right = range(0, 0)

    def __contains__(self, n):
        return n in self._left or n in self._right

@functools.cache
def pins_between(p1, p2, npins):
    first, last = (p1 + 1) % npins, (p2 - 1) % npins
    return modrange(first, last, npins)
          
def intersects_orig(npins, ch1, ch2) -> bool:
    s1, e1 = ch1
    s2, e2 = ch2
    
    if (s1 + 1) % npins == e1: return False
    if (s2 + 1) % npins == e2: return False
    
    if len({s1, e1, s2, e2}) < 4: return False
        
    s2e2 = pins_between(s2, e2, npins)
    e2s2 = pins_between(e2, s2, npins)
    
    if s1 in s2e2 and e1 in s2e2:
        return False
    elif s1 in e2s2 and e1 in e2s2:
        return False
    else:
        return True
        
@pytest.mark.parametrize(
    "npins, chord1, chord2, expected", [
        (8, (0, 1), (1, 7), False),
        (8, (0, 4), (4, 1), False),
        (8, (0, 4), (1, 5), True),
        
    ]
)
def test_intersects(npins, chord1, chord2, expected):
    assert intersects_orig(npins, chord1, chord2) == expected
    assert intersects_orig(npins, chord2, chord1) == expected

def part2(input):
    pins = [p - 1 for p in input]   # makes % easier to use
    npins = 256     # 8 for sample input
    prev_chords = []
    
    print(f"... {len(pins) = }")

    total = 0
    for i, chord in enumerate(pairwise(pins)):
        # print(f"... {i}: {chord = }")
        for prev in prev_chords:
            # print(f"... ... {prev = }")
            if intersects_orig(npins, chord, prev):
                # print(f"... ... intersects!")
                total += 1
        prev_chords.append(chord)
    return total

def prod(items):
    return reduce(lambda x, y: x * y, items, 1)

def intersects(npins, ch1, ch2):
    import operator
    
    # coincident chords and two chords with a common endpoint
    # do not intersect.
    if ch1 == ch2: return False
    if len({*ch1, *ch2}) == 3: return False
    
    a, b = ch1
    c, d = ch2
        
    # normalize so a == 0. this is equivalent to rotating the pins
    # `a` steps ccw around the circle, so it doesn't change intersections.

    a, b, c, d = map(lambda n: (n - a) % npins, (a, b, c, d))
    # assert a == 0

    # cwpins = range(a+1, b) # pins between a and b, clockwise from a
    
    # 1. c and d in cwpins => both on one side of (a, b)
    # 2. one of c and d in cwpins => (c, d) crosses (a, b)
    # 3. neither of c, d in cwpins -> both on the *other side* of (a, b)
    
    # assert (1 <= c < b) + (1 <= d < b) == (c in cwpins) + (d in cwpins)
    # return (1 <= c < b) + (1 <= d < b) == 1   

    return (1 <= c < b) + (1 <= d < b) == 1

def part3(input):
    pins = [p - 1 for p in input]
    npins = 8 if len(pins) < 20 else 256 # auto-adjust for sample inputs

    # normalize each chord described the by the pin sequence
    chords = [tuple(sorted(pair)) for pair in pairwise(pins)]
    count = defaultdict(lambda: 0)
    for ch in chords: count[ch] += 1
    
    max_cut = 0
    for i, stroke in enumerate(combinations(range(npins), 2)):
        if i % 1000 == 0: print(f"... {i}: {stroke = } {max_cut = }")
        cuts = (
            sum(map(partial(intersects, npins, stroke), chords))
            + count[stroke]
        )
        max_cut = max(max_cut, cuts)
    return max_cut

dispatch = {
    1: part1,
    2: part2,
    3: part3,
}

def error(message):
    print(f"{sys.argv[0]}: {message}", file=sys.stderr)
    exit(1)
    
import time
    
class perftimer():
    def __init__(self):
        self._start = None
        self._stop = None
    def __enter__(self):
        self._start = time.perf_counter()
        return self
    def __exit__(self, exctype, excval, exctb):
        self._stop = time.perf_counter()
        return False
    def elapsed(self):
        if self._start is None:
            return 0
        elif self._start is None:
            return timer.perf_counter() - self._start
        else:
            return self._stop - self._start

def main(argv: list[str]):
    parts = []

    while len(argv) > 0 and argv[0].startswith("-"):
        arg = argv.pop(0)
        if arg == "--": 
            break
        if re.search("^-[^-].+$", arg):
            argv[0:0] = [
                f"-{letter}"
                for letter in arg[1:]
            ]
            continue

        if re.search(r"^-[123]$", arg):
            parts.append(int(arg[1]))
        else:
            error(f"unrecognized argument {arg}")

    if len(argv) != 1:
        error(f"expecting exactly one filename")
    
    if len(parts) == 0:
        parts = sorted(dispatch.keys())
    parts.sort()
    
    input = read_input(argv[0])
    for part in parts:
        with perftimer() as t:
            result = dispatch[part](input)
        print(f"part {part} answer = {result} elapsed = {t.elapsed():g}")

if __name__ == "__main__":
    main(sys.argv[1:])