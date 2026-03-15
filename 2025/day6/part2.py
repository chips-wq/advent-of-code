from math import prod
import sys

infile = sys.argv[1]

"""

[i, j)

i  j
123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +

k  i
123 328  51 64 
51  64  387 23 
33  98  215 314
*   +   *   +

by looking at the first four strings n lines, what is the max(i | i > k and str_k[

for a fixed i

f(s1) = the first j > i s.t s1[j] == ' '

max(s_k) = current j

then do processing of the current ops

j = i + 1



"""

def compute_sum(slices: list[str], op: str):
    op = op.strip()
    m = len(slices[0])
    assert all(len(slc) == m for slc in slices)
    n = len(slices)
    nums = []
    for j in range(m):
        num = 0
        for i in range(n):
            if slices[i][j] == ' ': continue
            num = num * 10
            num += int(slices[i][j])
        nums.append(num)

    # Sum them up or times them up
    if op == '+':
        return sum(nums)
    elif op == '*':
        return prod(nums)
    assert False

with open(infile, "r") as f:
    lines = f.read().splitlines()
    ops = lines[-1]
    lines = lines[:-1]
    n = len(lines[0])
    assert all(len(line) == n for line in lines)
    ops = ops + " " * (n-len(ops))
    assert len(ops) == n

    ans = 0
    i = 0
    while i < n:
        # Find the current j
        j = max([(line.find(' ', i) if line.find(' ', i) != -1 else n) for line in lines])
        slices = []
        for line in lines:
            slices.append(line[i:j])
            print(f"{line[i:j]}")
        print(f"{ops[i:j]}")
        c_ans = compute_sum(slices, ops[i:j])
        ans += c_ans
        print(f"{c_ans=}")
        print()
        i = j + 1
    print(f"{ans=}")
