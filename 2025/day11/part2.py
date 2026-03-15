from collections import defaultdict
from functools import cache

"""
is this a topological graph ?

aaa -> 

How do I check if this is acyclic ?

In oriented graphs


Remember dfs coloring

black = already explored
grey = currently on the stack
white = unexplored completely

back edges = an edge pointing back to an edge that is currently grey (evidently this is a cycle)
cross edges = an edge pointing to a black edge (this is not a cycle in oriented graphs)

it's an acyclic graph, so now you can just do a dp on it to find the response
"""

import sys
infile = sys.argv[1]

START_NODE = "svr"
END_NODE = "out"

NODE_ONE = "dac"
NODE_TWO = "fft"

def dfs(node: str, coloring: dict[str, int]):
    ans = 0

    coloring[node] = 1
    for neigh in D[node]:
        if coloring[neigh] == 2: continue
        if coloring[neigh] == 1: return 1
        assert coloring[neigh] == 0
        ans = (ans | dfs(neigh, coloring))
    coloring[node] = 2

    return ans



with open(infile, "r") as f:
    lines = f.read().splitlines()
    D = defaultdict(list)
    
    for line in lines:
        node, neighs = line.split(":")
        node = node.strip()
        neighs = neighs.strip().split()
        # print(f"{node=}")
        # print(f"{neighs=}")
        # print()
        
        for neigh in neighs:
            D[node].append(neigh)

    coloring = defaultdict(int)
    cycle_exists = dfs(START_NODE, coloring)
    assert cycle_exists == 0

    @cache
    def dp(node: str, hasn1: bool, hasn2: bool):
        if node == END_NODE:
            if hasn1 and hasn2:
                return 1
            return 0

        ans = 0
        new_hasn1 = (hasn1 or node == NODE_ONE)
        new_hasn2 = (hasn2 or node == NODE_TWO)

        for neigh in D[node]:
            ans += dp(neigh, new_hasn1, new_hasn2)
        return ans
    ans = dp(START_NODE, False, False)
    print(f"{ans=}")

