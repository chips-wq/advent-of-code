import sys
from functools import cache

infile = "example1.in" if len(sys.argv) <= 1 else sys.argv[1]


@cache
def dp(x: int, steps: int):
    assert steps >= 0
    assert x >= 0
    if steps == 0: return 1
    if x == 0: return dp(1, steps-1)
    if len(str(x)) % 2 == 0:
        return dp(int(str(x)[:len(str(x))//2]), steps-1) + dp(int(str(x)[len(str(x))//2:]), steps-1)
    return dp(x*2024, steps-1)



def blink_t(x: int):
    if x == 0: return [1]
    if len(str(x)) % 2 == 0: return [int(str(x)[:len(str(x))//2]), int(str(x)[len(str(x))//2:])]
    return [x*2024]

ITERS = 75
with open(infile, "r") as f:
    A = list(map(int, (el for el in f.read().strip().split())))

    ans = 0
    for x in A:
        ans += dp(x, ITERS)
    print(f"{ans=}")
