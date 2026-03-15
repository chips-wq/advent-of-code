from math import prod
import sys

infile = sys.argv[1]

with open(infile, "r") as f:
    lines = f.read().splitlines()
    mat = []
    for line in lines[:-1]:
        mat.append(list(map(int, line.split())))
    ops = lines[-1].split()

    n, m = len(mat), len(mat[0])
    assert m == len(ops)
    ans = 0
    for j in range(m):
        if ops[j] == '+':
            ans += sum(mat[i][j] for i in range(n))
        elif ops[j] == '*':
            ans += prod(mat[i][j] for i in range(n))
        else:
            assert False
    print(f"{ans=}")
