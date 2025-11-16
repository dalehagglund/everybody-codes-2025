import sys
import re
from functools import partial, reduce
import functools
from dataclasses import dataclass
from collections import defaultdict, deque, Counter
from bisect import bisect_left, bisect_right
import pytest
from itertools import (
    pairwise,
    count,
    groupby,
    combinations,
    product
)
from typing import NamedTuple, Iterator

def star(f): lambda t: f(*t)

def read_input(fname):
    with open(fname) as f:
        s = f.readlines()
        s = map(str.strip, s)
        s = map(lambda line: line.split(":"), s)
        s = map(lambda t: (int(t[0]), t[1]), s)
        input = list(s)
    return input
    
def part1(input):
    dna = [d for _, d in input]
    assert all(len(d) == len(dna[0]) for d in dna)

    def possible_child(child, parent1, parent2):
        return all(
            a == b or a == c 
            for a, b, c
            in zip(dna[child], dna[parent1], dna[parent2])
        )

    if possible_child(0, 1, 2):
        ch, p1, p2 = 0, 1, 2
    elif possible_child(1, 0, 2):
        ch, p1, p2 = 1, 0, 2
    elif possible_child(2, 0, 1):
        ch, p1, p2 = (2, 0, 1)
    else:
        assert False, "NO CHILD"
    
    def similarity(d1, d2):
        return sum(a == b for a, b in zip(d1, d2))
        
    return (
        similarity(dna[ch], dna[p1]) * similarity(dna[ch], dna[p2])
    )

def part2v1(input):
    dna = [d for _, d in input]
    
    def possible_child(d1, d2, d3):
        return all(
            a == b or a == c 
            for a, b, c
            in zip(d1, d2, d3)
        )
        
    def possible_family(a, b, c):
            if possible_child(a, b, c): return a, b, c
            if possible_child(b, a, c): return b, a, c
            if possible_child(c, a, b): return c, a, b
            return None

    def similarity(d1, d2):
        return sum(a == b for a, b in zip(d1, d2))
    
    total = 0
    for loops, triple in enumerate(combinations(range(len(dna)), 3)):
        if loops % 1000 == 0: print(f"... {loops}")
        i, j, k = triple
        di, dj, dk = dna[i], dna[j], dna[k]
        result = possible_family(di, dj, dk)
        if result is None:
            continue
        ch, p1, p2 = result
        s = similarity(ch, p1) * similarity(ch, p2)
        total += s
        print(f"... possible {i, j, k = } sim = {s}")
        
    return total
        

# def part2_v2(input):
    # dna = [d for _, d in input]
    
    # def possible_child(d1, d2, d3):
        # return all(
            # a == b or a == c 
            # for a, b, c
            # in zip(d1, d2, d3)
        # )
        
    # def possible_family(a, b, c):
        # return (
            # possible_child(a, b, c)
            # or possible_child(b, a, c)
            # or possible_child(c, a, b)
        # )

    # def similarity(d1, d2):
        # return sum(a == b for a, b in zip(d1, d2))


    # groups = defaultdict(list)
    # for i, d in enumerate(dna):
        # groups[d[2:3]].append(i)
    # print(groups)
    # candidates = []
    # total_combos = 0
    # families = 0
    # for triple in combinations(groups.keys(), 3):
        # if possible_family(*triple):
            # families += 1
            # n = prod(map(lambda g: len(groups[g]), triple))
            # print(f'... {triple} {n}')
            # total_combos += n
    # print(f"{families = } {total_combos = }")

def prod(items):
    return reduce(lambda x, y: x * y, items, 1)
    
def part3(input):
    dna = [d for _, d in input]

    related = defaultdict(set)
    for loops, triple in enumerate(combinations(range(len(dna)), 3)):
        if loops % 100000 == 0: print(f"... {loops:-8}")
        i, j, k = triple
        if any(a != b and b != c and a != c for a, b, c in zip(dna[i], dna[j], dna[k])):
            continue
        print(f"...    possible {i, j, k = }")
        for id1, id2 in product(triple, repeat=2):
            related[id1].add(id2)
    
    # print("related:")
    # for id in range(len(dna)):
        # if id not in related: continue
        # print(f"... {id:3d} - > {', '.join(str(f) for f in sorted(related[id]))}")
        
    def bfs(start) -> Iterator[int]:
        q = deque()
        visited: set[int] = set()
        
        # print(f"... bfs({start})")
        push = q.append
        pop = q.popleft
        push(start)
        while len(q) > 0:
            n = pop()
            if n in visited:
                continue
            visited.add(n)
            yield n
            for i in related[n]:
                push(i)
        
    nodes = set(related.keys())
    components: set[frozenset[int]] = set()
    
    while len(nodes) > 0:
        start = nodes.pop()
        cc = frozenset(bfs(start))
        components.add(cc)
        nodes -= cc
    
    # print("components:")
    # for cc in components:
        # print(f"... {set(cc)}")

    return sum(i+1 for i in max(components, key=len))

dispatch = {
    1: part1,
    2: part2v1,
    3: part3,
}

def error(message):
    print(f"{sys.argv[0]}: {message}", file=sys.stderr)
    exit(1)
    
import time
import contextlib

@contextlib.contextmanager
def suppress_stdout():
    import os
    with (
        open(os.devnull, "w") as f,
        contextlib.redirect_stdout(f)
    ):
        yield

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
    quiet = False

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

        if re.search(r"^-\d$", arg):
            parts.append(int(arg[1]))
        elif arg in ('-q'):
            quiet = True
        else: 
            error(f"unrecognized argument <{arg}>")

    if len(argv) != 1:
        error(f"expecting exactly one filename")
    
    if len(parts) == 0:
        parts = sorted(dispatch.keys())
    parts.sort()
    
    no_io = suppress_stdout if quiet else contextlib.nullcontext
    input = read_input(argv[0])

    print(f"running parts: {' '.join(map(str, parts))}")
    for part in parts:
        with no_io():
            with perftimer() as t:
                result = dispatch[part](input)
        print(f"part {part} answer = {result} elapsed = {t.elapsed():g}")

if __name__ == "__main__":
    main(sys.argv[1:])