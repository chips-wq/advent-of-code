from functools import cache
from collections import deque 
from string import digits
import sys

infile = "example1.in" if len(sys.argv) <= 1 else sys.argv[1]

with open(infile, "r") as f:
    matrix = [list(line) for line in f.read().splitlines()]

    @cache
    def dp(i: int, j: int):
        n, m = len(matrix), len(matrix[0])

        dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        cdigit = int(matrix[i][j])
        if cdigit == 9: return 1
        
        ans = 0
        for di, dj in dirs:
            r, c = i + di, j + dj
            if r < 0 or r >= n or c < 0 or c >= m: continue
            if matrix[r][c] not in digits: continue
            ndigit = int(matrix[r][c])
            if cdigit + 1 != ndigit: continue
            assert (cdigit + 1 == ndigit)
            ans += dp(r, c)
        return ans
        
    ans = 0
    for i, line in enumerate(matrix):
        for j, el in enumerate(line):
            if el == '0':
                distinct_paths = dp(i, j)
                ans += distinct_paths
                print(f"{i=}, {j=}, {matrix[i][j]=}, {distinct_paths=}")
                dp.cache_clear()
    print(f"{ans=}")
