import sys
import re
from functools import partial, reduce
from dataclasses import dataclass
from collections import defaultdict
from bisect import bisect_left, bisect_right
import pytest
from itertools import pairwise

def star(f): lambda t: f(*t)

def read_input(fname):
    follows = dict()
    with open(fname) as f:
        names, _, *rest = f.readlines()
        s = map(str.strip, rest)
        s = map(lambda item: item.split(" > "), s)
        for char, after in s:
            follows[char] = set(after.split(","))
    return names.split(","), follows

def part1(input):
    names, follows = input
    
    for name in names:
        if all(
            ch2 in follows[ch1]
            for ch1, ch2
            in pairwise(name)
        ):
            return name
    else:
        return "Error: no matching name found"

def part2(input):
    pass

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

def main(argv: list[str]):
    import time
    
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

        if re.search("^-[123]$", arg):
            parts.append(int(arg[1]))
        else: 
            error(f"unrecognized argument {arg}")

    if len(argv) != 1:
        error(f"expecting exactly one filename")
    
    if len(parts) == 0:
        parts = sorted(dispatch.keys())
    parts.sort()
    
    def now():
        return time.perf_counter()
    
    input = read_input(argv[0])
    for part in parts:
        start = now()
        result = dispatch[part](input)
        elapsed = now() - start
        print(f"part {part} answer = {result} {elapsed = :g}")

if __name__ == "__main__":
    main(sys.argv[1:])