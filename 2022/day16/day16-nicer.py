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
    for line in Path(file).read_text().splitlines():
        line = line.strip().split()
        valve, flow, neighs =line[1], line[4], ''.join(line[9:])
        neighs = [neigh.strip() for neigh in neighs.split(",")]
        flow = int(flow.split("rate=")[1][:-1])

        print(f"{valve=}, {flow=}, {neighs=}")
        flows[valve] = flow
        assert valve not in graph
        graph[valve] = neighs
    return flows, graph

first_valve = "AA"
first_minute = 26
flows, graph = read_input(file)


def generate_moves(open_: frozenset[str], valve: str, flow_rate: int):
    if valve not in open_ and flow_rate != 0:
        yield Open()
    for target in graph[valve]:
        yield Go(target)


def apply(open_: frozenset[str], at: str, move: Union[Open, Go]):
    match move:
        case Open():
            return open_ | {at}, at
        case Go(target):
            return open_, target

Q = deque()
D = {}
MAX_LEN = 7_000_000

# Which sort of caching policy would be most efficient here ?
def f(open_: frozenset[str], valve1: str, valve2: str, minutes: int):
    if minutes == 0: return 0
    if (open_, valve1, valve2, minutes) in D:
        return D[(open_, valve1, valve2, minutes)]

    # How much do you win during this minute ?
    won = sum(flows[cc] for cc in open_)
    assert all(flows[cc] != 0 for cc in open_)
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
    
    return ans + won


print(f"{first_valve=}, {first_minute=}")
ans = f(frozenset(), first_valve, first_valve, first_minute)
print(f"{ans=}")

