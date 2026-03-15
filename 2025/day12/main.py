import sys

infile = sys.argv[1]

with open(infile, "r") as f:
    _, sp = f.read().split("\n\n\n")
    sp = sp.strip().splitlines()
    ans = 0
    print(sp)
    for line in sp:
        size_str, amounts = line.split(":")
        width, height = map(int, size_str.split("x"))

        amounts = list(map(int, amounts.strip().split()))
        
        can_place = (width // 3) * (height // 3)

        has_to_place = sum(amounts)

        if has_to_place <= can_place:
            ans += 1
    print(f"{ans=}")
