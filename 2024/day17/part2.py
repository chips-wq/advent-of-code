import sys
from math import log2, floor
infile = sys.argv[1] if len(sys.argv) > 1 else "example.in"

"""
Our puzzle program:
rb = rc = 0
program = [2,4,1,4,7,5,4,1,1,4,5,5,0,3,3,0]

bst 4
bxl 4
cdv 5
bxc 1
bxl 4

out 5
adv 3
jnz 0

Translating to C-like language:

start:
B = A % 8         |
B = B^4           |     B = (A % 8) ^ 4   |  
C = A / (2**B)    |     C = A / (2 ^ B)   |  C = A / (1 << ((A % 8) ^ 4))
B = B^C           |     B = B ^ C ^ 4     |  print((A % 8) ^ 42,4,1,4,7,5,4,1,1,4,5,5,0,3,3,01
B = B^4           |<-- A %

print(B % 8)
A = A / 8
goto start

Translate again:
    
1. look at the last 3 bits (A_3), and xor them with 4 (B)
2. A2 = A take away B bits
3. Xor A_3 with A2_3
"""

with open(infile, "r") as f:
    regs, program = f.read().split('\n\n')
    ra, rb, rc = [int(reg.split(": ")[1].strip()) for reg in regs.splitlines()]
    program = list(map(int, program.split(": ")[1].strip().split(',')))
    print(f"{ra=}, {rb=}, {rc=}, {program=}")
    program_serialized = ','.join(str(el) for el in program)

    outs = []

    def bkt(i: int, A: int):
        if i < 0:
            outs.append(A)
            print(A)
            return
        
        for k in range(8):
            nA = A
            nA |= (k << (i * 3))

            # What restriction does this impose to the left of me ?
            B = (k ^ 4)
            restriction = ((nA >> (i * 3 + B)) & 7)
            
            if (restriction ^ k) != program[i]:
                continue
            
            bkt(i-1, nA)

    bkt(15, 0)
    
    for o in outs:
        print(f"{o=}, needs {floor(log2(o)) + 1} bits.")



