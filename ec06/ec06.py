import sys
import re
from functools import partial, reduce
from dataclasses import dataclass
from collections import defaultdict
from bisect import bisect_left, bisect_right
import pytest

def read_input(fname):
    with open(fname) as f:
        input = f.readlines()[0].strip()
    return input

def part1(input):
    mentors = 0
    pairs = 0
    for ch in input:
        if ch not in "aA": continue
        if ch == "A":
            mentors += 1
        else:
            pairs += mentors
    return pairs

def part2(input):
    mentors = defaultdict(lambda: 0)
    pairs = defaultdict(lambda: 0)
    for ch in input:
        if ch in "ABC": mentors[ch] += 1
        else: pairs[ch] += mentors[ch.upper()]
    return sum(pairs.values())

def prod(items):
    return reduce(lambda x, y: x * y, items, 1)
    
def find_interval(items, lower, upper):
    left, right = bisect_left(items, lower), bisect_right(items, upper)
    if left == len(items): return (0, 0) # empty range
    assert right is not None
    return left, right
    

@pytest.mark.parametrize(
    "items, lower, upper, expected", [
        ([], 3, 5, (0, 0)),
        ([1, 1, 3, 11], 0, 100, (0, 4)),
        ([1, 1, 1, 2, 2], 1, 1, (0, 3)),
        ([1, 1, 1, 2, 2], 2, 2, (3, 5)),
        ([1, 2, 3, 4, 5, 6, 7, 8], 2, 5, (1, 5)),
        ([1, 2, 3, 4, 5, 6, 7, 8], 10, 10, (0, 0)),
        ([1, 2, 3, 4, 5, 6, 7, 8], -2, -1, (0, 0)),
        ([1, 2, 3, 4, 5, 6, 7, 8], -2, 3, (0, 3)),
        ([1, 2, 3, 4, 5, 6, 7, 8], -2, 10, (0, 8)),
            
    ]
)    
def test_find_interval(items, lower, upper, expected):
    assert find_interval(items, lower, upper) == expected

def part3(input):
    mentors = defaultdict(list)
    novices = defaultdict(list)

    mindist = 1000
    reps = 1000

    for pos, ch in enumerate(input * reps):
        if ch in "ABC": mentors[ch].append(pos)
        else: novices[ch].append(pos)

    # position lists are sorted by construction

    total = 0
    for category in "abc":
        #print(f"cat {category}:")
        for npos in novices[category]:
            left, right = find_interval(
                mentors[category.upper()],
                npos - mindist,
                npos + mindist
            )
            #print(f"... nov {npos} {left, right = }")
            total += right - left
    
    return total
    
# this turns out to be slower then the above by a factor
# of about 3 on my part 3 input. it gets the right answer
# though.

def part3_alternate(input):
    mindist = 1000
    input = input * 1000
    
    total = 0
    for pos, ch in enumerate(input):
        if ch in "ABC": continue
        left, right = max(pos - mindist, 0), min(pos + mindist, len(input))
        total += input.count(ch.upper(), left, right + 1)
        
    return total
    
    
dispatch = {
    1: part1,
    2: part2,
    3: part3,
    #3: part3_alternate,
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