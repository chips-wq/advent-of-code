import sys
import heapq

infile = sys.argv[1] if len(sys.argv) > 1 else "example.in"

"""
(i, j, d)

d in {0, 1, 2, 3}
     N   E  S  W

dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]

"""


def dijkstra(si: int, sj: int, ei: int, ej: int, matrix: list[list[str]]):
    # (i, j, 0)
    q = [(0, si, sj, 1)]
    V = set()
    n, m = len(matrix), len(matrix[0])

    dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    while q:
        dist, i, j, d = heapq.heappop(q)
        assert 0 <= d < 4
        
        if (i, j, d) in V: continue
        V.add((i, j, d))

        # print(f"State = {i=}, {j=}, {d=} and distance is {dist=}")

        if (i, j) == (ei, ej):
            print(f"Reached {ei=}, {ej=} {d=} in distance {dist}")

        # continue going forward I guess
        di, dj = dirs[d]

        neighs = [(1000, i, j, (d-1)%4), (1000, i, j, (d+1)%4), (1, i+di, j+dj, d)]

        for (cost, r, c, nd) in neighs:
            # is it a valid neighbour ?
            if r < 0 or r >= n or c < 0 or c >= m: continue
            if matrix[r][c] not in ['.', 'S', 'E']: continue
            if (r, c, nd) in V: continue
            heapq.heappush(q, (dist+cost, r, c, nd))

with open(infile, "r") as f:
    matrix = [list(line) for line in f.read().splitlines()]
    si, sj = -1, -1
    ei, ej = -1, -1
    for i, line in enumerate(matrix):
        for j, el in enumerate(line):
            if el == 'S':
                si, sj = i, j
            if el == 'E':
                ei, ej = i, j
    print(f"{si=}, {sj=}, {ei=}, {ej=}")
    dijkstra(si, sj, ei, ej, matrix)
