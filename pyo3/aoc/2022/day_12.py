"""Solve day 12."""
from collections import defaultdict

from aoc.helpers import time_it

from aoc_py03 import dijkstra


def _parse_input(
    input_: str, is_b: bool
) -> tuple[int, int, dict[int, list[tuple[int, int]]]]:
    # The index in the input string is the "node identifier".
    line_length = input_.find("\n") + 1
    start = input_.find("S") if not is_b else len(input_) + 2
    goal = input_.find("E")

    # Cheeky hack: replace `S` and `E` with characters with the desired `ord`.
    input_ = input_.replace("S", "`").replace("E", "{")
    successors = defaultdict(list)

    offsets = (1, -1, line_length, -line_length)
    for idx, char in enumerate(input_):
        if char == "\n":
            continue
        for offset in offsets:
            other_idx = idx + offset
            if other_idx < 0 or other_idx >= len(input_) or input_[other_idx] == "\n":
                continue

            if is_b:
                linked = ord(char) - ord(input_[other_idx]) < 2
            else:
                linked = ord(input_[other_idx]) - ord(char) < 2
            if linked:
                # Another cheeky hack: for part B we replace "a" with a index out of
                # our bounds.
                if input_[idx] == "a" and is_b:
                    from_idx = start
                else:
                    from_idx = idx

                if input_[other_idx] == "a" and is_b:
                    to_idx = start
                else:
                    to_idx = other_idx
                successors[from_idx].append((1, to_idx))
    return start, goal, successors


@time_it
def part_a(input_: str):
    return len(dijkstra(*_parse_input(input_, False))[1:])


@time_it
def part_b(input_: str):
    goal, start, successors = _parse_input(input_, True)
    return len(dijkstra(start, goal, successors)[1:])
