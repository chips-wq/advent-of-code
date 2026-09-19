from itertools import product
from dataclasses import dataclass
from abc import ABC, abstractmethod
# from functools import cache
from pathlib import Path
from collections import deque
from typing import Union
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

# Cartesian product of possible moves

Q: Could these be dataclasses ?

Given a Move type, you come back with open_ and target I guess

2^66 <-- how do you deal with this, there's too many numbers in here
how many that can actually be opened ?

print(f"{len([idx for vv, idx in V.items() if flows[idx] != 0])=}, {first_valve=}, {first_minute=}")
this one prints 15 for the first one so only map those
"""

file = sys.argv[1] if len(sys.argv) > 1 else "example.in"

@dataclass(frozen=True)
class Open: ...

@dataclass(frozen=True)
class Go:
    target: str

# apply(open_, valve, move: Either[Open, Go])

def read_input(file):
    flows = {}
    graph = {}
    valves = set()

    ilines = Path(file).read_text().splitlines()

    for line in ilines:
        line = line.strip().split()
        valve, _, _ =line[1], line[4], ''.join(line[9:])
        valves.add(valve)

    valves = list(valves)
    valves.sort()
    V = {vv: idx for idx, vv in enumerate(valves)}

    for line in ilines:
        line = line.strip().split()
        valve, flow, neighs =line[1], line[4], ''.join(line[9:])
        neighs = [neigh.strip() for neigh in neighs.split(",")]
        flow = int(flow.split("rate=")[1][:-1])

        assert valve in valves
        assert all(vv in valves for vv in neighs)
        valve = V[valve]
        neighs = [V[vv] for vv in neighs]

        print(f"{valve=}, {flow=}, {neighs=}")
        flows[valve] = flow
        assert valve not in graph
        graph[valve] = neighs

    return V, flows, graph

V, flows, graph = read_input(file)
first_valve = V["AA"]
first_minute = 26

def generate_moves(open_: int, valve: str, flow_rate: int):
    if valve in OO and (open_ >> (OO[valve]) & 1) == 0 and flow_rate != 0:
        yield Open()
    for target in graph[valve]:
        yield Go(target)


def apply(open_: int, at: int, move: Union[Open, Go]):
    match move:
        case Open():
            return open_ | (1 << OO[at]), at
        case Go(target):
            return open_, target

def parse_open(open_: int):
    cidx = 0
    while open_:
        if open_ & 1:
            yield cidx
        open_ >>= 1
        cidx += 1

Q = deque()
D = {}
MAX_LEN = 7_000_000

# Which sort of caching policy would be most efficient here ?
def f(open_: int, valve1: int, valve2: int, minutes: int):
    if minutes == 0: return 0
    if (open_, valve1, valve2, minutes) in D:
        return D[(open_, valve1, valve2, minutes)]

    # How much do you win during this minute ?
    won = sum(flows[OO2[cidx]] for cidx in parse_open(open_))
    assert all(flows[OO2[cidx]] != 0 for cidx in parse_open(open_))
    # possible moves:
    # you open, elephant opens
    # you go to some neighbour, elephant opens
    # you open, elephant goes to some neighbour
    # you go to some neighbour, elephant goes to some neighbour

    my_moves = generate_moves(open_, valve1, flows[valve1])
    elephant_moves = generate_moves(open_, valve2, flows[valve2])

    ans = 0

    for mv1, mv2 in product(my_moves, elephant_moves):
        open1_, tg1 = apply(open_, valve1, mv1)
        open2_, tg2 = apply(open_, valve2, mv2)
        ans = max(ans, f(open1_ | open2_, tg1, tg2, minutes-1))

    Q.append((open_, valve1, valve2, minutes))
    D[(open_, valve1, valve2, minutes)] = ans + won
    if len(Q) > MAX_LEN:
        t1, t2, t3, t4 = Q.popleft()
        assert (t1, t2, t3, t4) in D
        del D[(t1, t2, t3, t4)]
    if minutes == first_minute:
        print("hello, {ans=}")
        # Ok what's the best answer here ddk
        # PRUNE.append(ans)
        # PRUNE.sort()
    if minutes % 5 == 0 and minutes > 10:
        print(f"{minutes=}, {ans=}")

    
    return ans + won


print(f"{len([idx for vv, idx in V.items() if flows[idx] != 0])=}, {first_valve=}, {first_minute=}")
# have a second contigous mapping for those

valid_opens = [idx for vv, idx in V.items() if flows[idx] != 0]
OO = {idx: ii for ii, idx in enumerate(valid_opens)}
OO2 = {cidx: oidx for oidx, cidx in OO.items()}
print(f'{len(OO)=}')

ans = f(0, first_valve, first_valve, first_minute)
print(f"{ans=}")

