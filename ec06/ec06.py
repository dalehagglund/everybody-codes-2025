import sys
import re
from functools import partial, reduce
from dataclasses import dataclass

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
    return None
    
def prod(items):
    return reduce(lambda x, y: x * y, items, 1)
    
def part3(input):
    return None
    
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