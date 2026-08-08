import sys


inp = sys.argv[1] if len(sys.argv) > 1 else "example.in"

"""
DP problem:

Given a word (W) like: brwrr

01234
brwrr

dp[i] = can you build W[:(i+1)] from your list of patterns ?

dp[i] = is there any true in the set {dp[i-len(k)] and W[i-len(k)+1:(i+1)] == k | k is a pattern}

dp[i] = how many ways are there to build W[:i] ?
dp[i] = is there any true in the set {dp[i-len(k)] and W[i-len(k):i] == k | k is a pattern}


dp[3] = 2

0  1   3
(2 ways) <-- two different ways to build this

you go to 5 and find two patterns

0  1   3           5
(2 ways)    (3 ways)

you add 2 to dp[5] 3 times, once for every pattern
"""

with open(inp, "r") as f:
    patterns, words = f.read().split('\n\n')
    words = words.splitlines()
    patterns = [p.strip() for p in patterns.split(",")]

    ans = 0
    for word in words:
        n = len(word)
        dp = [0] * (n+1)
        # dp[0], dp[1], dp[2], ..., dp[n-1], dp[n]
        dp[0] = 1
        for i in range(1, n+1):
            for k in patterns:
                if i - len(k) >= 0 and dp[i-len(k)] and word[i-len(k):i] == k:
                    dp[i] += dp[i-len(k)]
        ans += dp[n]
        print(f"{word=}, {dp[n]=}")
    print(f"{ans=}")

