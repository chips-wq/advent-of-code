import sys
from collections import deque

infile = "example1.in" if len(sys.argv) <= 1 else sys.argv[1]

def bfs(si: int, sj: int, matrix: list[list[str]], s: set[tuple[int, int]]):
    typ = matrix[si][sj]
    q = deque([(si, sj)])
    s.add((si, sj))

    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    n, m = len(matrix), len(matrix[0])

    area = 0
    perimeter = 0
    while q:
        i, j = q.popleft()

        assert matrix[i][j] == typ
        area += 1
        # Look at all 4 sides of it I guess to count the perimeter
        for di, dj in dirs:
            r, c = i + di, j + dj
            # It's outside or they are different symbols += 1
            if (r < 0 or r >= n or c < 0 or c >= m):
                perimeter += 1
                continue
            if typ != matrix[r][c]:
                perimeter += 1
        
        for di, dj in dirs:
            r, c = i + di, j + dj
            if (r < 0 or r >= n or c < 0 or c >= m): continue
            if typ != matrix[r][c]: continue
            if (r, c) in s: continue
            s.add((r, c))
            q.append((r, c))
    return area, perimeter
    
        


with open(infile, "r") as f:
    matrix = [list(line) for line in f.read().splitlines()]

    s = set()
    ans = 0
    for i, line in enumerate(matrix):
        for j, el in enumerate(line):
            # Compute the area, perimiter for this particular region 
            if (i, j) not in s:
                area, perimeter = bfs(i, j, matrix, s)
                ans += area * perimeter
                print(f"{i=}, {j=}, {area=}, {perimeter=}")
    print(f"{ans=}")
    
