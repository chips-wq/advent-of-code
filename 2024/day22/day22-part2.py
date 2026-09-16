"""

prefix sums and changes array

prefix sums: [i, x1, x2, x3, x4, x5,x6 ] <-- len 2001
changes:     [   -3, 6,  -1, -1, 0, 2  ]

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
    C = []
    
    for x in nums:
        seq = [x % 10]
        changes = []
        for i in range(2000):
            x = next_num(x)
            seq.append(x % 10)
        for i in range(1, len(seq)):
            changes.append(seq[i] - seq[i-1])
        C.append(changes)

    print(f"Processing done")
    G = bkt(0, [0, 0, 0, 0])

    best = -1
    bseq = None
    idx = 0
    for m_seq in G:
        if idx % 1_000 == 0:
            print(f"{m_seq=}, {idx=}")
        # print(f"{m_seq=}")
        cand = 0
        for i, x in enumerate(nums):
            x = x % 10
            tmp = x
            res = 0
            found = False
            for k, ch in enumerate(C[i]):
                tmp = tmp + ch
                if k >= 3 and C[i][k] == m_seq[-1] and C[i][k-1] == m_seq[-2] and C[i][k-2] == m_seq[-3] and C[i][k-3] == m_seq[-4]:
                    res = tmp
                    # print(f"{i=}, {len(C[i])=}, {x=}, {k=}, {res=}")
                    found = True
                    break
            if not found:
                pass
                # print(f"{i=}, {len(C[i])=}, {x=}, skipping")
            cand += res
        if cand > best:
            print(f"{m_seq=}, {cand=}, {best=}")
            best = cand
            bseq = m_seq
        idx += 1

        

