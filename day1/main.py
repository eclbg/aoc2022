def part1():
    with open("input.txt") as f:
        curr_elf_cals = most_cals = 0
        for row in map(lambda x: x.strip(), f):
            if not row:
                most_cals = max(most_cals, curr_elf_cals)
                curr_elf_cals = 0
            else:
                curr_elf_cals += int(row)
        most_cals = max(most_cals, curr_elf_cals)
    return most_cals


def part2():
    with open("input.txt") as f:
        top_3_elves_cals = [0, 0, 0]
        curr_elf_cals = 0
        for row in map(lambda x: x.strip(), f):
            if not row:
                top_3_elves_cals = sorted(
                    top_3_elves_cals + [curr_elf_cals],
                    reverse=True
                )[:3]
                curr_elf_cals = 0
            else:
                curr_elf_cals += int(row)
        top_3_elves_cals = sorted(
            top_3_elves_cals + [curr_elf_cals],
            reverse=True
        )[:3]
        return sum(top_3_elves_cals)


if __name__ == "__main__":
    print(part1())
    print(part2())
