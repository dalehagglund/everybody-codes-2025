import sys
import re
from functools import partial, reduce
from dataclasses import dataclass
from collections import defaultdict, deque
from bisect import bisect_left, bisect_right
import pytest
from itertools import pairwise, count
from typing import NamedTuple

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

def part2(input):
    return None

def prod(items):
    return reduce(lambda x, y: x * y, items, 1)
    
def part3(input):
    pass

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