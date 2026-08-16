from copy import deepcopy
from collections import deque
import heapq
import sys

inp = sys.argv[1] if len(sys.argv) > 2 else "example.in"

"""
You need to do dijksra on levels, 

(i.e: how expensive is it for me to go left right now based on the underlying machinery ?"


n1 ---> n2

cost(n1, n2) -> depends on "underlying machinery"


(-1, 0), (0, 1), (1, 0), (0, -1)
   U,       R,      D,        L

"""

DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
MAP =  ['U', 'R', 'D', 'L', 'A']



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

    def cost(self, map_symbol: str) -> int:
        # Starting from (i, j) and using the underlying machinery, how many moves
        # to get to `map_symbol`

        # do a dijkstra where costs are determined by the underlying's
        q = [(0, self.i, self.j)]
        heapq.heapify(q)
        v = set()

        fi, fj, fdist = -1, -1, -1

        # print("fun call")
        # print(f"{len(q)=}")
        while q:
            dist, ci, cj = heapq.heappop(q)
            
            # print(f"{ci=}, {cj=}, {self.board[ci][cj]=}")
            # Am I finished (i.e did I get to map_symbol)
            if self.board[ci][cj] == map_symbol:
                fi, fj, fdist = ci, cj, dist
                # print(f"{ci=}, {cj=}")
                break

            if (ci, cj) in v:
                continue
            # Can you relax ?
            v.add((ci, cj))

            for di, dj in DIRS:
                cost = self.underlying.cost(MAP[DIRS.index((di,dj))])
                r, c = ci + di, cj + dj
                if r < 0 or r >= self.n or c < 0 or c >= self.m:
                    continue
                if self.board[r][c] == '':
                    continue
                heapq.heappush(q, (dist + cost, r, c))


        # Now has expensive is it to press the button ?
        # print(f"{fi=}, {fj=}, {fdist=}")
        self.i = fi
        self.j = fj
        return fdist + self.underlying.cost('A')

    def __lt__(self, other):
        return 'YES'

class Myself:
    i: int
    j: int
    board: list[list[str]]

    def __init__(self, si: int ,sj: int, board: list[list[str]]):
        self.i = si
        self.j = sj

    def cost(self, map_symbol: str) -> int:
        return 1

def dijkstra(si: int, sj: int, board: list[list[int]], passcode: list[int], robot: Robot):
    for x in passcode:
        assert 0 <= x <= 0xA

    q = [(0, 0, si, sj, robot)]
    # (distance, lvl, i, j, robot)

    v = set()

    n, m = len(board), len(board[0])

    fi, fj, flvl, fdist = -1, -1, -1, -1

    while q:
        dist, lvl, i, j, robot = heapq.heappop(q)
        
        assert 0 <= lvl <= len(passcode)
        assert 0 <= i < n and 0 <= j < m

        if (lvl, i, j) in v:
            continue

        v.add((lvl, i, j))

        # Is this over ?
        if lvl == len(passcode):
            fi, fj, flvl, fdist = i, j, lvl, dist
            break

        # Is this just a press move ?
        if board[i][j] == passcode[lvl]:
            nrobot = deepcopy(robot)
            cost = nrobot.cost('A')
            heapq.heappush(q, (dist + cost, lvl+1, i, j, nrobot))

            continue
            
        
        for di, dj in DIRS:
            r, c = i + di, j + dj
            if r < 0 or r >= n or c < 0 or c >= m: continue
            if board[r][c] == -1: continue
            
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
        ['L','D', 'R']
    ]

    robot = Robot(0, 2, keypad)

    robot.underlying = Myself(0, 0, keypad)

    myself = Myself(0, 0, keypad)
    robot1 = Robot(0, 2, keypad)
    robot1.underlying = myself

    robot2 = Robot(0, 2, keypad)
    robot2.underlying = robot1

    
    passcodes = f.read().splitlines()
    passcodes = [[int(x, 16) for x in a] for a in passcodes]

    for passcode in passcodes:
        dijkstra(3, 2, board, passcode, robot2)
        break

    # Just ask robot2 how expensive things are
