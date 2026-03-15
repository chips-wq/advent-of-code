import sys
from collections import deque

infile = sys.argv[1]

def bfs(end_diagram, buttons):
    start_diagram = "." * len(end_diagram)
    q = deque([(start_diagram, 0)])
    visited = set([start_diagram])


    def toggle_diagram(diagram: str, button: list[int]) -> str:
        def toggle(y: str):
            assert len(y) == 1
            if y == '.': return '#'
            if y == '#': return '.'
            assert False
        
        n_diagram = "".join(toggle(el) if i in button else el for i, el in enumerate(diagram))
        return n_diagram

    while q:
        diagram, dist = q.popleft()
        
        if diagram == end_diagram:
            return dist

        for button in buttons:
            n_diagram = toggle_diagram(diagram, button)
            if n_diagram in visited: continue
            
            visited.add(n_diagram)
            q.append((n_diagram, dist+1))

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
        joltage = list(map(int, joltage))
        machines.append((diagram, buttons, joltage))
        # Parse the buttons

    ans = 0
    for machine in machines:
        end_diagram, buttons, joltage = machine
        min_steps = bfs(end_diagram, buttons)
        ans += min_steps
    print(f"{ans=}")
        

    
