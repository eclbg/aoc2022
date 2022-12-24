from typing import Tuple

DIRECTIONS = {
    "R": (1, 0),
    "U": (0, 1),
    "L": (-1, 0),
    "D": (0, -1),
}


class Rope:
    directions = {
        "R": (1, 0),
        "U": (0, 1),
        "L": (-1, 0),
        "D": (0, -1),
    }

    def __init__(self) -> None:
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
