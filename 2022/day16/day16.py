from functools import cache
from pathlib import Path
import sys

"""
     1min    (1min)
AA <-------> DD     --------> CC
 |                       |--> EE
 |
 |---------> II
 |
 |---------> BB

Is it ever worth going to a valve but not opening it ? (I think yes)

AA --------> 1 --------------> 100
            
1. go to 1, go to 100, open 100 (by minute 27) = 27 * 100 = 2700
1. go to 1, open 1, go to 100, open 100 = 28 * 1 + 26 * 100 = 2600 + 28 = 2628  (SOMETIMES it's not worth opening the valve you're on)

There's a sequence of steps that you could do:


AA <-------> DD
 |
 |
 |---------> II

1. say DD and II have quite high flow rates => 
    1. open DD
    2. go to AA
    3. open II

1. who is open
2. where i'm at
3. which minute is it

D[who is open][where i'm at][which minute is it]

"""


file = sys.argv[1] if len(sys.argv) > 1 else "example.in"

flows = {}
graph = {}
first_valve = "AA"
first_minute = 30

for line in Path(file).read_text().splitlines():
    line = line.strip().split()
    valve, flow, neighs =line[1], line[4], ''.join(line[9:])
    neighs = [neigh.strip() for neigh in neighs.split(",")]
    flow = int(flow.split("rate=")[1][:-1])

    print(f"{valve=}, {flow=}, {neighs=}")
    flows[valve] = flow
    assert valve not in graph
    graph[valve] = neighs

@cache
def f(c_open: frozenset[str], valve: str, minutes: int):
    if minutes == 0: return 0
    # How much do you win during this minute ?
    won = sum(flows[cc] for cc in c_open)
    assert all(flows[cc] != 0 for cc in c_open)

    ans = 0
    # Try opening yourself
    if valve not in c_open and flows[valve] != 0:
        ans = max(ans, f(c_open | {valve}, valve, minutes-1))

    # Try going to any of your neighbours
    for neigh in graph[valve]:
        ans = max(ans, f(c_open, neigh, minutes-1))

    return ans + won


print(f"{first_valve=}, {first_minute=}")
ans = f(frozenset(), first_valve, first_minute)
print(f"{ans=}")

