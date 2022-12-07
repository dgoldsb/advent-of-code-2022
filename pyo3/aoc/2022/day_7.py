"""Solve day 7."""
from dataclasses import dataclass
from functools import lru_cache
from typing import Union

from aoc.helpers import time_it


@dataclass
class File:
    name: str
    size: int


@dataclass
class Dir:
    name: str
    parent: "Dir"
    contents: dict[str, Union[File, "Dir"]]

    def __hash__(self):
        """Hash for use in the LRU cache, invalidate when contents change."""
        return hash((self.name, self.parent, len(self.contents)))

    @property
    @lru_cache
    def size(self):
        return sum([c.size for c in self.contents.values()])


@lru_cache
def _run(input_: str):
    root = Dir("/", None, {})  # type: ignore
    cd = root
    all_directories = [root]
    for command in input_.split("\n"):
        match command.split(" "):
            case ["$", "cd", ".."]:
                cd = cd.parent
            case ["$", "cd", "/"]:
                cd = root
            case ["$", "cd", dir_name]:
                cd = cd.contents[dir_name]
            case ["$", "ls"]:
                pass
            case ["dir", name]:
                cd.contents[name] = Dir(name, cd, {})
                all_directories.append(cd.contents[name])
            case [size, name]:
                cd.contents[name] = File(name, int(size))
            case _:
                raise RuntimeError("Unexpected operation")
    return root, all_directories


@time_it
def part_a(input_: str):
    _, all_directories = _run(input_)
    return sum(d.size for d in all_directories if d.size < 100000)


@time_it
def part_b(input_: str):
    root, all_directories = _run(input_)
    required_extra_space = root.size - (70000000 - 30000000)
    sorted_directories = sorted(all_directories, key=lambda d: d.size)
    for dir in sorted_directories:
        if dir.size > required_extra_space:
            return dir.size
