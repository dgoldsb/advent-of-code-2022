"""Solve day 14."""
from aoc.helpers import time_it

MODS = [(0, 1), (-1, 1), (1, 1)]


class FreeFallError(RuntimeError):
    """Sand is in a free-fall."""


class FullOfSandError(RuntimeError):
    """The sand spawn position is taken!"""


def drop_grain(topology: set[tuple[int, int]], spawn: tuple[int, int] = (500, 0)):
    lowest_y = max((l[1] for l in topology))
    if spawn in topology:
        raise FullOfSandError("Sand everywhere!")
    location = spawn
    while True:
        if location[1] > lowest_y:
            raise FreeFallError("Grain of sand fell past the topology!")

        for mod in MODS:
            location_candidate = (location[0] + mod[0], location[1] + mod[1])
            if location_candidate not in topology:
                location = location_candidate
                break
        else:
            topology.add(location)
            return


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
    counter = 0
    while True:
        try:
            drop_grain(topology)
            counter += 1
        except (FreeFallError, FullOfSandError):
            break
    return counter


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
