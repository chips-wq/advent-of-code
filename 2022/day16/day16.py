from itertools import product
from dataclasses import dataclass
from abc import ABC, abstractmethod
# from functools import cache
from pathlib import Path
from collections import deque, defaultdict
from typing import Union
from functools import cache
from collections import deque
import sys

file = sys.argv[1] if len(sys.argv) > 1 else "example.in"

def read_input(file):
    valves = set()

    ilines = Path(file).read_text().splitlines()

    for line in ilines:
        line = line.strip().split()
        valve, _, _ =line[1], line[4], ''.join(line[9:])
        valves.add(valve)

    valves = list(valves)
    valves.sort()
    V = {vv: idx for idx, vv in enumerate(valves)}

    graph = [[] for _ in range(len(valves))]
    flows = [-1] * len(valves)

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

    # Now preprocess this input I guess
    # from anyone who has flow_rate != 0, we want to know what's the smallest distance to get to anyone else
    def bfs(valve: int, graph: list[list[int]], flows: list[int]):
        q = deque([valve])
        d = [0] * len(valves)
        d[valve] = 1
        while q:
            vv = q.popleft()
            for nn in graph[vv]:
                if d[nn] != 0: continue
                q.append(nn)
                d[nn] = d[vv] + 1
        return d

    # We want a mapping from valve -> relevant valve (one where it's not 0)
    relevant_valves = [V[valve] for valve in valves if flows[V[valve]] != 0]
    relevant_valves.insert(0, 0)
    
    rgraph = [[] for _ in range(len(relevant_valves))]
    valve_mapping = {v: idx for idx, v in enumerate(relevant_valves)}
    print(valve_mapping)

    for rv in relevant_valves:
        d = bfs(rv, graph, flows)
        assert len(d) == len(valves)
        assert (flows[rv] != 0 or rv == 0)
        for valve, dd in enumerate(d):
            if valve == rv: continue
            if flows[valve] == 0: continue
            assert flows[valve] != 0
            print(f"{valve=}")
            print(f"{valve_mapping=}")
            print(f"{flows[valve]=}")
            rgraph[valve_mapping[rv]].append((valve_mapping[valve], dd, flows[valve]))

    flows2 = [-1] * len(relevant_valves)
    for rv in relevant_valves:
        flows2[valve_mapping[rv]] = flows[rv]

    return rgraph, flows2

# (seen so far, current, minutes)
@cache
def foo(open_: int, current: int, minutes: int):
    if minutes == 0:
        return 0
    if minutes < 0:
        return float('-inf')

    per_minute = 0
    for kk in range(32):
        if (open_ >> kk) & 1 == 1:
            per_minute += flows[kk]
    
    # do nothing make a move
    ans = per_minute + foo(open_, current, minutes-1)
    for (neigh, cost, _) in graph[current]:
        ans = max(ans, per_minute * cost + foo(open_ | (1 << neigh), neigh, minutes-cost))
    return ans

# if I keep on going with my current mask, how much do I win ?

# There's multiple ways to arrive at a certain mask, so each time you do arrive at that mask
# if you can get a better "score", then store that somewhere
best = defaultdict(int)
def bar(open_: int, current: int, minutes: int, pressure: int):
    assert 1 <= minutes
    if pressure > best[open_]:
        best[open_] = pressure

    for (neigh, cost, flow) in graph[current]:
        if minutes - cost < 1: continue
        if (open_ >> neigh) & 1: continue
        bar(open_ | (1 << neigh), neigh, minutes-cost, (minutes-cost) * flow + pressure)


"""
Think of best[mask] as:
    1. there is a certain path, using some amount of minutes to open everything as according to mask
    2. which would then lead me if I then stop to win best[mask]
    3. this path is optimal in the sense that there is no other way to reach mask and then stop and then win more

If you have best[mask1], best[mask2]. You can think of these as two independent paths if they are disjoint.

"""

graph, flows = read_input(file)
bar(0, 0, 26, 0)

T = sorted(best.items(), key=lambda x: x[1], reverse=True)
# Pick two indices, i1, i2
nn = len(T)
ans = 0
for i1, (m1, p1) in enumerate(T):
    for i2, (m2, p2) in enumerate(T[i1+1:]):
        if (m1 & m2) != 0: continue
        ans = max(ans, p1 + p2)
print(ans)
