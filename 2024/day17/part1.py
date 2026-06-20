import sys

infile = sys.argv[1] if len(sys.argv) > 1 else "example.in"

def get_operand(operand: int, ra: int, rb: int, rc: int, combo=False):
    if not combo: return operand
    assert operand != 7
    assert combo
    if 0 <= operand <= 3: return operand
    match operand:
        case 4: return ra
        case 5: return rb
        case 6: return rc
        case _: assert False
    assert False

with open(infile, "r") as f:
    regs, program = f.read().split('\n\n')
    ra, rb, rc = [int(reg.split(": ")[1].strip()) for reg in regs.splitlines()]
    program = list(map(int, program.split(": ")[1].strip().split(',')))
    print(f"{ra=}, {rb=}, {rc=}, {program=}")

    out = []
    n = len(program)
    assert n % 2 == 0
    # the instruction pointer
    ip = 0
    while ip < n:
        assert ip % 2 == 0
        assert ip + 1 < n

        opcode = program[ip]
        operand = program[ip+1]
        match opcode:
            case 0:
                # adv
                ra = ra // (2 ** get_operand(operand, ra, rb, rc, combo=True))
            case 1:
                rb = (rb ^ get_operand(operand, ra, rb, rc))
            case 2:
                rb = get_operand(operand, ra, rb, rc, combo=True) % 8
            case 3:
                if ra != 0:
                    ip = get_operand(operand, ra, rb, rc)
                    assert ip % 2 == 0
                    continue
            case 4:
                rb = (rb ^ rc)
            case 5:
                out.append(get_operand(operand, ra, rb, rc, combo=True) % 8)
            case 6:
                rb = ra // (2 ** get_operand(operand, ra, rb, rc, combo=True))
            case 7:
                rc = ra // (2 ** get_operand(operand, ra, rb, rc, combo=True))
        ip += 2

    out_str = ','.join(str(el) for el in out)
    print(out_str)
    
