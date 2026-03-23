from collections import deque 
from string import digits
import sys

infile = "example1.in" if len(sys.argv) <= 1 else sys.argv[1]

def bfs(matrix: list[list[str]], si: int, sj: int):
    q = deque([(si, sj)])
    S = set([(si, sj)])
    
    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    n, m = len(matrix), len(matrix[0])

    while q:
        ci, cj = q.popleft()
        cdigit = int(matrix[ci][cj])
        
        for di, dj in dirs:
            r, c = ci + di, cj + dj
            if r < 0 or r >= n or c < 0 or c >= m: continue
            if matrix[r][c] not in digits: continue
            ndigit = int(matrix[r][c])
            if cdigit + 1 != ndigit: continue
            assert (cdigit + 1 == ndigit)
            if (r, c) in S: continue
            S.add((r, c))
            q.append((r, c))

    reached = 0
    for i, line in enumerate(matrix):
        for j, el in enumerate(line):
            if (i, j) in S and matrix[i][j] == '9':
                reached += 1
    print(f"{reached=}")
    return reached

with open(infile, "r") as f:
    matrix = [list(line) for line in f.read().splitlines()]
    
    ans = 0
    for i, line in enumerate(matrix):
        for j, el in enumerate(line):
            if el == '0':
                reached = bfs(matrix, i, j)
                ans += reached
                print(f"{i=}, {j=}, {matrix[i][j]=}, {reached=}")
    print(f"{ans=}")
