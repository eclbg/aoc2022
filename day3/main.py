def grouper(iterable, n):
    "Collect data into non-overlapping fixed-length chunks or blocks"
    args = [iter(iterable)] * n
    return zip(*args)


def intersection(set1, *args):
    return set1.intersection(*args)


def compute_priority(item):
    if item.isupper():
        offset = 38
    else:
        offset = 96
    return ord(item) - offset


def part1():
    with open("input.txt") as f:
        total_priority = 0
        for row in f:
            row = row.strip()
            no_items = len(row)
            first_compartment_items = set(row[: no_items // 2])
            for item in row[no_items // 2 :]:
                if item in first_compartment_items:
                    misplaced_item = item
                    total_priority += compute_priority(misplaced_item)
                    break
    return total_priority


def part2():
    with open("input.txt") as f:
        total_priority = 0
        for group in grouper(f, 3):
            badge = intersection(*[set(x.strip()) for x in group]).pop()
            total_priority += compute_priority(badge)
    return total_priority


if __name__ == "__main__":
    print(part1())
    print(part2())
