from collections import deque
import sys

infile = "example.in" if len(sys.argv) <= 1 else sys.argv[1]

D = {
    '^': (-1, 0),
    '>': (0, 1),
    'v': (1, 0),
    '<': (0, -1)
}

"""
  ^         >       d       <
(-1, 0), (0, 1), (1, 0), (0, -1)

# is there a pair to the direction on the right
# is there a pair to the direction on the left
if yes pull it with us

.#
[]
@

Crazy example:
 ..
#[].
[]..
 @


Left and right are transparent to part2

Move: >

@[][]



"""

def move_robot(ri: int, rj: int, di: int, dj: int, matrix: list[list[str]]):

    n, m = len(matrix), len(matrix[0])
    # Can I move him ?
    assert 0 <= ri < n
    assert 0 <= rj < m

    Q = deque()
    Q.append((ri, rj))
    SEEN = set()

    ok = True
    while Q:
        i, j = Q.popleft()

        if (i, j) in SEEN: continue
        SEEN.add((i, j))
        assert (i, j) in SEEN
        assert 0 <= i < n and 0 <= j < m

        if matrix[i][j] == '[':
            assert matrix[i][j+1] == ']'
            Q.append((i, j+1))

        if matrix[i][j] == ']':
            assert matrix[i][j-1] == '['
            Q.append((i, j-1))

        if matrix[i+di][j+dj] == '#':
            ok = False
            break

        if matrix[i+di][j+dj] in ['[', ']']:
            Q.append((i+di, j+dj))

    # print(ok)
    # print(SEEN)

    if ok:
        while len(SEEN) > 0:
            removed = set()
            for r, c in SEEN:
                if matrix[r+di][c+dj] == '.':
                    matrix[r+di][c+dj] = matrix[r][c]
                    matrix[r][c] = '.'
                    removed.add((r, c))
            SEEN = SEEN ^ removed

    if ok:
        return (True, ri + di, rj + dj)
    return (False, -1, -1)

with open(infile, "r") as f:
    matrix, moves = f.read().split('\n\n')
    matrix = [list(line) for line in matrix.splitlines()]

    matrix2 = []
    for _, line in enumerate(matrix):
        cline = []
        for _, el in enumerate(line):
            if el == '#':
                cline.append('#')
                cline.append('#')
            if el == 'O':
                cline.append('[')
                cline.append(']')
            if el == '.':
                cline.append('.')
                cline.append('.')
            if el == '@':
                cline.append('@')
                cline.append('.')
        matrix2.append(cline)
    matrix = matrix2

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
        # print()
        (res, nri, nrj) = move_robot(ri, rj, di, dj, matrix)
        """
        print(f"{k=}, {move=}, {res=}")
        for line in matrix:
            print("".join(line))
        """

        if res:
            ri, rj = nri, nrj
        
    ans = 0
    for i, line in enumerate(matrix):
        for j, el in enumerate(line):
            if el == '[':
                ans += (i * 100) + j
    print(f"{ans=}")
