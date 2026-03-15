from collections import defaultdict
import sys

infile = sys.argv[1] if len(sys.argv) > 1 else "example0.in"

with open(infile, "r") as f:
    inp = [list(line) for line in f.read().splitlines()]
    D = defaultdict(list)
    for i, line in enumerate(inp):
        for j, el in enumerate(line):
            if el != '.':
                D[el].append((i, j))
    print(D)
    n, m = len(inp), len(inp[0])
    antinodes = set()
    
    def valid(x: int, y: int):
        return x >= 0 and x < n and y >= 0 and y < m

    for freq, nodes in D.items():
        n_ = len(nodes)
        for i in range(n_):
            for j in range(i+1, n_):
                x1, y1 = nodes[i]
                x2, y2 = nodes[j]
                x = x2-x1
                y = y2-y1

                xx1, yy1 = x1, y1
                while valid(xx1, yy1):
                    antinodes.add((xx1, yy1))
                    xx1 -= x
                    yy1 -= y

                xx2, yy2 = x2, y2
                while valid(xx2, yy2):
                    antinodes.add((xx2, yy2))
                    xx2 += x
                    yy2 += y

    for i, line in enumerate(inp):
        line_str = ''.join('#' if (i, j) in antinodes else line[j] for j, _ in enumerate(line))
        print(line_str)

    print(f"{len(antinodes)=}")
