# https://adventofcode.com/2022/day/12

import math
import copy
from dataclasses import dataclass
from typing import Tuple, TextIO


class Cell:
    def __init__(self, height):
        self._height = height
        self._distance = None

    def set_distance(self, distance: int) -> None:
        self._distance = distance

    def get_distance(self) -> int:
        return self._distance

    def get_height(self) -> int:
        return self._height

    def __repr__(self):
        return f"<Cell: height={self._height}, distance={self._distance}"

    def __str__(self):
        return repr(self)


@dataclass
class HeightMap:
    _DIRECTIONS = {
        "U": (-1, 0),
        "D": (1, 0),
        "L": (0, -1),
        "R": (0, 1),
    }

    def __init__(self):
        self._grid = {}
        self._start_pos = None
        self._end_pos = None
        self._num_rows = 0

    def set_start_pos(self, start_pos: Tuple) -> None:
        self._start_pos = start_pos

    def set_end_pos(self, end_pos: Tuple) -> None:
        self._end_pos = end_pos

    def get_num_rows(self) -> int:
        return self._num_rows

    def add_row(self, row: list[Cell]) -> None:
        row_index = self.get_num_rows()
        for j, cell in enumerate(row):
            self._grid[(row_index, j)] = cell
        self._num_rows += 1

    def is_valid_destination(self, position: Tuple[int, int], from_height: int):
        dest_cell = self._get_cell(position)
        return dest_cell is not None and dest_cell.get_height() - 1 <= from_height

    def _get_valid_destinations(
        self, position: Tuple[int, int], from_height: int
    ) -> list(Tuple[int, int]):
        neighbor_positions = [
            (position[0] + movement[0], position[1] + movement[1])
            for movement in self._DIRECTIONS.values()
        ]
        valid_destinations = list(
            filter(
                lambda x: self.is_valid_destination(x, from_height), neighbor_positions
            )
        )
        return valid_destinations

    def _get_cell(self, position: Tuple[int, int]) -> Cell:
        return self._grid.get(position)

    def compute_shortest_path_length(self) -> int:
        start = self._get_cell(self._start_pos)
        start.set_distance(0)
        curr_step = 1
        valid_destinations = self._get_valid_destinations(
            self._start_pos, from_height=start.get_height()
        )
        to_eval_next = []
        for dest in valid_destinations:
            cell = self._get_cell(dest)
            cell.set_distance(curr_step)
            to_eval_next.append(dest)
        curr_step = 2
        while to_eval_next:
            to_eval_now = copy.deepcopy(to_eval_next)
            to_eval_next = []
            for pos in to_eval_now:
                valid_destinations = self._get_valid_destinations(
                    position=pos, from_height=self._get_cell(pos).get_height()
                )
                for dest in valid_destinations:
                    if dest == self._end_pos:
                        return curr_step
                    if self._get_cell(dest).get_distance() is not None:
                        continue
                    cell = self._get_cell(dest)
                    cell.set_distance(curr_step)
                    to_eval_next.append(dest)
            curr_step += 1

    def get_cells_of_height(self, height: int) -> list(Tuple[int, int]):
        return [
            x[0]
            for x in filter(lambda x: x[1].get_height() == height, self._grid.items())
        ]

    def reset_distances(self) -> None:
        for cell in self._grid.values():
            cell.set_distance(None)


def parse_input_file(f: TextIO) -> HeightMap:
    heightmap = HeightMap()
    for i, row in enumerate(f):
        row = row.strip()
        try:
            start_j = row.index("S")
            start_i = i
            heightmap.set_start_pos((start_i, start_j))
            row = row.replace("S", "a")
        except ValueError:
            pass
        try:
            end_j = row.index("E")
            end_i = i
            heightmap.set_end_pos((end_i, end_j))
            row = row.replace("E", "z")
        except ValueError:
            pass
        heights = [ord(x) - 97 for x in row]
        cells = [Cell(height) for height in heights]
        heightmap.add_row(cells)
    return heightmap


def part1():
    with open("input.txt") as f:
        heightmap = parse_input_file(f)
    shortest_path = heightmap.compute_shortest_path_length()
    return shortest_path


def part2():
    with open("input.txt") as f:
        heightmap = parse_input_file(f)
    shortest_overall = math.inf
    possible_starts = heightmap.get_cells_of_height(height=0)
    for start_pos in possible_starts:
        heightmap.reset_distances()
        heightmap.set_start_pos(start_pos)
        shortest_path = heightmap.compute_shortest_path_length()
        if shortest_path is None:
            # There is no possible path from this start
            continue
        shortest_overall = min(shortest_overall, shortest_path)
    return shortest_overall


if __name__ == "__main__":
    print(part1())
    print(part2())
