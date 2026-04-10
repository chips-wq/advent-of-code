from collections import Counter
import sys

infile = "example.in" if len(sys.argv) <= 1 else sys.argv[1]

# WIDE = 11
# TALL = 7

WIDE = 101
TALL = 103
SECONDS = 100

with open(infile, "r") as f:
    robots = []
    lines = f.read().splitlines()
    for line in lines:
        px, py = map(int, line.split("p=")[1].split(" v")[0].strip().split(","))
        vx, vy = map(int, line.split("v=")[1].strip().split(","))
        print(f"{(px, py)=}, {(vx, vy)=}")
        robots.append(((px, py), (vx, vy)))

    robots2 = Counter([((px + SECONDS * vx) % WIDE, (py + SECONDS * vy) % TALL)  for (px, py), (vx, vy) in robots])

    

    q1 = 0
    for i in range(WIDE//2):
        for j in range(TALL//2):
            q1 += robots2[(i, j)]

    q2 = 0
    for i in range(WIDE//2+1, WIDE):
        for j in range(TALL//2):
            q2 += robots2[(i, j)]
    
    q3 = 0
    for i in range(WIDE//2):
        for j in range(TALL//2+1, TALL):
            q3 += robots2[(i, j)]

    q4 = 0
    for i in range(WIDE//2+1, WIDE):
        for j in range(TALL//2+1, TALL):
            q4 += robots2[(i, j)]

    print(f"{q1=}, {q2=}, {q3=}, {q4=}")
    print(q1 * q2 * q3 * q4)

    


