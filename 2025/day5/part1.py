import sys

infile = sys.argv[1]

with open(infile, "r") as f:
    rngs, ids = f.read().split("\n\n")

    intervals = []
    for rng in rngs.splitlines():
        i, j = map(int, rng.split("-"))
        intervals.append((i, j))
    

    ids = list(map(int, ids.splitlines()))
    
    ans = 0
    for ii in ids:
        ok = False
        for (l, r) in intervals:
            if l <= ii <= r:
                ok = True
                break
        if ok:
            ans += 1
    print(f"{ans=}")
