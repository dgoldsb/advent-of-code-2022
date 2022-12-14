"""Solve day 14."""
from aoc.helpers import time_it

MODS = [(0, 1), (-1, 1), (1, 1)]


class FreeFallError(RuntimeError):
    """Sand is in a free-fall."""


def drop_grain(topology: set[tuple[int, int]], max_depth, spawn: tuple[int, int]):
    if spawn[1] > max_depth:
        raise FreeFallError("Sand dropped over the edge!")
    for mod in MODS:
        if (candidate := (spawn[0] + mod[0], spawn[1] + mod[1])) not in topology:
            drop_grain(topology, max_depth, candidate)
    topology.add(spawn)


def _parse(input_) -> set[tuple[int, int]]:
    set_ = set()
    for line in input_.split("\n"):
        x_old, y_old = None, None
        for range_ in line.split(" -> "):
            x_new, y_new = range_.split(",")
            x_new = int(x_new)
            y_new = int(y_new)
            if x_old is not None:
                for x in range(min(x_old, x_new), max(x_old, x_new) + 1):
                    for y in range(min(y_old, y_new), max(y_old, y_new) + 1):
                        set_.add((x, y))
            x_old, y_old = x_new, y_new
    return set_


def solve(topology) -> int:
    start_len = len(topology)
    try:
        drop_grain(topology, max(loc[1] for loc in topology), (500, 0))
    except FreeFallError:
        pass
    return len(topology) - start_len


@time_it
def part_a(input_: str):
    return solve(_parse(input_))


@time_it
def part_b(input_: str):
    topology = _parse(input_)
    floor_y = max((l[1] for l in topology)) + 2
    for x in range(500 - floor_y * 2, 500 + floor_y * 2):
        topology.add((x, floor_y))
    return solve(topology)
