import sys

infile = sys.argv[1]

"""

process them by ending time 

(1, 3)
(2, 3)


3-1+1 = 3

3-3+1 = 1


(1----------4)

  (2--------4)


        (3-------------------9)
            (5-------------------------12)
(1--------------------------------------------15)


do a line sweep instead (keeping after each jump how many active ones you got) -> use events


"""

with open(infile, "r") as f:
    rngs, ids = f.read().split("\n\n")

    intervals = []
    for rng in rngs.splitlines():
        i, j = map(int, rng.split("-"))
        intervals.append((i, j))
    
    events = []
    for s, e in intervals:
        events.append((s, 1))
        events.append((e, -1))
    events.sort(key=lambda x: (x[0], -x[1]))

    n = len(events)
    assert events[0][1] == 1
    assert events[n-1][1] == -1
    pf = 1

    am = 0
    for i in range(1, n):
        x, typ = events[i]
        assert pf >= 0
        pf += typ
        # print(f"{i=}")
        # print(f"{x=}")
        # print(f"{typ=}")
        if pf == 1 and typ == 1:
            # Look at x-events[i-1][0]-1
            # if events[i-1][1] == -1:
            am += x-events[i-1][0]-1
            assert events[i-1][1] == -1
                # print(f"({events[i-1][0]+1}, {x-1})")

    total = events[n-1][0] - events[0][0] + 1
    print(f"{total-am=}")

