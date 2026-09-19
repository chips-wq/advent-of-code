from abc import ABC, abstractmethod
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

# Cartesian product of possible moves

Q: Could these be dataclasses ?
"""

class Move(ABC):
    @abstractmethod
    def apply(self):
        pass

    @abstractmethod
    def can_apply(self):
        pass

class OpenMove(Move):
    def __init__(self, c_open: frozenset[str], valve: str, minutes: int, flow_rate: int):
        self.c_open = c_open
        self.valve = valve
        self.minutes = minutes
        self.flow_rate = flow_rate

    def apply(self):
        assert self.can_apply()
        return (self.c_open | {self.valve}, self.valve, self.minutes-1)
    
    def can_apply(self):
        return self.valve not in self.c_open and self.flow_rate != 0

class NeighbourMove(Move):
    def __init__(self, c_open: frozenset[str], valve: str, minutes: int, neighbour: str):
        self.c_open = c_open
        self.valve = valve
        self.minutes = minutes
        self.neighbour = neighbour

    def apply(self):
        assert self.can_apply()
        return (self.c_open, self.neighbour, self.minutes-1)
    
    def can_apply(self):
        return True

file = sys.argv[1] if len(sys.argv) > 1 else "example.in"

flows = {}
graph = {}
first_valve = "AA"
first_minute = 26

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
def f(c_open: frozenset[str], valve1: str, valve2: str, minutes: int):
    if minutes == 0: return 0
    # How much do you win during this minute ?
    won = sum(flows[cc] for cc in c_open)
    assert all(flows[cc] != 0 for cc in c_open)

    # possible moves:
    # you open, elephant opens
    # you go to some neighbour, elephant opens
    # you open, elephant goes to some neighbour
    # you go to some neighbour, elephant goes to some neighbour

    my_moves = [OpenMove(c_open, valve1, minutes, flows[valve1]), *([NeighbourMove(c_open, valve1, minutes, neigh) for neigh in graph[valve1]])]

    elephant_moves = [OpenMove(c_open, valve2, minutes, flows[valve2]), *([NeighbourMove(c_open, valve2, minutes, neigh) for neigh in graph[valve2]])]


    ans = 0

    for move1 in my_moves:
        if not move1.can_apply(): continue
        for move2 in elephant_moves:
            if not move2.can_apply(): continue
            c_open1, valve1, _ = move1.apply()
            c_open2, valve2, _ = move2.apply()
            ans = max(ans, f(c_open1 | c_open2, valve1, valve2, minutes-1))

    return ans + won


print(f"{first_valve=}, {first_minute=}")
ans = f(frozenset(), first_valve, first_valve, first_minute)
print(f"{ans=}")

