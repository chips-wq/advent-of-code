import sys

infile = "day16.in" if len(sys.argv) <= 1 else sys.argv[1]

with open(infile, "r") as f:
    constraints, own_ticket, tickets = f.read().split('\n\n')
    own_ticket = list(map(int, own_ticket.splitlines()[1].split(",")))

    tickets = [list(map(int, ticket.split(","))) for ticket in tickets.splitlines()[1:]]
    print(own_ticket)
    print(tickets)

    rngs = []
    for constraint in constraints.splitlines():
        rng1, rng2 = constraint.split(": ")[1].split(" or ")
        x1, y1 = map(int, rng1.split("-"))
        rngs.append((x1, y1))
        x1, y1 = map(int, rng2.split("-"))
        rngs.append((x1, y1))

    def is_valid(x: int):
        for (x1, y1) in rngs:
            if x1 <= x <= y1: return True
        return False

    ans = 0
    for ticket in tickets:
        # How many invalid ones are in here
        invalids = [x for x in ticket if not is_valid(x)]
        #print(invalids)
        assert len(invalids) <= 1
        if invalids:
            ans += invalids[0]
    print(f"{ans=}")

