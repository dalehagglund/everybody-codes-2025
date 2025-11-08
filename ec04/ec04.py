import sys
import re
from functools import partial, reduce

def read_input(fname):
    with open(fname) as f:
        s = f.readlines()
        s = map(str.strip, s)
        s = map(lambda item: item.split("|"), s)
        s = map(partial(map, int), s)
        s = map(list, s)
        input = list(s)
    return input

def part1(input):
    pass
    
def part2(input):
    pass
    
def prod(items):
    return reduce(lambda x, y: x * y, items, 1)
    
def part3(input):
    from copy import deepcopy
    input = deepcopy(input)
    
    assert len(input) > 1

    input[0].insert(0, 1)
    input[-1].append(1)

    num = prod(right for _, right in input)
    den = prod(left  for left, _  in input)
    
    return int((100 * num) / den)

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