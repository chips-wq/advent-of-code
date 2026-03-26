import sys

infile = "example1.in" if len(sys.argv) <= 1 else sys.argv[1]

def blink_t(x: int):
    if x == 0: return [1]
    if len(str(x)) % 2 == 0: return [int(str(x)[:len(str(x))//2]), int(str(x)[len(str(x))//2:])]
    return [x*2024]

ITERS = 25
with open(infile, "r") as f:
    A = list(map(int, (el for el in f.read().strip().split())))

    for i in range(ITERS):
        s = []
        for el in A:
            s += blink_t(el)
        A = list(s)
        # print(A)
        print(f"{len(A)=}")
        print(f"{i=}")


    num_stones = len(A)
    print(f"{num_stones=}")
