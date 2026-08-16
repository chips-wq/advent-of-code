from copy import deepcopy
import heapq
import sys

inp = sys.argv[1] if len(sys.argv) > 2 else "example.in"

DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
MAP = ['U', 'R', 'D', 'L', 'A']


def state_key(obj):
    """Full hashable state of a robot chain: (i, j) of this robot plus
    every underlying robot's (i, j), down to (but not including) the
    stateless human base case."""
    if isinstance(obj, Robot):
        return (obj.i, obj.j) + state_key(obj.underlying)
    return ()


class Robot:
    i: int
    j: int
    board: list[list[str]]

    def __init__(self, si: int, sj: int, board: list[list[str]]):
        self.i = si
        self.j = sj
        self.board = board
        self.n = len(self.board)
        self.m = len(self.board[0])
        self.underlying = None

    def cost(self, map_symbol: str) -> int:
        # (dist, ci, cj, underlying_snapshot)
        q = [(0, self.i, self.j, self.underlying)]
        heapq.heapify(q)
        v = set()

        fi, fj, fdist, funderlying = -1, -1, -1, None

        while q:
            dist, ci, cj, underlying = heapq.heappop(q)

            if self.board[ci][cj] == map_symbol:
                fi, fj, fdist, funderlying = ci, cj, dist, underlying
                break

            key = (ci, cj) + state_key(underlying)
            if key in v:
                continue
            v.add(key)

            for di, dj in DIRS:
                r, c = ci + di, cj + dj
                if r < 0 or r >= self.n or c < 0 or c >= self.m:
                    continue
                if self.board[r][c] == '':
                    continue

                # Snapshot BEFORE mutating, so each direction is costed
                # from the same starting state, not a sibling's leftovers.
                nunderlying = deepcopy(underlying)
                move_cost = nunderlying.cost(MAP[DIRS.index((di, dj))])

                heapq.heappush(q, (dist + move_cost, r, c, nunderlying))

        self.i = fi
        self.j = fj
        self.underlying = funderlying
        return fdist + self.underlying.cost('A')

    def __lt__(self, other):
        return True


class Myself:
    i: int
    j: int
    board: list[list[str]]

    def __init__(self, si: int, sj: int, board: list[list[str]]):
        self.i = si
        self.j = sj

    def cost(self, map_symbol: str) -> int:
        return 1

    def __lt__(self, other):
        return True


def dijkstra(si: int, sj: int, board: list[list[int]], passcode: list[int], robot: Robot):
    for x in passcode:
        assert 0 <= x <= 0xA

    q = [(0, 0, si, sj, robot)]
    v = set()

    n, m = len(board), len(board[0])

    fi, fj, flvl, fdist = -1, -1, -1, -1

    while q:
        dist, lvl, i, j, robot = heapq.heappop(q)

        assert 0 <= lvl <= len(passcode)
        assert 0 <= i < n and 0 <= j < m

        key = (lvl, i, j) + state_key(robot)
        if key in v:
            continue
        v.add(key)

        if lvl == len(passcode):
            fi, fj, flvl, fdist = i, j, lvl, dist
            break

        if board[i][j] == passcode[lvl]:
            nrobot = deepcopy(robot)
            cost = nrobot.cost('A')
            heapq.heappush(q, (dist + cost, lvl + 1, i, j, nrobot))
            continue

        for di, dj in DIRS:
            r, c = i + di, j + dj
            if r < 0 or r >= n or c < 0 or c >= m:
                continue
            if board[r][c] == -1:
                continue

            nrobot = deepcopy(robot)
            cost = nrobot.cost(MAP[DIRS.index((di, dj))])

            heapq.heappush(q, (dist + cost, lvl, r, c, nrobot))

    print(f"{fi=}, {fj=}, {flvl=}, {fdist=}")


with open(inp, "r") as f:
    board = [
        [7, 8, 9],
        [4, 5, 6],
        [1, 2, 3],
        [-1, 0, 0xA]
    ]

    keypad = [
        ['', 'U', 'A'],
        ['L', 'D', 'R']
    ]

    myself = Myself(0, 0, keypad)
    robot1 = Robot(0, 2, keypad)
    robot1.underlying = myself

    robot2 = Robot(0, 2, keypad)
    robot2.underlying = robot1

    passcodes = f.read().splitlines()
    passcodes = [[int(x, 16) for x in a] for a in passcodes]

    for passcode in passcodes:
        dijkstra(3, 2, board, passcode, robot2)
