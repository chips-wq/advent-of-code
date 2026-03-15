import sys

infile = sys.argv[1]

with open(infile, "r") as f:
    points = [tuple(map(int, line.split(","))) for line in f.read().splitlines()]
    print(points)

    assert len(set(points)) == len(points)
    
    area = 0
    n = len(points)
    for i in range(n):
        for j in range(n):
            if i != j:
                dx = abs(points[i][0] - points[j][0]+1)
                dy = abs(points[i][1] - points[j][1]+1)
                area = max(area, dx * dy)
    print(f"{area=}")
