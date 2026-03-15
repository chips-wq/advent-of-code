import sys

infile = sys.argv[1]

"""
Choose 12 to maximize that sum

n-i >= 12

n-12 >= i

i <= n-12

take the biggest one that is `9`

plan:
    always take the biggest number and most to the left 
    with the condition that i <= n-x

x = 12,11,10.....1

two loops or something

greedy
"""

def take_best(digits: list[int]):
    n = len(digits)
    assert n >= 12

    ans = []
    idx = 0
    x = 12

    for x in range(12, 0, -1):
        # x <- [12..1]
        # [idx, n-x] is a valid range to find the best one
        c_digit, c_idx = -1, -1
        for i in range(idx, n-x+1):
            if digits[i] > c_digit:
                c_digit = digits[i]
                c_idx = i
        ans.append(c_digit)
        idx = c_idx + 1
    # print(len(ans))
    # print(ans)
    return int("".join(str(el) for el in ans))

with open(infile, "r") as f:
    content = f.read().splitlines()
    res = 0
    for line in content:
        line = list(map(int, line.strip()))

        res += take_best(line)
    print(f"{res=}")
