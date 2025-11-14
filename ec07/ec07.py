import sys
import re
from functools import partial, reduce
import functools
from dataclasses import dataclass
from collections import defaultdict, deque
from bisect import bisect_left, bisect_right
import pytest
from itertools import pairwise, count, groupby
from typing import NamedTuple

def star(f): lambda t: f(*t)

def read_input(fname):
    follows = dict()
    with open(fname) as f:
        names, _, *rest = f.readlines()
        s = map(str.strip, rest)
        s = map(lambda item: item.split(" > "), s)
        for char, after in s:
            follows[char] = set(after.split(","))
    return names.strip().split(","), follows
    
def is_valid(follows, name):
    return all(
        ch2 in follows[ch1]
        for ch1, ch2
        in pairwise(name)
    )
    

def part1(input):
    names, follows = input
    
    for name in names:
        if is_valid(follows, name):
            return name
    else:
        return "Error: no matching name found"

def part2(input):
    names, follows = input

    total = 0
    for index, name in zip(count(1), names):
        if is_valid(follows, name):
            total += index
    return total

def prod(items):
    return reduce(lambda x, y: x * y, items, 1)
    
def part3(input):
    prefixes, follows = input

    minlen, maxlen = 7, 11
    targetlen = range(minlen, maxlen + 1)
    
    def extend(root):
        if len(root) > maxlen:
            return
        if len(root) in targetlen:
            yield root
        if root[-1] not in follows:
            return

        for ch in follows[root[-1]]:
            yield from extend(root + ch)
    
    names = set()
    generated = 0
    for root in prefixes:
        if not is_valid(follows, root):
            continue
        for name in extend(root):
            generated += 1
            names.add(name)
            if generated % 1000000 == 0:
                print(f"... generated {generated} unique {len(names)}")
    return len(names)

def part3_dynprog(input):
    prefixes, follows = input

    minlen, maxlen = 7, 11

    trace = print
    trace = lambda *a, **kw: None
    
    
    def find_roots(prefixes):
        roots = set()
        for candidate in prefixes:
            if any(candidate.startswith(r) for r in roots):
                continue
            roots.add(candidate)
        return roots

    @functools.cache
    def extensions(last, length, depth=2):
        recur = partial(extensions, depth=depth+1)
        prefix = ".. " * depth
        trace(f"{prefix}> ({last}, {length})")
        
        total = 0
        if length == maxlen:
            trace(f"{prefix}  reached max length")
            total = 1
        else:
            if minlen <= length < maxlen:
                total += 1
            successors = follows.get(last, {})
            trace(f"{prefix}  successors = {''.join(successors)!r}")
            for ch in successors:
                total += recur(ch, length + 1)
        
        trace(f"{prefix}< ({last}, {length}) = {total}")
        return total
    
    total = 0
    for root in find_roots(prefixes):
        if not is_valid(follows, root):
            continue
        total += extensions(root[-1], len(root))
    return total
        
dispatch = {
    1: part1,
    2: part2,
    3: part3,
    4: part3_dynprog,
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

        if re.search(r"""^-\d$""", arg):
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