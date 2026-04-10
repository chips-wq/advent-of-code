import sys

"""
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

A: x1, y1
B: x2, y2
P: X=x, Y=y

for the x coordinate

how many times you press a: a
how many times you press b: b

a*x1 + b*x2 = x
a*y1 + b*y2 = y

b = (y-a*y1)/y2

a * (y2 * x1 - x2 * y1) = x*y2-y*x2

1. if x1*y2 == x2*y1
    1. if (x*y2 == y*x2), then any single `a` satisfies the equation
        just pick minimum `a` s.t (y-a*y1) % y2 == 0

    2. else nobody satisfies the equation

2. otherwise, they're both fixed and
a = (x*y2-y*x2) / (x1*y2 - x2*y1)
(if they're not integers, we're done I guess)

[x1 x2] * [a] = [x]
[y1 y2]   [b]   [y]

just find inverse of this: Q: can this be solved

(2x2) * (2x1)
Solve for a and b:
    1. just a system of equations

Overall cost: 3a + b
"""
infile = "example.in" if len(sys.argv) <= 1 else sys.argv[1]

def parse_test(test: str):
    test = test.strip().splitlines()
    x1 = int(test[0].split("X+")[1].split(", ")[0])
    y1 = int(test[0].split("Y+")[1].split(", ")[0])

    x2 = int(test[1].split("X+")[1].split(", ")[0])
    y2 = int(test[1].split("Y+")[1].split(", ")[0])

    x = int(test[2].split("X=")[1].split(", ")[0])
    y = int(test[2].split("Y=")[1].strip())
    
    return x1, y1, x2, y2, x, y

with open(infile, "r") as f:
    tests = f.read().split('\n\n')
    cost = 0
    for test in tests:
        x1, y1, x2, y2, x, y = parse_test(test)
        assert (x1*y2 != x2*y1)
        if (x*y2-y*x2) % (y2*x1-x2*y1) != 0: continue

        a = (x*y2-y*x2) // (y2*x1-x2*y1)
        if (y-a*y1) % y2 != 0: continue
        b = (y-a*y1)//y2
        print(f"{a=}, {b=}")
        cost += 3 * a + b
    print(f"{cost=}")

