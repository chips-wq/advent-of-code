from collections import Counter
import sys

infile = "example.in" if len(sys.argv) <= 1 else sys.argv[1]

# WIDE = 11
# TALL = 7

WIDE = 101
TALL = 103
SECONDS = 7858 + 10403 * 100

"""
18260
7858

18260-7858 = 10402

"""

with open(infile, "r") as f:
    robots = []
    lines = f.read().splitlines()
    for line in lines:
        px, py = map(int, line.split("p=")[1].split(" v")[0].strip().split(","))
        vx, vy = map(int, line.split("v=")[1].strip().split(","))
        print(f"{(px, py)=}, {(vx, vy)=}")
        robots.append(((px, py), (vx, vy)))

    seconds = 7858
    while seconds <= SECONDS:
        robots2 = set([((px + seconds * vx) % WIDE, (py + seconds * vy) % TALL)  for (px, py), (vx, vy) in robots])

        # (x, y) coordinates
        print(f"{seconds=}")
        for y in range(TALL):
            line = "".join('#' if (x, y) in robots2 else '.' for x in range(WIDE))
            print(line)

        print()
        print()
        seconds += 10403

