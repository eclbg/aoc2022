from functools import reduce

DIRECTIONS = {
    "up": (-1, 0),
    "left": (0, -1),
    "down": (1, 0),
    "right": (0, 1),
}


class Grid:
    def __init__(self):
        self._grid = []
        self._num_rows = None
        self._num_cols = None

    def add_row(self, row: list[int]):
        self._grid.append([{"height": x, "is_visible": None} for x in row])

    @property
    def num_rows(self):
        if self._num_rows is None:
            num_rows = len(self._grid)
            self._num_rows = num_rows
        return self._num_rows

    @property
    def num_cols(self):
        if self._num_cols is None:
            num_cols = len(self._grid[0])
            self._num_cols = num_cols
        return self._num_cols

    def get_nth_row(self, n, reverse=False):
        row = self._grid[n]
        if reverse:
            row.reverse()
            # return reversed(row)
        return row

    def get_nth_col(self, n, reverse=False):
        col = [row[n] for row in self._grid]
        if reverse:
            col.reverse()
            # return reversed(col)
        return col

    def get_tree_from_coords(self, x, y):
        if x < 0 or y < 0:
            raise IndexError
        return self._grid[x][y]

    @property
    def visible_count(self):
        total_visible = 0
        for row in self._grid:
            total_visible += len(list(filter(lambda x: x["is_visible"], row)))
        return total_visible

    def __iter__(self):
        for row in self._grid:
            yield row

    def draw(self):
        result = ""
        for row in self._grid:
            result += " ".join([str(tree["height"]) for tree in row]) + "\n"
        return result


def part1():
    grid = Grid()
    with open("input.txt") as f:
        for row in f:
            row = row.strip()
            heights = [int(x) for x in row]
            grid.add_row(heights)
    # From the left
    for i in range(grid.num_rows):
        strip = grid.get_nth_row(i)
        tallest = strip[0]
        tallest["is_visible"] = True
        for tree in strip[1:]:
            if tree["height"] > tallest["height"]:
                tallest = tree
                tree["is_visible"] = True

    # From the top
    for i in range(grid.num_cols):
        strip = grid.get_nth_col(i)
        tallest = strip[0]
        tallest["is_visible"] = True
        for tree in strip[1:]:
            if tree["height"] > tallest["height"]:
                tallest = tree
                tree["is_visible"] = True

    # From the right
    for i in range(grid.num_rows):
        strip = grid.get_nth_row(i, reverse=True)
        tallest = strip[0]
        tallest["is_visible"] = True
        for tree in strip[1:]:
            if tree["height"] > tallest["height"]:
                tallest = tree
                tree["is_visible"] = True

    # From the bottom
    for i in range(grid.num_cols):
        strip = grid.get_nth_col(i, reverse=True)
        tallest = strip[0]
        tallest["is_visible"] = True
        for tree in strip[1:]:
            if tree["height"] > tallest["height"]:
                tallest = tree
                tree["is_visible"] = True
    return grid.visible_count


def compute_scenic_score(grid: Grid, tree_height: int, x: int, y: int) -> int:
    # If tree is at the edge, scenic_score = 0
    if x in (0, grid.num_rows) or y in (0, grid.num_cols):
        return 0
    trees_visible = {}
    for name, direction in DIRECTIONS.items():
        trees_visible[name] = 0
        i = 1
        while True:
            try:
                next_tree = grid.get_tree_from_coords(
                    x + i * direction[0], y + i * direction[1]
                )
                trees_visible[name] += 1
                if next_tree["height"] < tree_height:
                    i += 1
                elif next_tree["height"] >= tree_height:
                    break
            except IndexError:
                break
        # If no trees are visible in one direction we can stop calculating
        if trees_visible[name] == 0:
            return 0
    return reduce(lambda x, y: x * y, trees_visible.values())


def part2():
    grid = Grid()
    with open("input.txt") as f:
        for row in f:
            row = row.strip()
            heights = [int(x) for x in row]
            grid.add_row(heights)
    best_scenic_score = 0
    for x, row in enumerate(grid):
        for y, tree in enumerate(row):
            scenic_score = compute_scenic_score(grid, tree["height"], x, y)
            tree["scenic_score"] = scenic_score
            best_scenic_score = max(best_scenic_score, scenic_score)
    return best_scenic_score


if __name__ == "__main__":
    print(part1())
    print(part2())
