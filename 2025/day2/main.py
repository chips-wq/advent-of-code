import sys
"""
is there some suffix that replicated gives you the entire string


ffa

  i

(n-i) % (i+1) == 0
c_substr + c_substr * (n-i)//(i+1)

c_substr * (1 + (n-i) // (i+1))

322 322 322
012

9-2
len = 9
"""

def is_invalid2(x: int):
    num = str(x)
    n = len(num)
    for i in range(n-1):
        if (n-1-i) % (i+1) != 0: continue
        # print(f"{i=} -> {num[:(i+1)] * (1 + (n-1-i) // (i+1))}")
        c_str = num[:(i+1)]
        repl = (n-1-i) // (i+1)
        # print(f"{i=}, {c_str=}, {repl=}")

        if c_str * (1 + repl) == num:
            return True
    return False

def is_invalid(x: int):
    num = str(x)
    n = len(num)
    for i in range(n-1):
        c_str = num[:(i+1)]

        if c_str * 2 == num:
            return True
    return False

def check_range(rng: tuple[int, int]):
    ans = []
    l, r = rng
    for k in range(l, r+1):
        if is_invalid2(k): ans.append(k)
    return ans

assert len(sys.argv) > 1
infile = sys.argv[1]

with open(infile, "r") as f:
    rngs = f.read().split(",")
    ans = 0
    for s_rng in rngs:
        l, r = map(int, s_rng.split("-"))
        ans += sum(check_range((l, r)))
    print(ans)
