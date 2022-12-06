def part1():
    with open("input.txt") as f:
        count = 0  # count pairs where one assignment fully contains the other
        for row in f:
            # import pdb; pdb.set_trace()  # fmt: skip
            row = row.strip()
            ((start1, end1), (start2, end2)) = tuple(
                map(lambda x: int(x), x.split("-")) for x in row.split(",")
            )

            if start1 == start2:
                count += 1
            elif start1 > start2 and end1 <= end2:
                count += 1
            elif start1 < start2 and end2 <= end1:
                count += 1
        return count


def part2():
    with open("input.txt") as f:
        count = 0  # count pairs where one assignment fully contains the other
        for row in f:
            # import pdb; pdb.set_trace()  # fmt: skip
            row = row.strip()
            ((start1, end1), (start2, end2)) = tuple(
                map(lambda x: int(x), x.split("-")) for x in row.split(",")
            )
            if start1 <= end2 and end1 >= start2:
                count += 1
        return count


if __name__ == "__main__":
    print(part1())
    print(part2())
