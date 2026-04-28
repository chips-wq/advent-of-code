import sys
from collections import deque

infile = "puzzle.in" if len(sys.argv) <= 1 else sys.argv[1]

def revise_trick(i: int, j: int, D: dict[int, set[str]]):
    assert len(D[i]) > 0
    assert len(D[j]) > 0

    to_remove = set()
    if len(D[j]) > 1: return to_remove
    for vv in D[i]:
        if vv in D[j]: to_remove.add(vv)
    return to_remove

def revise(i: int, j: int, D: dict[int, set[str]]):
    to_remove = set()
    for vv in D[i]:
        # Is there someone different to `vv` in D[j]
        ok = False
        for v2 in D[j]:
            if vv != v2: ok = True
        if not ok: to_remove.add(vv)
    return to_remove

with open(infile, "r") as f:
    constraints, own_ticket, tickets = f.read().split('\n\n')
    own_ticket = list(map(int, own_ticket.splitlines()[1].split(",")))
    constraints = constraints.splitlines()

    tickets = [list(map(int, ticket.split(","))) for ticket in tickets.splitlines()[1:]]
    # print(own_ticket)
    # print(tickets)

    rngs = []
    for constraint in constraints:
        rng1, rng2 = constraint.split(": ")[1].split(" or ")
        x1, y1 = map(int, rng1.split("-"))
        x2, y2 = map(int, rng2.split("-"))

        rngs.append([(x1, y1), (x2, y2)])

    def is_valid(x: int):
        for L in rngs:
            for (x1, y1) in L:
                if x1 <= x <= y1: return True
        return False

    valid_tickets = []
    ans = 0
    for ticket in tickets:
        # How many invalid ones are in here
        invalids = [x for x in ticket if not is_valid(x)]
        #print(invalids)
        assert len(invalids) <= 1
        if invalids:
            ans += invalids[0]
        else:
            valid_tickets.append(ticket)

    m = len(rngs)
    assert m == len(valid_tickets[0])
    constraint_names = [C.split(": ")[0] for C in constraints]

    D = {i: set(constraint_names) for i in range(m)}
    # print(D)

    # Reduce the unary constraints now
    for j in range(m):
        for i in range(len(valid_tickets)):
            value = valid_tickets[i][j]
            # If this value is not present for some constraint, remove it from domain D[j]
            for k, L in enumerate(rngs):
                ok = False
                for (x1, y1) in L:
                    if x1 <= value <= y1: ok = True
                if not ok:
                    D[j].discard(constraint_names[k])

    Q = deque([])
    for i in range(m):
        for j in range(m):
            if i == j: continue
            Q.append((i, j))
    assert (len(domain) >= 1 for domain in D.values())
    
    while Q:
        i, j = Q.popleft()
        # is arc i -> j consistent
        # i.e for every possible value of X_i in D_i, there is a compatible value in X_j in D_j
        to_remove = revise_trick(i, j, D)

        if to_remove:
            D[i] = D[i] - to_remove
            if len(D[i]) == 0:
                print("IMPOSSBILE TO SATISFY CONSTRAINTS")
                exit(0)

            # Just propagate all constraints, i.e for any X_k, add the arc
            # (X_k, X_i) back here with k != i
            for k in range(m):
                if k == i: continue
                Q.append((k, i))

            # SHORTCUT
            """
            if len(D[i]) == 1:
                # Only in this case it's worth propagating into Q new constraints
                for k in range(m):
                    if k == i: continue
                    Q.append((k, i))
            """

    # print(D)
    # NOTE: The following assert only works in this case, because AC-3 reduced all domains to 1.
    assert (len(domain) == 1 for domain in D.values())
    ans = 1
    for i, value in enumerate(own_ticket):
        if list(D[i])[0].startswith("departure"):
            ans *= value
    print(f"{ans=}")




