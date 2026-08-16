from collections import deque
import sys

inp = sys.argv[1] if len(sys.argv) > 2 else "example.in"

def bfs1(si: int, sj: int, board: list[list[int]], passcode: list[int]):
    for x in passcode:
        assert 0 <= x <= 0xA
    q = deque([(si, sj, 0)])
    v = set([(si, sj, 0)])
    # p[r][c][lvl] = (i, j, lvl)

    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    mapping = ['>', '<', 'v', '^']

    n, m = len(board), len(board[0])

    p = [[[[] for _ in range(len(passcode) + 1)] for _ in range(m)] for _ in range(n)]
    print(f"{len(p[si][sj])=}")


    p[si][sj][0] = (si, sj, 0)
    
    fi, fj, flvl = -1, -1, -1
    while q:
        i, j, lvl = q.popleft()

        # did we finish this up ?
        if lvl == len(passcode):
            fi, fj, flvl = i, j, nlvl
            print(f"finished: {lvl=}, {passcode=}, {i=}, {j=}")
            break


        assert 0 <= i < n and 0 <= j < m
        assert board[i][j] != -1
        assert (i, j, lvl) in v

        if board[i][j] == passcode[lvl]:
            nlvl = lvl + 1

            if (i, j, nlvl) in v: continue

            p[i][j][nlvl] = (i, j, lvl)
            v.add((i, j, nlvl))
            q.append((i, j, nlvl))
            continue
        
        for di, dj in dirs:
            r, c = i + di, j + dj
            if r < 0 or r >= n or c < 0 or c >= m: continue
            if (r, c, lvl) in v: continue
            if board[r][c] == -1: continue

            p[r][c][lvl] = (i, j, lvl)
            v.add((r, c, lvl))
            q.append((r, c, lvl))

    assert flvl == len(passcode)
    path = []
    while True:
        bi, bj, blvl = p[fi][fj][flvl]

        if (fi, fj, flvl) == (bi, bj, blvl):
            break

        if blvl != flvl:
            assert blvl + 1 == flvl
            path.append('A')
        else:
            # fi, fj is r, c
            # r = i + di
            # c = j + dj
            path.append(mapping[dirs.index((fi - bi, fj - bj))])

        fi, fj, flvl = bi, bj, blvl
    path.reverse()
    print(f"{''.join(path)=}")

with open(inp, "r") as f:
    board = [
        [7, 8, 9],
        [4, 5, 6],
        [1, 2, 3],
        [-1, 0, 0xA]
    ]

    passcodes = f.read().splitlines()
    passcodes = [[int(x, 16) for x in a] for a in passcodes]
    for passcode in passcodes:
        print(f"bfs for {passcode=}")
        bfs1(3, 2, board, passcode)

        break

