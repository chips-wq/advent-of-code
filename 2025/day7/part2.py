"""
just use a step function


x = stored in cache
.......x.......
...............
......x^x......
...............
.....x^x^x.....
...............
....x^x^x^x....
[...not filled with caches from here (it actually is, not drawing it anymore)]
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............
"""

import sys
from functools import cache


def print_grid(grid):
    for line in grid:
        print("".join(line))
    print()

infile = sys.argv[1]
with open(infile, "r") as f:
    grid = f.read().splitlines()
    for i, line in enumerate(grid):
        grid[i] = list(line)

    si, sj = -1, -1
    for i, line in enumerate(grid):
        for j, el in enumerate(line):
            if el == 'S':
                si, sj = i, j

    n, m = len(grid), len(grid[0])

    @cache
    def dp(i: int, j: int):
        assert 0 <= i < n
        if j < 0 or j >= m: return 0

        while i < n and grid[i][j] != '^':
            i += 1

        if i == n:
            return 1

        return dp(i, j-1) + dp(i, j+1)            

    assert (si, sj) != (-1, -1)
    ans = dp(si, sj)
    print(f"{ans=}")
