import sys
import heapq

infile = sys.argv[1] if len(sys.argv) > 1 else "example.in"

"""
(i, j, d)

d in {0, 1, 2, 3}
     N   E  S  W

dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]

Dstart = {
    (i, j, d) -> minimal distance to get from start to (i, j, d)
}

"""


def dijkstra(si: int, sj: int, dstart: int, matrix: list[list[str]]):
    # (i, j, 0)
    q = [(0, si, sj, dstart)]
    n, m = len(matrix), len(matrix[0])
    D = {(si, sj, dstart): 0}

    dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    while q:
        dist, i, j, d = heapq.heappop(q)
        assert 0 <= d < 4

        if D.get((i, j, d), float('inf')) < dist: continue
        assert D[(i, j, d)] == dist

        # continue going forward I guess
        di, dj = dirs[d]

        neighs = [(1000, i, j, (d-1)%4), (1000, i, j, (d+1)%4), (1, i+di, j+dj, d)]

        for (cost, r, c, nd) in neighs:
            # is it a valid neighbour ?
            if r < 0 or r >= n or c < 0 or c >= m: continue
            if matrix[r][c] not in ['.', 'S', 'E']: continue
            # Relax the edge
            if cost + dist < D.get((r, c, nd), float('inf')):
                D[(r, c, nd)] = cost + dist
                heapq.heappush(q, (cost+dist, r, c, nd))

    return D

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
    Dstart = dijkstra(si, sj, 1, matrix)

    dendb = -1
    bdist = float('inf')
    for d in range(4):
        if Dstart[(ei, ej, d)] < bdist:
            bdist = Dstart[(ei, ej, d)]
            dendb = d
    dendb = (dendb+2) % 4
    print(f"{bdist=}, {dendb=}")


    # N = 0 -> S = 3
    Dend = dijkstra(ei, ej, dendb, matrix)

    def is_part(r: int, c: int):
        for d in range(4):
            if Dstart[(r, c, d)] + Dend[(r, c, (d-2)%4)] == bdist:
                return 'O'
        return '.'
    assert is_part(si, sj)
    assert is_part(ei, ej)

    tiles = 0
    for i, line in enumerate(matrix):
        ll = ''.join(is_part(i, j) if el in ['.', 'S', 'E'] else el for j, el in enumerate(line))
        tiles += sum(1 for el in ll if el == 'O')
        # print(ll)
    print(f"{tiles=}")
