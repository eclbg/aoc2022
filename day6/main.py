def part1():
    with open("input.txt") as f:
        seq = f.read(4)
        pos = 4
        if len(seq) == len(set(x for x in seq)):
            return pos
        pos += 1
        c = f.read(1)
        while c:
            seq = seq[1:] + c
            if len(seq) == len(set(x for x in seq)):
                return pos
            pos += 1
            c = f.read(1)


def part2():
    with open("input.txt") as f:
        seq = f.read(14)
        pos = 14
        if len(seq) == len(set(x for x in seq)):
            return pos
        pos += 1
        c = f.read(1)
        while c:
            seq = seq[1:] + c
            if len(seq) == len(set(x for x in seq)):
                return pos
            pos += 1
            c = f.read(1)


if __name__ == "__main__":
    print(part1())
    print(part2())
