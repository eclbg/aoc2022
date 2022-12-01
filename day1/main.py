def aggregate_elves_calories(filename):
    with open("input.txt") as f:
        elf_cals = []
        curr_elf_cals = 0
        for row in map(lambda x: x.strip('\n'), f.readlines()):
            if row:
                curr_elf_cals += int(row)
            else:
                elf_cals.append(curr_elf_cals)
                curr_elf_cals = 0
    return elf_cals


def part1(elves_calories):
    return max(elves_calories)


def part2(elves_calories):
    return sum(sorted(elves_calories, reverse=True)[:3])


if __name__ == "__main__":
    filename = "input.txt"
    elves_calories = aggregate_elves_calories(filename)
    print(part1(elves_calories))
    print(part2(elves_calories))
