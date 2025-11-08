import sys
import re
from functools import partial, reduce
from dataclasses import dataclass

@dataclass
class Segment:
    center: int
    
    left: int = None
    right: int = None
    
    def score(self) -> int:
      left = str(self.left) if self.left is not None else "";
      right = str(self.right) if self.right is not None else ""
      return int("".join((left, center, right)))

    def __str__(self):
        left = str(self.left) if self.left is not None else "_";
        right = str(self.right) if self.right is not None else "_"
        return f"{left} / {self.center} / {right}"

def read_input(fname):
    with open(fname) as f:
        input = []
        for line in f.readlines():
            left, right = line.strip().split(":")
            input.append((
                int(left),
                list(map(int, right.split(",")))
            ))
    return input
    
def fishbone(nums: int) -> list[Segment]:
    segs = [Segment(nums[0])]
    for n in nums[1:]:
        for s in segs:
            if   n < s.center and s.left  is None: 
                s.left  = n
                break
            elif n > s.center and s.right is None: 
                s.right = n
                break
        else:
            segs.append(Segment(n))
    return segs
    
def quality(fishbone: list[Segment]) -> int:
    return int("".join(str(seg.center) for seg in fishbone))
    

def part1(input):
    if len(input) != 1:
        return "Error: expecting a single line"
    _, input = input[0]
    return quality(fishbone(input))
    
def part2(input):
    qualities = [
        quality(fishbone(nums))
        for _, nums
        in input
    ]
    
    return max(qualities) - min(qualities)
    
def prod(items):
    return reduce(lambda x, y: x * y, items, 1)
    
def part3(input):
    swords = [
        (n, fishbone(nums), quality(fishbone(nums)))
        for n, nums
        in input
    ]
    
    def key(s):
        n, fishbone, quality = s
        return (
            quality,
            tuple(seg.score() for seg in fishbone),
            n,
        )

    swords.sort(key=key, reverse=True)
    return sum(
        (i + 1) * sword[0] for i, sword in enumerate(swords)
    )
     
dispatch = {
    1: part1,
    2: part2,
    3: part3,
}

def error(message):
    print(f"{sys.argv[0]}: {message}", file=sys.stderr)
    exit(1)

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

        if re.search("^-[123]$", arg):
            parts.append(int(arg[1]))
        else: 
            error(f"unrecognized argument {arg}")

    if len(argv) != 1:
        error(f"expecting exactly one filename")
    
    if len(parts) == 0:
        parts = [1, 2, 3]
    parts.sort()
    
    input = read_input(argv[0])
    for part in parts:
        print(f"part {part} answer = {dispatch[part](input)}")

if __name__ == "__main__":
    main(sys.argv[1:])