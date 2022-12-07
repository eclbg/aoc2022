import abc
from typing import Optional


LIST = "ls"
CHANGE_DIR = "cd"

FILE = "file"
DIR = "dir"

INDENTATION = 4


class FSItem(abc.ABC):
    @abc.abstractmethod
    def get_size(self):
        ...

    @abc.abstractmethod
    def draw(self):
        ...

    @abc.abstractmethod
    def contribute_to_part1(self):
        ...

    @abc.abstractmethod
    def contribute_to_part2(self, space_needed):
        ...


class Dir(FSItem):
    def __init__(
        self, name: str, parent: Optional[FSItem] = None, level: Optional[int] = None
    ):
        self.name = name
        self.parent = parent
        self.contents: dict[str, FSItem] = {}
        self._size = None
        self.level = level if level is not None else parent.level + 1

    def get_size(self):
        if self._size is None:
            size = 0
            for item in self.contents.values():
                size += item.get_size()
            self._size = size
        return self._size

    def add_to_contents(self, item: FSItem):
        self.contents[item.name] = item

    def draw(self):
        result = (
            " " * self.level * INDENTATION
            + f"- {self.name} (dir, size={self.get_size()})\n"
        )
        for item in self.contents.values():
            result += item.draw()
        return result

    def contribute_to_part1(self):
        result = 0
        if self.get_size() < 100_000:
            result += self.get_size()
        for item in self.contents.values():
            result += item.contribute_to_part1()
        return result

    def contribute_to_part2(self, curr_result, space_needed):
        size = self.get_size()
        if size > space_needed:
            if curr_result == 0:
                curr_result = size
            else:
                curr_result = min(curr_result, size)
            for item in self.contents.values():
                curr_result = item.contribute_to_part2(curr_result, space_needed)
        return curr_result


class File(FSItem):
    def __init__(self, name: str, parent: Optional[Dir], size: int):
        self.name = name
        self.parent = parent
        self._size = size

    def get_size(self):
        return self._size

    def draw(self):
        return (
            " " * (self.parent.level + 1) * INDENTATION
            + f"- {self.name} (file, size={self._size})\n"
        )

    def contribute_to_part1(self):
        return 0

    def contribute_to_part2(self, curr_result, space_needed):
        return curr_result


class FileSystem:
    def __init__(self):
        self.root_dir = Dir(name="/", level=0)

    def draw(self):
        return self.root_dir.draw()

    def get_total_size(self):
        return self.root_dir.get_size()

    def compute_part1_answer(self):
        return self.root_dir.contribute_to_part1()

    def compute_part2_answer(self):
        curr_result = 0
        space_needed = self.root_dir.get_size() - 40_000_000
        return self.root_dir.contribute_to_part2(curr_result, space_needed)


def parse_action(row):
    assert row.startswith("$")
    command = row[2:4]
    if command == "ls":
        action = LIST
        dest = "."  # Current directory
    elif command == "cd":
        action = CHANGE_DIR
        dest = row[5:]
    return (action, dest)


def change_dir(cwd: FSItem, dest: str):
    if dest == "..":
        cwd = cwd.parent
    else:
        cwd = cwd.contents[dest]
    return cwd


def parse_item_info(row):
    size_or_dir, name = row.split()
    if size_or_dir == "dir":
        item_type = DIR
        size = None
    else:
        item_type = FILE
        size = int(size_or_dir)
    return item_type, name, size


def init_fs():
    filesystem = FileSystem()
    root_dir = filesystem.root_dir
    cwd = root_dir
    with open("input.txt") as f:
        next(f)  # Skip first command 'cd /'
        try:
            row = next(f).strip()
            while row:
                if row.startswith("$"):
                    action, dest = parse_action(row)
                    if action == CHANGE_DIR:
                        cwd = change_dir(cwd, dest)
                        row = next(f).strip()
                    elif action == LIST:
                        row = next(f).strip()
                        while not row.startswith("$"):
                            item_type, name, size = parse_item_info(row)
                            # TODO: FSItemFactory
                            if item_type == FILE:
                                item = File(name=name, parent=cwd, size=size)
                            elif item_type == DIR:
                                item = Dir(name=name, parent=cwd)
                            cwd.add_to_contents(item)
                            row = next(f).strip()
        except StopIteration:
            pass
    return filesystem


if __name__ == "__main__":
    filesystem = init_fs()
    print(filesystem.draw())
    print(filesystem.compute_part1_answer())
    print(filesystem.compute_part2_answer())
