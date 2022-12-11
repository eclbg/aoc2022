from __future__ import annotations
import copy
from typing import Callable, Tuple
from dataclasses import dataclass
import re
import operator
from math import floor


OPERATIONS = {"+": operator.add, "*": operator.mul}


@dataclass
class Item:
    worry_level: int


class MonkeyGame:
    def __init__(self, monkeys: list[Monkey]):
        self._monkeys = copy.deepcopy(monkeys)
        for monkey in self._monkeys:
            monkey.register_to_game(self)

    def run_round(self) -> None:
        for monkey in self.iter_monkeys():
            monkey.play_turn()

    def get_monkey(self, index: int) -> Monkey:
        return self._monkeys[index]

    def iter_monkeys(self):
        return iter(self._monkeys)

    def compute_monkey_business_level(self):
        most_items_inspected = sorted(
            (x.get_no_items_inspected() for x in self._monkeys), reverse=True
        )[:2]
        return operator.mul(*most_items_inspected)


class Monkey:
    def __init__(
        self,
        starting_items: list[Item],
        operation_func,
        test_func,
        receiver_if_true: int,
        receiver_if_false: int,
    ):
        self._items = starting_items
        self._operation_func = operation_func
        self._test_func = test_func
        self._receiver_if_true_index = receiver_if_true
        self._receiver_if_false_index = receiver_if_false
        self._items_inspected_count = 0
        self._game = None

    def register_to_game(self, game: MonkeyGame) -> None:
        self._game = game

    def inspect_item(self, item: Item) -> None:
        worry_level = self._operation_func(item.worry_level)
        # worry_level = floor(worry_level / 3)
        item.worry_level = worry_level
        self._items_inspected_count += 1

    def get_receiving_monkey(self, item) -> Monkey:
        if self._test_func(item.worry_level):
            return self._game.get_monkey(self._receiver_if_true_index)
        return self._game.get_monkey(self._receiver_if_false_index)

    def play_turn(self) -> None:
        for item in self._items:
            self.inspect_item(item)
            receiver = self.get_receiving_monkey(item)
            receiver.receive_item(item)
        self._items = []

    def receive_item(self, item) -> None:
        self._items.append(item)

    def get_no_items_inspected(self) -> int:
        return self._items_inspected_count


class InputParser:
    @staticmethod
    def parse_starting_items(starting_items_row: str) -> list[Item]:
        items_worry_level = re.findall(r"\d+", starting_items_row)
        items = [Item(worry_level=int(x)) for x in items_worry_level]
        return items

    def parse_operation(operation_row: str) -> Callable:
        _operator, right_operand = operation_row.split()[-2:]
        operation_func = OPERATIONS[_operator]
        if right_operand == "old":

            def _func(x):
                return operation_func(x, x)

        else:

            def _func(x):
                return operation_func(x, int(right_operand))

        return _func

    def parse_test(test_row: str) -> Callable:
        denominator = int(re.findall(r"\d+", test_row)[0])

        def _test_func(x):
            return (x % denominator) == 0

        return _test_func

    def parse_receivers(receivers_rows: list[str]) -> Tuple(int, int):
        receivers = tuple(int(re.findall(r"\d+", x)[0]) for x in receivers_rows)
        return receivers

    @classmethod
    def parse_input(cls, input_text: str) -> list[Monkey]:
        monkeys = []
        raw_monkeys_data = input_text.split("\n\n")
        for raw_monkey_data in raw_monkeys_data:
            rows = raw_monkey_data.split("\n")
            starting_items = cls.parse_starting_items(rows[1])
            operation_func = cls.parse_operation(rows[2])
            test_func = cls.parse_test(rows[3])
            receivers = cls.parse_receivers(rows[4:6])
            monkey = Monkey(
                starting_items=starting_items,
                operation_func=operation_func,
                test_func=test_func,
                receiver_if_true=receivers[0],
                receiver_if_false=receivers[1],
            )
            monkeys.append(monkey)
        return monkeys


def part1():
    parser = InputParser
    with open("input.txt") as f:
        monkeys = parser.parse_input(f.read())
    game = MonkeyGame(monkeys)
    for monkey in game.iter_monkeys():
        print(monkey.__dict__)
    for _ in range(20):
        game.run_round()
    return game.compute_monkey_business_level()


def part2():
    parser = InputParser
    with open("test_input.txt") as f:
        monkeys = parser.parse_input(f.read())
    game = MonkeyGame(monkeys)
    for monkey in game.iter_monkeys():
        print(monkey.__dict__)
    for _ in range(1000):
        game.run_round()
    return game.compute_monkey_business_level()


if __name__ == "__main__":
    print(part1())
    print(part2())
