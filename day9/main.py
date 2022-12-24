from typing import Tuple


class Knot:
    def __init__(self) -> None:
        self._position = (0, 0)

    def move(self, prev_knot_pos: Tuple[int, int]) -> Tuple[Tuple[int, int], bool]:
        xgap = prev_knot_pos[0] - self._position[0]
        ygap = prev_knot_pos[1] - self._position[1]
        # Means it's touching the previous knot. No movement.
        if abs(xgap) <= 1 and abs(ygap) <= 1:
            movement = (0, 0)
        # Need to move knot horizontally
        elif ygap == 0:
            assert xgap in (-2, 2)
            movement = ((xgap // abs(xgap)), 0)
        # Need to move knot vertically
        elif xgap == 0:
            assert ygap in (-2, 2)
            movement = (0, (ygap // abs(ygap)))
        # Need to move knot diagonally
        else:
            movement = ((xgap // abs(xgap)), (ygap // abs(ygap)))
        has_moved = any(movement)
        if has_moved:
            new_x = self._position[0] + movement[0]
            new_y = self._position[1] + movement[1]
            self._position = (new_x, new_y)
        return (self._position, has_moved)

    def get_pos(self) -> Tuple[int, int]:
        return self._position


class Rope:
    directions = {
        "R": (1, 0),
        "U": (0, 1),
        "L": (-1, 0),
        "D": (0, -1),
    }

    def __init__(self, num_knots) -> None:
        self._head_pos = (0, 0)
        self._knots = [Knot() for _ in range(num_knots - 1)]

    def move_head(self, direction: str) -> None:
        movement = self.directions[direction]
        new_x = self._head_pos[0] + movement[0]
        new_y = self._head_pos[1] + movement[1]
        self._head_pos = (new_x, new_y)
        self.move_knots()

    def move_knots(self) -> None:
        prev_knot_pos = self.get_head_pos()
        for knot in self._knots:
            prev_knot_pos, has_moved = knot.move(prev_knot_pos=prev_knot_pos)
            if has_moved is False:
                break

    def get_head_pos(self) -> Tuple[int, int]:
        return self._head_pos

    def get_tail_pos(self) -> Tuple[int, int]:
        return self._knots[-1]._position


def part1():
    rope = Rope(num_knots=2)
    tail_positions = set()
    with open("input.txt") as f:
        for row in f:
            row = row.strip()
            direction, howmany = row.split()
            for _ in range(int(howmany)):
                rope.move_head(direction)
                tail_positions.add(rope.get_tail_pos())
    return len(tail_positions)


def part2():
    rope = Rope(num_knots=10)
    tail_positions = set()
    with open("input.txt") as f:
        for row in f:
            row = row.strip()
            direction, howmany = row.split()
            for _ in range(int(howmany)):
                rope.move_head(direction)
                tail_positions.add(rope.get_tail_pos())
    return len(tail_positions)


if __name__ == "__main__":
    print(part1())
    print(part2())
