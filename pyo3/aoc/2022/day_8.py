"""Solve day 8."""
from aoc.helpers import time_it


def _find_row_length(trees: str) -> int:
    return trees.find("\n") + 1


def _find_border(trees: str) -> set[int]:
    row_length = _find_row_length(trees)
    grid_size = row_length * (row_length - 1)
    return set(
        list(range(0, row_length - 1))
        + list(range(grid_size - row_length, grid_size - 1))
        + list(range(0, grid_size, row_length))
        + list(range(row_length - 2, grid_size, row_length))
    )


def _count_visible_trees(start: int, offset: int, trees: str, visible: set[int]):
    highest = -1
    new_idx = start
    while True:
        if (new_tree := int(trees[new_idx])) > highest:
            visible.add(new_idx)
            highest = new_tree
        new_idx = new_idx + offset
        if new_idx < 0 or new_idx >= len(trees) or trees[new_idx] == "\n":
            break


def _score_row(start: int, offset: int, trees: str):
    upper = int(trees[start])
    new_idx = start
    count = 0
    while True:
        new_idx = new_idx + offset

        if new_idx < 0 or new_idx >= len(trees) or trees[new_idx] == "\n":
            break

        count += 1
        if int(trees[new_idx]) >= upper:
            break
    return count


def _score(start: int, trees: str):
    result = 1
    for offset in (1, -1, _find_row_length(trees), -_find_row_length(trees)):
        result *= _score_row(start, offset, trees)
    return result


@time_it
def part_a(input_: str):
    visible_trees = set()
    for offset in (1, -1, _find_row_length(input_), -_find_row_length(input_)):
        for border_tree in _find_border(input_):
            _count_visible_trees(border_tree, offset, input_, visible_trees)
    return len(visible_trees)


@time_it
def part_b(input_: str):
    return max((_score(t, input_) for t in range(len(input_)) if input_[t] != "\n"))
