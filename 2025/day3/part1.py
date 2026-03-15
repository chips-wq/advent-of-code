import sys

infile = sys.argv[1]

with open(infile, "r") as f:
    content = f.read().splitlines()
    res = 0
    for line in content:
        line = list(map(int, line.strip()))

        sm = list(line)
        n = len(line)
        for i in range(n-2, -1, -1):
            sm[i] = max(sm[i], sm[i+1])

        ans = 0
        for i in range(n-2, -1, -1):
            ans = max(ans, line[i] * 10 + sm[i+1])
        print(f"{ans} -> {line}")
        res += ans
    print(res)

