import sys


infile = sys.argv[1]

def step_remove(mat: list[list[str]]):
    ret = [list(line) for line in mat]
    dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    assert len(dirs) == 8
    
    cnt = 0
    n, m = len(mat), len(mat[0])
    for i, line in enumerate(mat):
        for j, el in enumerate(line):
            if el != '@': continue
            # Find out how many adjacent @ there are
            c_adj = 0
            for di, dj in dirs:
                r, c = i + di, j + dj
                if r < 0 or r >= n or c < 0 or c >= m: continue
                if mat[r][c] == '@': c_adj += 1
            if c_adj < 4:
                ret[i][j] = '.'
                cnt += 1
    return (ret, cnt)

def print_mat(ret: list[list[str]]):
    for line in ret:
        print("".join(line))
    print()

with open(infile, "r") as f:
    inp = [list(line) for line in f.read().splitlines()]

    ret = inp
    ans = []
    while (T := step_remove(ret)) and T[1] != 0:
        ans.append(T[1])
        ret = T[0]
    print(ans)
    
    print(f"{sum(ans)=}")

