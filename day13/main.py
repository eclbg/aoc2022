import ast
from typing import Optional


def grouper(iterable, n):
    return zip(*[iter(iterable)] * n)


def items_in_right_order(left, right) -> Optional[bool]:
    """True if left < right else False according to the puzzle criteria"""
    right_order = None
    try:
        if left < right:
            right_order = True
        if left > right:
            right_order = False
        return right_order
    except TypeError:
        if type(left) == int:
            left = [left]
            return items_in_right_order(left, right)
        if type(right) == int:
            right = [right]
            return items_in_right_order(left, right)
        return is_right_order(left, right)


def is_right_order(left, right):
    # print("\n".join([str(x) for x in left]))
    # print()
    # print("\n".join([str(x) for x in right]))
    # print()
    # print()
    right_order = None
    left_consumed = False
    right_consumed = False
    try:
        next_left = next(iter(left))
        try:
            remaining_left = left[1:]
        except IndexError:
            remaining_left = []
    except StopIteration:
        left_consumed = True
    except TypeError:
        next_left = left
    try:
        next_right = next(iter(right))
        try:
            remaining_right = right[1:]
        except IndexError:
            remaining_right = []
    except StopIteration:
        right_consumed = True
    except TypeError:
        next_right = right
    if left_consumed and not right_consumed:
        return True
    if not left_consumed and right_consumed:
        return False
    right_order = items_in_right_order(next_left, next_right)
    if right_order is not None:
        return right_order
    else:
        return is_right_order(remaining_left, remaining_right)


class Packet:
    def __init__(self, data):
        self._data = data


def part1():
    result = 0
    with open("test_input.txt") as f:
        for i, (left, right, _) in enumerate(grouper(f, 3)):
            left = ast.literal_eval(left)
            right = ast.literal_eval(right)
            right_order = is_right_order(left, right)
            # print(
            #     str(right_order) + " vs " + str(bool(_.strip())) + " " + str(3 * i + 1)
            # )
            if right_order is True:
                result += i + 1
    return result


def part2():
    ...


if __name__ == "__main__":
    print(part1())
    # print(part2())
