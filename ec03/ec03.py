import sys
from collections import Counter
from itertools import chain

with open(sys.argv[1]) as f:
    input = [
        int(n) 
        for n
        in f.readlines()[0].strip().split(",")
    ]

def part1(input):
    return sum(set(input))
    
def part2(input):
    crates = sorted(set(input))
    return sum(crates[:20])

def part3(input):
    return max(Counter(input).values())

    # the following code works, and is what I wrote 
    # initially but the observation used above, that the 
    # number of sets must be equal to the maximum number
    # of times a value is *repeated* in the input, above
    # is much simpler.

    crates = sorted(input, reverse=True)
    sets = []
    for c in crates:
        for s in sets:
            if c < s[-1]:
                s.append(c)
                break
        else:
            sets.append([c])
    return len(sets)
    
print("part 1 = ", part1(input))
print("part 2 = ", part2(input))
print("part 3 = ", part3(input))