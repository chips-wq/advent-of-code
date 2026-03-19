import sys

infile = "example1.in" if len(sys.argv) <= 1 else sys.argv[1]

"""
(character, times_repeated)


also take a stack of some sort I guess
1. just as you go forward drop everything that's not a `.` into a stack


"""

with open(infile, "r") as f:
    line = f.read().strip()

    sf = []
    for i, el in enumerate(line):
        if int(el) == 0: continue
        if (i % 2 == 0):
            idx = i//2
            sf.append([str(idx), int(el)])
        else:
            sf.append(['.', int(el)])
    print(sf)

    i = 0
    res = []
    while i < len(sf):
        tup = sf[i]
        ch, times = tup
        if times == 0:
            i += 1
            continue

        if ch != '.':
            res.append(tuple(tup))
            i += 1
            continue

        if sf[-1][0] == '.' or sf[-1][1] == 0:
            sf.pop()
            continue
        
        # sf[i][0] == '.' (so it's free space)
        # sf[-1][0] != '.' (so you can take from there)
        
        # Take as much as you possibly can 
        # Case 1: x1 < x2 (so you can fulfill all of the x1 ones and subtract x1 from the one to the right)
        # Case 2: x1 > x2 (so you can fulfill all of the x2 from the right and then still be left with some

        assert sf[i][0] == '.'
        assert sf[i][1] > 0
        assert sf[-1][0] != '.'
        assert sf[-1][1] > 0
        decr = min(sf[i][1], sf[-1][1])
        res.append((sf[-1][0], decr))
        sf[i][1] -= decr
        sf[-1][1] -= decr

    j = 0
    check = 0
    for el, times in res:
        el = int(el)
        for _ in range(times):
            check += (j * el)
            j += 1
    print(f"{check=}")
