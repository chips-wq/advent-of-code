import sys
from collections import deque

infile = sys.argv[1]


"""
100_000 = 10**5


10**5 * 10**5 = 10**10 = like 10GB (we don't have that much)

I guess bfs from the inside and then maybe try printing (we got a lot of disk so don't try me)

"""

def bfs(si: int, sj: int, visited: set[tuple[int, int]]):
    q = deque([(si, sj)])

    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    while q:
        ci, cj = q.popleft()
        
        for di, dj in dirs:
            r, c = ci + di, cj + dj
            if (r, c) in visited: continue
            visited.add((r, c))
            q.append((r, c))

with open(infile, "r") as f:
    red = [tuple(map(int, line.split(","))) for line in f.read().splitlines()]
    assert len(set(red)) == len(red)
    n = len(red)

    for i, tup in enumerate(red):
        red[i] = (tup[1], tup[0])

    min_x, min_y = float('inf'), float('inf')
    max_x, max_y = float('-inf'), float('-inf')

    for (x, y) in red:
        min_x = min(x, min_x)
        min_y = min(y, min_y)

        max_x = max(x, max_x)
        max_y = max(y, max_y)

    points = set()

    red.append(red[0])
    for i in range(1, n+1):
        # From (i-1, i)
        px, py = red[i-1]
        cx, cy = red[i]
        if cx == px:
            for y in range(min(cy, py), max(cy,py)+1):
                points.add((cx, y))
        elif cy == py:
            for x in range(min(cx, px), max(cx, px)+1):
                points.add((x, cy))
        else:
            assert False
    red.pop()
    
    inside = (red[0][0] + 1, red[0][1] + 1)
    x1, y1 = inside


    bfs(x1, y1, points)

    print(len(points))
    print(f"{min_x=}, {min_y=}")
    print(f"{max_x=}, {max_y=}")
    # (min_x, min_y) = (0, 0)
    # (max_x, max_y) = (15, 15)

    # for x in range(min_x, max_x+1):
    #     for y in range(min_y, max_y+1):
    #         if (x, y) in red:
    #             sys.stdout.write('#')
    #         elif (x, y) in points:
    #             sys.stdout.write('X')
    #         else:
    #             sys.stdout.write('.')
    #     sys.stdout.write("\n")

