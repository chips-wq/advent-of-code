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
            cur = (cur - amt) % 100
        elif line[0] == 'R':
            amt = int(line[1:])
            cur = (cur + amt) % 100
        else:
            assert False

        if cur == 0:
            ans += 1
    print(ans)
    
