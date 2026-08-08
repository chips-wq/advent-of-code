from collections import deque, defaultdict
import sys

file = sys.argv[1] if len(sys.argv) > 1 else "example.in"

def bfs(si: int, sj: int, ei: int, ej: int, mat: list[list[str]]):
    q = deque([(si, sj)])
    n, m = len(mat), len(mat[0])

    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    d = [[0] * m for _ in range(n)]
    d[si][sj] = 1

    while q:
        i, j = q.popleft()
        assert i >= 0 and i < n and j >= 0 and j < m

        for di, dj in dirs:
            r, c = i + di, j + dj
            if r < 0 or r >= n or c < 0 or c >= m: continue
            if mat[r][c] != '#' and d[r][c] == 0:
                d[r][c] = d[i][j] + 1
                q.append((r, c))

    return d

"""
     +
    +++
   +++++
  +++x+++  <-- this is manhattan distance I think <= 3
   +++++
    +++
     +

3 second cheat

you can teleport to any cell with manhattan distance <= 20

there are <= 400 cells for one cell that has this property
"""

def iter_manhattan(r: int, c: int, x: int):
    # yield all i, j with abs(r-i) + abs(c-j) <= x
    q = deque([(r, c)])
    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    S = set([(r, c)])
    while q:
        i, j = q.popleft()
        yield (i, j)

        for di, dj in dirs:
            i1, j1 = i + di, j + dj
            if abs(i1-r) + abs(j1-c) <= 20 and (i1, j1) not in S:
                S.add((i1, j1))
                q.append((i1, j1))

def count_cheats_iter(d1: list[list[int]], d2: list[list[int]], mat: list[list[str]]):
    n, m = len(mat), len(mat[0])

    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    dirs2 = []
    for di1, dj1 in dirs:
        for di2, dj2 in dirs:
            if di1+di2 == 0 and dj1 + dj2 == 0: continue
            dirs2.append((di1+di2, dj1+dj2))

    F = defaultdict(int)
    for i, row in enumerate(mat):
        for j, el in enumerate(row):
            if el == '#': continue
            # try jumping two picoseconds in some direction and landing on a `.`

            # try jumping somewhere where manhattan distance <= 20
            for r, c in iter_manhattan(i, j, 20):
                if r < 0 or r >= n or c < 0 or c >= m: continue
                if mat[r][c] == '#': continue

                if abs(r-i) + abs(c-j) <= 20:
                    # You can jump to r, c
                    num_pic_cheat = d1[i][j]-1+abs(r-i)+abs(c-j)+d2[r][c]-1
                    num_no_cheat = d1[i][j]-1+d2[i][j]-1
                    
                    saved = num_no_cheat - num_pic_cheat
                    if saved > 0:
                        F[saved] += 1

    A = [(saved, num_cheats) for saved, num_cheats in F.items()]
    A.sort()

    ans = 0
    for saved, num_cheats in A:
        if saved >= 100:
            ans += num_cheats
        # print(f"{num_cheats=}, {saved=}")

    print(f"{ans=}")

def count_cheats(d1: list[list[int]], d2: list[list[int]], mat: list[list[str]]):
    n, m = len(mat), len(mat[0])

    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    dirs2 = []
    for di1, dj1 in dirs:
        for di2, dj2 in dirs:
            if di1+di2 == 0 and dj1 + dj2 == 0: continue
            dirs2.append((di1+di2, dj1+dj2))

    F = defaultdict(int)
    for i, row in enumerate(mat):
        for j, el in enumerate(row):
            if el == '#': continue
            # try jumping two picoseconds in some direction and landing on a `.`

            # try jumping somewhere where manhattan distance <= 20
            rr, cc = i-20, j-20

            for r in range(rr, rr+40+1):
                for c in range(cc, cc+40+1):
                    if r < 0 or r >= n or c < 0 or c >= m: continue
                    if mat[r][c] == '#': continue

                    if abs(r-i) + abs(c-j) <= 20:
                        # You can jump to r, c
                        num_pic_cheat = d1[i][j]-1+abs(r-i)+abs(c-j)+d2[r][c]-1
                        num_no_cheat = d1[i][j]-1+d2[i][j]-1
                        
                        saved = num_no_cheat - num_pic_cheat
                        if saved > 0:
                            F[saved] += 1

    A = [(saved, num_cheats) for saved, num_cheats in F.items()]
    A.sort()

    ans = 0
    for saved, num_cheats in A:
        if saved >= 100:
            ans += num_cheats
        # print(f"{num_cheats=}, {saved=}")

    print(f"{ans=}")
                

with open(file, "r") as f:
    mat = [list(r) for r in f.read().splitlines()]
    
    si, sj = -1, -1
    ei, ej = -1, -1
    for i, row in enumerate(mat):
        for j, el in enumerate(row):
            if el == 'S': si, sj = i, j
            if el == 'E': ei, ej = i, j

    d1 = bfs(si, sj, ei, ej, mat)
    d2 = bfs(ei, ej, si, sj, mat)

    count_cheats(d1, d2, mat)

