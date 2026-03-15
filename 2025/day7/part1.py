"""
just use a step function
"""
import sys

def step(grid: list[list[str]], i: int):
    n, m = len(grid), len(grid[0])
    assert i != n-1
    splits = 0
    for j in range(m):
        if grid[i][j] != '|': continue

        if grid[i+1][j] == '.':
            grid[i+1][j] = '|'
        elif grid[i+1][j] == '^':
            splits += 1
            if j-1 >= 0: grid[i+1][j-1] = '|'
            if j+1 < m: grid[i+1][j+1] = '|'
    return splits
            
def print_grid(grid):
    for line in grid:
        print("".join(line))
    print()

infile = sys.argv[1]
with open(infile, "r") as f:
    grid = f.read().splitlines()
    for i, line in enumerate(grid):
        grid[i] = list(line)

    for i, line in enumerate(grid):
        for j, el in enumerate(line):
            if el == 'S':
                grid[i][j] = '|'

    n = len(grid)
    print(f"{n=}")

    i = 0
    ans = 0
    while (i < n-1):
        print(f"{i=}")
        print_grid(grid)
        ans += step(grid, i)
        i += 1
    print_grid(grid)
    print(f"{ans=}")
