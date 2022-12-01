def part1():
    with open('input.txt') as f:
        elf_cals = []
        curr_elf_cals = 0
        for row in map(lambda x: x.strip('\n'), f.readlines()):
            if row:
                curr_elf_cals += int(row)
            else:
                elf_cals.append(curr_elf_cals)
                curr_elf_cals = 0
        return max(elf_cals)


def part2():
    with open('input.txt') as f:
        elf_cals = []
        curr_elf_cals = 0
        for row in map(lambda x: x.strip('\n'), f.readlines()):
            if row:
                curr_elf_cals += int(row)
            else:
                elf_cals.append(curr_elf_cals)
                curr_elf_cals = 0
        return sum(sorted(elf_cals, reverse=True)[:3])


if __name__ == "__main__":
    print(part1())
    print(part2())
