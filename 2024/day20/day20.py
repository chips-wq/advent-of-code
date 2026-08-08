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
            for di, dj in dirs2:
                r, c = i + di, j + dj
                if r < 0 or r >= n or c < 0 or c >= m: continue
                if mat[r][c] == '#': continue
            
                num_pic_cheat = d1[i][j]-1+2+d2[r][c]-1
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
        print(f"{num_cheats=}, {saved=}")

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

