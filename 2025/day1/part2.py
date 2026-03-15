import sys
assert len(sys.argv) > 1

infile = sys.argv[1]
with open(infile, "r") as f:
    content = f.read().splitlines()
    cur = 50
    ans = 0
    for line in content:
        if line[0] == 'L':
            amt = int(line[1:])
            for _ in range(amt):
                cur = (cur - 1) % 100
                if cur == 0:
                    ans += 1
        elif line[0] == 'R':
            amt = int(line[1:])
            for _ in range(amt):
                cur = (cur + 1) % 100
                if cur == 0:
                    ans += 1
        else:
            assert False
    print(ans)

    
