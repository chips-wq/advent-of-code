from collections import defaultdict
"""

prefix sums and changes array

              0  1   2   3   4
prefix sums: [i, x1, x2, x3, x4, x5,x6 ] <-- len 2001
changes:     [   -3, 6,  -1, -1, 0, 2  ]
                  0  1    2   3 

x_i in {0, 1, 2, ... 9}


choose a sequence of 4 numbers s.t you maximize the sum of x's.

How many sequences of 4 numbers are there ?
20 * 20 * 20 * 20 = 16 * 10^4 = 160.000 different sequences (just brute-force it), for each of those you do 2000 steps

16 * 10 ^ 4 * 2 * 10^3 = 32 * 10^7 <-- operations in total (seems manageable with pypy)

you want to maximize
pf1[i1] + pf2[i2] + ... + pf_k[i_k] with the condition that

1. ch1[i1-1], 

(ch_p[i1-1], ch_p[i1-2], ch_p[i1-3], ch_p[i1-4]) cu p din {1, 2, ..., k}
e mereu la fel

they share 1 => what's the best
they share 2 => what's the best ? (more restrictive but it must include the previous one)

they share 1:

ch1[i1] = ch2[i2] = ch3[i3] = ... ch_k[i_k]

try with (9), try with (8), etc

1. (find all of theses sort, then extend them left)
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

# Give me all monkey sequences I guess
def bkt(i: int, sol: list[int]):
    if i == 4:
        yield list(sol)
        return
    for cand in [-9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
        sol[i] = cand
        yield from bkt(i+1, sol)

with open(file, "r") as f:
    nums = [int(num) for num in f.read().splitlines()]

    D = [defaultdict(int) for _ in range(len(nums))]

    for idx, x in enumerate(nums):
        changes = []
        ix = x
        for i in range(2000):
            prev = x
            x = next_num(x)
            changes.append(x%10-prev%10)

        cur = ix%10 + changes[0] + changes[1] + changes[2]
        for k in range(3, len(changes)):
            cur += changes[k]
            cseq = (changes[k-3], changes[k-2], changes[k-1], changes[k]) 
            if cseq in D[idx]: continue
            D[idx][cseq] = cur


    print(f"Processing done")
    G = bkt(0, [0, 0, 0, 0])
    best, mseq = -1, None
    for m_seq in G:
        cand = 0
        for idx in range(len(nums)):
            cand += D[idx][tuple(m_seq)] if (tuple(m_seq) in D[idx]) else 0
        if cand > best:
            best = cand
            bseq = m_seq
            print(f"{m_seq=}, {cand=}, {best=}")


