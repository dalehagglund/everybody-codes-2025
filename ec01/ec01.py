import sys

with open(sys.argv[1]) as f:
    names, _, instructions = f.readlines()
    names = names.strip().split(",")
    instructions = list(map(lambda s: (s[0], int(s[1:])), instructions.split(",")))
    
def part2(names, instructions):
    pos = 0
    for dir, n in instructions:
        if dir == "L": pos = (pos - n) % len(names)
        elif dir == "R": pos = (pos + n) % len(names)
    return names[pos]

def part3(names, instructions):
    names = names[:]
    def swap(pos):
        names[0], names[pos] = names[pos], names[0]
    for dir, n in instructions:
        if dir == "L": swap(-n % len(names))
        elif dir == "R": swap(n % len(names))
    return names[0]

print("part 2 answer = ", part2(names, instructions))
print("part 3 answer = ", part3(names, instructions))
