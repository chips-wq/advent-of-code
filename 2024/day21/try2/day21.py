from functools import cache
from collections import deque, defaultdict
import sys
import string

"""

^^<A               <-- what top wants
<A, A, V<A, >>^A   <-- what robot1 needs to do under it
for 1st:
    [V<<A, >>^A]
for 2nd:
    [A]
for 3rd:
    [V<A, <A, >>^A]

a robot, is always given a sequence like: (always ends in A)
[x1, x2, x3 ... A]
he must be able to map each of these to what the "underlying chain" must do, which is esentially:
how do i move to hit x1, then x2, then x3 (I think this is a complex state bfs)
first try to get to x1, then try to get to x2, then try to get to x4, after you get to each one
you emit the next sequence for then underlying chain

a robot executing one of these sequences "ALWAYS" returns to A

there is a special robot called a human and he can execute this sequence in len(seq) steps (i.e by just pressing those)

Let's say you have your original keypad here:

+---+---+---+
| 7 | 8 | 9 |
+---+---+---+
| 4 | 5 | 6 |
+---+---+---+
| 1 | 2 | 3 |
+---+---+---+
    | 0 | A |
    +---+---+

robot1: (imagine initially arm hovering over A)
    +---+---+
    | ^ | A |
+---+---+---+
| < | v | > |
+---+---+---+

robot2: (imagine initially arm hovering over A)
    +---+---+
    | ^ | A |
+---+---+---+
| < | v | > |
+---+---+---+

get_cost(U, L, 1) -> [DL]

Imagine I initially want to hit that 5 so I would like robot1 to press in sequence:
^^<A

robot1 has to press:
1. ^

so it's arm must be moved to the left and then it has to go forward
(which means the robot2 behind it must do: human must do the following:
1. V, <, <, A, >, >, ^, A (first part moves it over ^, then second part actually presses it), notice we just got back to A

2. ^ (robot one presses this again), arm is already hoveing over that so robot under it, just has to go forward, human does:
A

3. < (robot presses left), so the robot under it must press, "V<A", so the human doing robot1 must do
V, <, A, <, A, >, >, ^, A (ends up at A after doing this multiple pass)


upper command chain always ends with A, it's usually just multiple things like:

[x1, x2, x3, x4, A]

We will pretend you can just come up with a minimal sequence bfs separated by A's, give this to underlyings and actually solve the problem


<<^A

    +---+---+
    | ^ | A |
+---+---+---+
| < | v | > |
+---+---+---+

human

V<<AA>^A>A

but if we had <^<A

human

V<<A>^AV<A>>^A <-- much longer so how do I do this, do I use all shortest paths, maybe there even is a longer path that results shorter down the chain

"""

def get_shortest_paths(start: str, end: str, grid: list[list[str]]):
    si, sj = -1, -1
    ei, ej = -1, -1
    for i, row in enumerate(grid):
        for j, el in enumerate(row):
            if el == start:
                si, sj = i, j
            if el == end:
                ei, ej = i, j

    q = deque([(si, sj)])
    V = set([(si, sj)])
    P = defaultdict(list)
    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    dirsm = {
        (-1, 0): 'U',
        (1 , 0): 'D',
        (0 , 1): 'R',
        (0 ,-1): 'L'
    }
    
    n, m = len(grid), len(grid[0])

    while q:
        ff = len(q)
        V2 = set()
        for _ in range(ff):
            i, j = q.popleft()
            for di, dj in dirs:
                r, c = i + di, j + dj
                if r < 0 or r >= n or c < 0 or c >= m:
                    continue
                if grid[r][c] == 'X': continue
                if (r, c) in V: continue
                
                if (r, c) not in V2:
                    V2.add((r, c))
                    q.append((r, c))
                
                P[(r, c)].append((i, j))
        V.update(V2)

    
    ans = []
    ansl = []
    def bkt(c: tuple[int, int], sol: list[tuple[int, int]]):
        sol.append(c)
        if not P[c]:
            ans.append(list(reversed(sol)))
            sol.pop()
            return
        for p in P[c]:
            bkt(p, sol)
        sol.pop()

    bkt((ei, ej), [])

    for ll in ans:
        ff = len(ll)
        ll2 = []
        for i in range(1, ff):
            dx, dy = ll[i][0] - ll[i-1][0], ll[i][1] - ll[i-1][1]
            ll2.append(dirsm[(dx, dy)])
        ansl.append(ll2)

    return ansl


grid = [["7", "6", "0"], ["8", "3", "4"], ["1", "2", "9"]]
start = "7"
end = "9"

get_shortest_paths(start, end, grid)


grids = {
    0: [["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"], ["X", "0", "A"]],
    1: [["X", "U", "A"], ["L", "D", "R"]]
}

@cache
def get_cost(s1: str, s2: str, depth: int):
    assert depth >= 0 and len(s1) == 1 and len(s2) == 1
    if depth == 0: return 1
    # print(f"{s1=}, {s2=}, {depth=}")
    # assert not (s1 == 'A' and s2 == 'A')
    assert not (s1 == 'X' or s2 == 'X')

    S1 = set([el for row in grids[0] for el in row])
    S2 = set([el for row in grids[1] for el in row])
    
    grid_idx = 0
    if ((s1 != 'A' and s1 in S2) or (s2 != 'A' and s2 in S2)): grid_idx = 1

    cgrid = grids[grid_idx]

    #print()
    shortest_paths = get_shortest_paths(s1, s2, cgrid)
    assert shortest_paths
    real_ans = float('inf')

    for path in shortest_paths:
        # What's the cost of this path ?
        path.insert(0, 'A')
        path.append('A')
        ans = 0
        for i in range(1, len(path)):
            ans += get_cost(path[i-1], path[i], depth-1)
        real_ans = min(real_ans, ans)
    return real_ans

    # print(f"{s1=}, {s2=}, {depth=}")
    # print(f"{cgrid=}")
    # print(f"{shortest_paths=}")
    # print(S1)
    # print(S2)
    # print()

# 26 robots for part2
# 3 robots for part1
DEPTH = 26

file = sys.argv[1] if len(sys.argv) > 1 else "input.in"

print(f"{file=}")

with open(file, "r") as f:
    res = 0
    for line in f.read().splitlines():
        line = [el for el in line]
        line.insert(0, 'A')
        n = len(line)
        ans = 0
        for i in range(1, n):
            # print(f"{line[i-1]=}, {line[i]=}")
            ans += get_cost(line[i-1], line[i], DEPTH)
        int_part = int(''.join(el for el in line if el in string.digits))
        print(f"{ans=}")
        print(f"{int_part=}")
        res += ans * int_part
    print(f"{res=}")
        # break

