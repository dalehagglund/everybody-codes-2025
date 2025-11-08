import sys
from collections import deque
from itertools import islice, takewhile

def add(n, m):
    X1, Y1 = n
    X2, Y2 = m
    return [ X1 + X2, Y1 + Y2 ]
    
# [X1,Y1] * [X2,Y2] = [X1 * X2 - Y1 * Y2, X1 * Y2 + Y1 * X2]
def mul(n, m):
    X1, Y1 = n
    X2, Y2 = m
    return [X1 * X2 - Y1 * Y2, X1 * Y2 + Y1 * X2]

# [X1,Y1] / [X2,Y2] = [X1 / X2, Y1 / Y2]
def div(n, m):
    X1, Y1 = n
    X2, Y2 = m
    return [int(X1 / X2), int(Y1 / Y2)]

def iterate(P, D, steps):
    result = [0, 0]
    for _ in range(steps):
        result = mul(result, result)
        result = div(result, D)
        result = add(result, P)
        yield result
        
def grid(A, div):
    UL = A
    LR = add(A, [1000, 1000])

    for Y in range(UL[1], LR[1]+1, div):
        for X in range(UL[0], LR[0]+1, div):
            yield [X, Y]
            
def engraved(P, debug=False):
    for step, Z in enumerate(iterate(P, [100000,100000], 100)):
        if abs(Z[0]) > 1000000 or abs(Z[1]) > 1000000:
            if debug:
                print(f"False {P = } {Z = } {step = }")
            return False
    if debug:
        print(f"True {P = } {Z = }")
    return True

def part2(A, div):
    count = 0
    points = 0

    for P in grid(A, div):
        if engraved(P):
            count += 1
        points += 1

    return count

with open(sys.argv[1]) as f:
    line = f.readlines()[0].strip()
    A = eval(line.split("=")[1])
    
print(A)

print("part 1 result = ", list(iterate(A, [10, 10], 3))[-1])
print("part 2 result = ", part2(A, 10))
print("part 3 result = ", part2(A, 1))