import sys


inp = sys.argv[1] if len(sys.argv) > 1 else "inp.in"

"""
DP problem:

Given a word (W) like: brwrr

01234
brwrr

dp[i] = can you build W[:(i+1)] from your list of patterns ?

dp[i] = is there any true in the set {dp[i-len(k)] and W[i-len(k)+1:(i+1)] == k | k is a pattern}

dp[i] = can you build W[:i] from your list of patterns ?
dp[i] = is there any true in the set {dp[i-len(k)] and W[i-len(k):i] == k | k is a pattern}

012345
brwrr
"""

with open(inp, "r") as f:
    patterns, words = f.read().split('\n\n')
    words = words.splitlines()
    patterns = [p.strip() for p in patterns.split(",")]

    ans = 0
    for word in words:
        n = len(word)
        dp = [False] * (n+1)
        # dp[0], dp[1], dp[2], ..., dp[n-1], dp[n]
        dp[0] = True
        for i in range(1, n+1):
            for k in patterns:
                if i - len(k) >= 0 and dp[i-len(k)] and word[i-len(k):i] == k:
                    dp[i] = True
                    break
        if dp[n]:
            ans += 1
        print(f"{word=}, {dp[n]=}")
    print(f"{ans=}")

