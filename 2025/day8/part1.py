import sys

infile = sys.argv[1]

FIRST = 1000

def get_distance(p1, p2):
    return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2

def find(x: int, parents: list[int]):
    tmp = x
    while parents[tmp] != tmp:
        tmp = parents[tmp]
    # tmp is now the root
    while parents[x] != x:
        parents[x], x = tmp, parents[x]
    return tmp

def union(x: int, y: int, parents: list[int], sizes: list[int]):
    x = find(x, parents)
    y = find(y, parents)
    if x == y: return
    
    if sizes[x] < sizes[y]:
        parents[x] = y
        sizes[y] += sizes[x]
    else:
        parents[y] = x
        sizes[x] += sizes[y]

with open(infile, "r") as f:
    lines = f.read().splitlines()
    points = []
    for line in lines:
        P = tuple(map(int, line.split(",")))
        points.append(P)
    n = len(points)

    parents = [i for i in range(n)]
    sizes = [1] * n

    # 10 shortest connections
    distances = []
    for i in range(n):
        for j in range(i + 1, n):
            p1, p2 = points[i], points[j]
            distances.append((get_distance(p1, p2), (i, j)))
    distances.sort()

    for _, (i, j) in distances[:FIRST]:
        union(i, j, parents, sizes)

    print(f"{n=}")
    # Compress
    for i in range(n):
        find(i, parents)

    circuit_sizes = []
    for i in range(n):
        if parents[i] == i:
            circuit_sizes.append(sizes[i])
    circuit_sizes.sort(reverse=True)
    print(circuit_sizes)
    print(f"{circuit_sizes[0] * circuit_sizes[1] * circuit_sizes[2]=}")
            

