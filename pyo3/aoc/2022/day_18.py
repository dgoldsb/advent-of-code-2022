"""Solve day 18."""
from collections import deque
from typing import Generator

from aoc.helpers import time_it

MODS = (
    (1, 0, 0),
    (-1, 0, 0),
    (0, 1, 0),
    (0, -1, 0),
    (0, 0, 1),
    (0, 0, -1),
)


def _parse(input_: str):
    for line in input_.split("\n"):
        x, y, z = line.split(",")
        yield int(x), int(y), int(z)


def _count_surface(set_: set[tuple[int, int, int]]) -> Generator[bool, None, None]:
    for drop in set_:
        for mod in MODS:
            yield (drop[0] + mod[0], drop[1] + mod[1], drop[2] + mod[2]) not in set_


@time_it
def part_a(input_: str):
    return sum(_count_surface(set(_parse(input_))))


def _flood(water, all_lava):
    queue = deque([water])
    all_water = {water}

    while queue:
        water = queue.popleft()

        for mod in MODS:
            new = (water[0] + mod[0], water[1] + mod[1], water[2] + mod[2])
            if (
                new not in all_lava
                and new not in all_water
                and 0 <= new[0] < 30
                and 0 <= new[1] < 30
                and 0 <= new[2] < 30
            ):
                queue.append(new)
                all_water.add(new)
    return all_water


@time_it
def part_b(input_: str):
    water = (0, 0, 0)
    all_lava = set(_parse(input_))
    all_water = _flood(water, all_lava)
    all_air = {
        (x, y, z)
        for x in range(30)
        for y in range(30)
        for z in range(30)
        if (x, y, z) not in all_water and (x, y, z) not in all_lava
    }
    return sum(_count_surface(all_lava.union(all_air)))
