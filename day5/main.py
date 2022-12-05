from itertools import zip_longest
from functools import reduce
import re

INSTRUCTIONS_RE = re.compile(r"\d+")


def str_grouper_filler(iterable, n):
    args = [iter(iterable)] * n
    for group in zip_longest(*args, fillvalue=" "):
        yield reduce(lambda x, y: x + y, group)


def parse_row_items(row):
    parsed_items = []
    for i, crate in enumerate(str_grouper_filler(row, 4)):
        parsed_items.append(crate[1] if crate.strip() else None)
    return parsed_items


def parse_row_instruction(row):
    parsed = re.findall(pattern=INSTRUCTIONS_RE, string=row)
    return map(int, parsed)


def part1():
    with open("input.txt") as f:
        stacks = [[]]
        row = next(f).strip("\n")
        while not row.startswith(" 1"):
            parsed_items = parse_row_items(row.strip("\n"))
            no_stacks = len(stacks)
            if no_stacks < len(parsed_items):
                for i in range(len(parsed_items) - no_stacks):
                    stacks.append([])
            for i, item in enumerate(parsed_items):
                if item:
                    stacks[i].insert(0, item)
            row = next(f)
        next(f)  # skip empty row
        for row in f:
            (howmany, stack_from, stack_to) = parse_row_instruction(row.strip("\n"))
            stacks[stack_to - 1].extend(
                [stacks[stack_from - 1].pop() for x in range(howmany)]
            )
    return reduce(lambda x, y: x + y, [stack[-1] for stack in stacks])


def part2():
    with open("input.txt") as f:
        stacks = [[]]
        row = next(f).strip("\n")
        while not row.startswith(" 1"):
            parsed_items = parse_row_items(row.strip("\n"))
            no_stacks = len(stacks)
            if no_stacks < len(parsed_items):
                for i in range(len(parsed_items) - no_stacks):
                    stacks.append([])
            for i, item in enumerate(parsed_items):
                if item:
                    stacks[i].insert(0, item)
            row = next(f)
        next(f)  # skip empty row
        for row in f:
            (howmany, stack_from, stack_to) = parse_row_instruction(row.strip("\n"))
            stacks[stack_to - 1].extend(stacks[stack_from - 1][-howmany:])
            [stacks[stack_from - 1].pop() for x in range(howmany)]
    return reduce(lambda x, y: x + y, [stack[-1] for stack in stacks])


if __name__ == "__main__":
    print(part1())
    print(part2())
