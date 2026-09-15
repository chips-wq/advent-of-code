import sys

file = sys.argv[1] if len(sys.argv) > 1 else "example.in"

def union(parents: list[int], size: list[int], x: int, y: int):
    x = find(parents, x)
    y = find(parents, y)
    if x == y: return
    # I think this supposes something like it's depths is proportional to size somehow
    if size[y] < size[x]:
        parents[y] = x
        size[x] += size[y]
    else:
        parents[x] = y
        size[y] += size[x]

def find(parents: list[int], x: int):
    tmp = x
    while parents[x] != x:
        x = parents[x]
    while tmp != x:
        tmp, parents[tmp] = parents[tmp], x
    return x

with open(file) as f:
    lines = f.read().splitlines()
    lines = [list(map(int, line.split(","))) for line in lines]
    print(lines)

    n = len(lines)
    parents = [i for i in range(n)]
    size = [1] * n

    for i in range(n):
        for j in range(i+1, n):
            line1, line2 = lines[i], lines[j]
            mh = abs(line1[0] - line2[0]) + abs(line1[1] - line2[1]) + abs(line1[2] - line2[2]) + abs(line1[3] - line2[3])
            if mh <= 3:
                union(parents, size, i, j)
    S = set()
    for x in range(n):
        S.add(find(parents, x))
    print(S)
    print(len(S))
            

