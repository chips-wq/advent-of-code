import sys

infile = "example.in" if len(sys.argv) <= 1 else sys.argv[1]

D = {
    '^': (-1, 0),
    '>': (0, 1),
    'v': (1, 0),
    '<': (0, -1)
}

def move_robot(ri: int, rj: int, di: int, dj: int, matrix: list[list[str]]):
    n, m = len(matrix), len(matrix[0])
    # Can I move him ?
    assert 0 <= ri < n
    assert 0 <= rj < m

    i, j = ri, rj
    assert matrix[i][j] == '@'

    while 0 <= i < n and 0 <= j < m and matrix[i][j] != '.':
        if matrix[i][j] == '#':
            return (False, -1, -1)
        assert matrix[i][j] in ['@', 'O']
        i += di
        j += dj
    assert matrix[i][j] == '.'
    while True:
        matrix[i][j] = matrix[i-di][j-dj]
        if matrix[i][j] == '@':
            matrix[i-di][j-dj] = '.'
            return (True, i, j)
        i -= di
        j -= dj
    assert False

with open(infile, "r") as f:
    matrix, moves = f.read().split('\n\n')
    matrix = [list(line) for line in matrix.splitlines()]

    ri, rj = -1, -1
    for i, line in enumerate(matrix):
        for j, el in enumerate(line):
            if el == '@':
                ri, rj = i, j
    assert ri != -1
    assert rj != -1

    print("INITIAL:")
    for line in matrix:
        print("".join(line))

    moves = "".join(el for el in moves.strip().splitlines())
    for k, move in enumerate(moves):
        di, dj = D[move]
        (res, nri, nrj) = move_robot(ri, rj, di, dj, matrix)
        print()
        print(f"{k=}, {move=}, {res=}")
        """
        for line in matrix:
            print("".join(line))
        """

        if res:
            ri, rj = nri, nrj
        
    ans = 0
    for i, line in enumerate(matrix):
        for j, el in enumerate(line):
            if el == 'O':
                ans += (i * 100) + j
    print(f"{ans=}")
