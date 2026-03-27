import sys
from collections import deque

infile = "example1.in" if len(sys.argv) <= 1 else sys.argv[1]

"""

NW N NE
W  . E
SW S SE

W N E S

external corner: (i, i+1, combined) are different from R (or just outside)
internal corner: (i, i+1) are == R, combined is different from R

Every single time it's an external / internal counter that's the "start" of a new side.

this here is an external corner (two external corners)
|  |
|  |
>-d
|R|
|R|
|R|>--d
|RRRRR|
^-----<

Notice how each corner sort of counts a single side
"""

def is_corner(el: str, neighs: list[str]):
    if (el != neighs[0] and el != neighs[1]):
        return True
    if el == neighs[0] and el == neighs[1] and el != neighs[2]:
        return True
    return False

def bfs(si: int, sj: int, matrix: list[list[str]], s: set[tuple[int, int]]):
    typ = matrix[si][sj]
    q = deque([(si, sj)])
    s.add((si, sj))

    # dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    dirs = [(0, -1), (-1, 0), (0, 1), (1, 0)]

    n, m = len(matrix), len(matrix[0])

    area = 0
    perimeter = 0
    sides = 0
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
        # Check if it's a corner for all possible 4 ways of it being a corner
        for k in range(len(dirs)):
            d1, d2 = dirs[k]
            f1, f2 = dirs[(k+1)%len(dirs)]
            c1, c2 = d1+f1, d2+f2
            A = [(i + d1, j + d2), (i + f1, j + f2), (i + c1, j + c2)]
            neighs = ['!' if (r < 0 or r >= n or c < 0 or c >= m) else matrix[r][c] for (r, c) in A]
            if is_corner(typ, neighs):
                sides += 1
        
        for di, dj in dirs:
            r, c = i + di, j + dj
            if (r < 0 or r >= n or c < 0 or c >= m): continue
            if typ != matrix[r][c]: continue
            if (r, c) in s: continue
            s.add((r, c))
            q.append((r, c))
    return area, perimeter, sides


with open(infile, "r") as f:
    matrix = [list(line) for line in f.read().splitlines()]

    s = set()
    ans = 0
    for i, line in enumerate(matrix):
        for j, el in enumerate(line):
            # Compute the area, perimiter for this particular region 
            if (i, j) not in s:
                area, perimeter, sides = bfs(i, j, matrix, s)
                ans += area * sides
                print(f"{matrix[i][j]=}, {i=}, {j=}, {area=}, {perimeter=}, {sides=}")
    print(f"{ans=}")
    
