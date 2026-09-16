"""

prefix sums and changes array

prefix sums: [i, x1, x2, x3, x4, x5,x6 ] <-- len 2001
changes:     [   -3, 6,  -1, -1, 0, 2  ]

x_i in {0, 1, 2, ... 9}


choose a sequence of 4 numbers s.t you maximize the sum of x's.

"""

import sys

MOD = 16777216

def next_num(secret: int):
    # Notice those are all powers of 2, probably that's the key to part 2 IG
    # secret * 2^6

    # What happens if you multiply by a power of 2 ?
    secret = (secret ^ (secret * 64)) % MOD
    secret = (secret ^ (secret // 32)) % MOD
    secret = (secret ^ (secret * 2048)) % MOD
    return secret

"""
a = next_num(123)
b = next_num(a)
c = next_num(b)
print(f"{123=}, {a=}, {b=}, {c=}")
"""

file = sys.argv[1] if len(sys.argv) > 1 else "input.in"

with open(file, "r") as f:
    nums = [int(num) for num in f.read().splitlines()]
    
    ans = 0
    for x in nums:
        for i in range(2000):
            x = next_num(x)
        # print(x)
        ans += x
    print(ans)

