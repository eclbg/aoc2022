from typing import Tuple

RIGHT = "R"
UP = "U"
LEFT = "L"
DOWN = "D"

DIRECTIONS = {
    RIGHT: (1, 0),
    UP: (0, 1),
    LEFT: (-1, 0),
    DOWN: (0, -1),
}


class Knot:
    def __init__(self):
        self._position = (0, 0)

    def move(self, prev_knot_pos) -> Tuple[Tuple[int, int], bool]:
        xgap = prev_knot_pos[0] - self._position[0]
        ygap = prev_knot_pos[1] - self._position[1]
        # Means it's touching the previous know. No movement.
        if abs(xgap) <= 1 and abs(ygap) <= 1:
            movement = (0, 0)
        # Need to move tail horizontally
        elif ygap == 0:
            assert xgap in (-2, 2)
            movement = ((xgap // abs(xgap)), 0)
        # Need to move tail vertically
        elif xgap == 0:
            assert ygap in (-2, 2)
            movement = (0, (ygap // abs(ygap)))
        # Need to move diagonally
        else:
            movement = ((xgap // abs(xgap)), (ygap // abs(ygap)))
        has_moved = any(movement)
        if has_moved:
            new_x = self._position[0] + movement[0]
            new_y = self._position[1] + movement[1]
            self._position = (new_x, new_y)
        return (self._position, has_moved)

    def get_pos(self):
        return self._position


class Rope:
    directions = DIRECTIONS

    def __init__(self):
        self._position = {
            "head": [0, 0],
            "tail": [0, 0],
        }

    def move_tail(self):
        xgap = self._position["head"][0] - self._position["tail"][0]
        ygap = self._position["head"][1] - self._position["tail"][1]
        # Means head and tail are touching. Tail doesn't move.
        if abs(xgap) <= 1 and abs(ygap) <= 1:
            return
        # Need to move tail horizontally
        elif ygap == 0:
            assert xgap in (-2, 2)
            movement = ((xgap // abs(xgap)), 0)
        # Need to move tail vertically
        elif xgap == 0:
            assert ygap in (-2, 2)
            movement = (0, (ygap // abs(ygap)))
        # Need to move diagonally
        else:
            movement = ((xgap // abs(xgap)), (ygap // abs(ygap)))
        self._position["tail"][0] = self._position["tail"][0] + movement[0]
        self._position["tail"][1] = self._position["tail"][1] + movement[1]

    def move_head(self, direction: str):
        movement = self.directions[direction]
        self._position["head"][0] = self._position["head"][0] + movement[0]
        self._position["head"][1] = self._position["head"][1] + movement[1]
        self.move_tail()

    def get_tail_pos(self) -> Tuple:
        return tuple(self._position["tail"])


class Rope2:
    directions = DIRECTIONS

    def __init__(self, num_knots):
        self._head_pos = (0, 0)
        self._knots = [Knot() for _ in range(num_knots - 1)]

    def move_head(self, direction: str):
        movement = self.directions[direction]
        new_x = self._head_pos[0] + movement[0]
        new_y = self._head_pos[1] + movement[1]
        self._head_pos = (new_x, new_y)
        self.move_knots()

    def move_knots(self):
        prev_knot_pos = self.get_head_pos()
        for knot in self._knots:
            prev_knot_pos, has_moved = knot.move(prev_knot_pos=prev_knot_pos)
            if has_moved is False:
                break

    def get_head_pos(self):
        return self._head_pos

    def get_tail_pos(self):
        return self._knots[-1]._position


def part1():
    rope = Rope()
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
    rope = Rope2(num_knots=10)
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
