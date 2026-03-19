import sys

infile = "example1.in" if len(sys.argv) <= 1 else sys.argv[1]

"""
(character, times_repeated) ... 

decreasing file_id means from right to left I guess

(id0, x0), ('.', x1), (id1, x1), ('.', x2), ..... (idn, x4)

Find the first `idx` to the left of idn s.t x_idx >= x4
I guess you could then mutate the structure in place.

Q: Is there a natural way of doing this ?

Mutating the whole array is easiest I think and it will run (though a little slower)

1. Find a candidate from the right
2. Do a for loop from i = 0 all the way up
3. If you found something fitting
    1. Decrease the amount of free space
    2. Insert the actual thing

Your index actually got "subtracted" by itself if decreasing the amount of free space didn't make it == 0
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
    #print(sf)

    #print(f"{len(sf)=}")
    i = len(sf)-1

    while i >= 0:
        ch, times = sf[i]
        if times == 0:
            i -= 1
            continue
        if ch == '.':
            i -= 1
            continue
        # We have a real candidate here
        ok = False
        for j in range(i):
            if sf[j][0] != '.': continue
            if sf[j][1] < times: continue
            assert sf[j][0] == '.' and sf[j][1] >= times
            sf[i][0] = '.'

            sf[j][1] -= times
            sf.insert(j, [ch, times])
            ok = True
            break

        if not ok: i -= 1
        # print(f"{sf=}, {ok=}, {i=}")

    j = 0
    check = 0
    for el, times in sf:
        for _ in range(times):
            if el != '.':
                check += (j * int(el))
            j += 1
    print(f"{check=}")
