import sys
from collections import deque
from functools import cache

infile = sys.argv[1]

"""
1. Add weighted buttons ?
and then run dijsktra

this is an acyclic graph <-- shortest path in some acyclic graph
the graph is immensely big

look at all buttons that have 0 in them

B0 = {all buttons that have 0 in them)

b01, b02, b03 ... b0k1 <-- we will choose joltage[0] of those

B1 = {all buttons that have 1 in them}

b11, b12, b13 ... b1k1 <-- we will choose joltage[1] of those

"""

def add_weights(buttons: list[int]):
    weighted_buttons = []
    weights = [50,30,20,1]
    
    for weight in weights:
        for button in buttons:
            weighted_buttons.append((weight, button))
    return weighted_buttons


def bfs(end_joltage, buttons):
    start_joltage = (0,) * len(end_joltage)
    q = deque([(start_joltage, 0)])
    visited = set([start_joltage])

    def increase_joltage(joltage: tuple, weighted_button: list[int]) -> tuple:
        weight, button = weighted_button
        return tuple(jj+weight if i in button else jj for i, jj in enumerate(joltage))

    while q:
        joltage, dist = q.popleft()
        print(joltage)

        # Should we prune this branch ?
        bad = False
        for j1, j2 in zip(joltage, end_joltage):
            if j1 > j2: bad = True
        if bad: continue

        if joltage == end_joltage:
            return dist

        for button in buttons:
            n_joltage = increase_joltage(joltage, button)
            if n_joltage in visited: continue
            
            visited.add(n_joltage)
            q.append((n_joltage, dist+1))

with open(infile, "r") as f:
    lines = f.read().splitlines()
    machines = []
    for line in lines:
        fp, sp = line.split("{")
        fp = fp.strip()
        sp, _ = sp.strip().split("}")
        joltage = sp.split(",")

        ffp, sfp = fp.split("]")
        _, diagram = ffp.split("[")

        buttons = sfp.strip().split()


        buttons = [list(map(int, (button[1:len(button)-1]).split(","))) for button in buttons]
        joltage = tuple(map(int, joltage))
        machines.append((diagram, buttons, joltage))
        # Parse the buttons

    ans = 0
    for k, machine in enumerate(machines):
        print(f"{k=}")
        _, buttons, start_joltage = machine
        weighted_buttons = add_weights(buttons)
        
        min_steps = bfs(start_joltage, weighted_buttons)
        # @cache
        # def dp(joltage):
        #     if any(el < 0 for el in joltage):
        #         return float('inf')
        #     if all(el == 0 for el in joltage):
        #         return 0
        #
        #     ans = float('inf')
        #     for weight, button in weighted_buttons:
        #         n_joltage = tuple(jj-weight if i in button else jj for i, jj in enumerate(joltage))
        #         ans = min(ans, 1 + dp(n_joltage))
        #     return ans
        #
        # min_steps = dp(start_joltage)

        ans += min_steps
    print(f"{ans=}")
        

    
