from collections import defaultdict

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

START_NODE = "you"
END_NODE = "out"

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

    def dp(node: str):
        if node == END_NODE:
            return 1
        ans = 0
        for neigh in D[node]:
            ans += dp(neigh)
        return ans
    ans = dp(START_NODE)
    print(f"{ans=}")

    
    

