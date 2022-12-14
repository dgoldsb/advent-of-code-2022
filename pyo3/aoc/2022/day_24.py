"""Solve day 24.

Notes:
 - Shifting terrain invalidates Dijkstra assumptions.
 - Lot of blizzards, so branches will be limited.
 - Standing still is an option.
 - Cartesian distance as heuristic, then aggressive pruning once we find a path.
"""
import heapq
import sys
from dataclasses import dataclass
from enum import Enum
from functools import lru_cache
from typing import NewType, Generator

from aoc.helpers import time_it

Coordinate = NewType("Coordinate", tuple[int, int])
MODS = [(0, 1), (0, -1), (1, 0), (-1, 0), (0, 0)]


class Direction(Enum):
    NORTH = "N"
    SOUTH = "S"
    WEST = "W"
    EAST = "E"


Blizzard = NewType("Blizzard", tuple[Direction, Coordinate])


class Valley:
    def __init__(self, start, end, blizzards, walls):
        self.start: Coordinate = start
        self.end: Coordinate = end
        self.blizzards: list[Blizzard] = blizzards
        self.walls: set[Coordinate] = walls

    def _evolve_blizzard(self, blizzard: Blizzard):
        direction, loc = blizzard
        match direction:
            case Direction.NORTH:
                candidate = (loc[0], loc[1] + 1)
                if candidate in self.walls:
                    # Compensate for my earlier hack.
                    candidate = (loc[0], min(w[1] for w in self.walls) + 2)
            case Direction.SOUTH:
                candidate = (loc[0], loc[1] - 1)
                if candidate in self.walls:
                    # Compensate for my earlier hack.
                    candidate = (loc[0], max(w[1] for w in self.walls) - 2)
            case Direction.EAST:
                candidate = (loc[0] + 1, loc[1])
                if candidate in self.walls:
                    candidate = (min(w[0] for w in self.walls) + 1, loc[1])
            case Direction.WEST:
                candidate = (loc[0] - 1, loc[1])
                if candidate in self.walls:
                    candidate = (max(w[0] for w in self.walls) - 1, loc[1])
            case _:
                raise RuntimeError(f"Sir this is a Wendy's: {blizzard}")
        return candidate

    @lru_cache
    def _get_state(self, time: int) -> "Valley":
        if time == 0:
            return self
        start_state = self._get_state(time - 1)
        new_blizzards = [
            (b[0], self._evolve_blizzard(b)) for b in start_state.blizzards
        ]
        return type(self)(self.start, self.end, new_blizzards, self.walls)

    @lru_cache
    def _get_terrain(self, time: int) -> set[Coordinate]:
        state = self._get_state(time)
        set_ = set()
        for wall in state.walls:
            set_.add(wall)
        for blizzard in state.blizzards:
            set_.add(blizzard[1])
        return set_

    def branch(self, time: int, loc: Coordinate) -> Generator[Coordinate, None, None]:
        terrain = self._get_terrain(time)
        for mod in MODS:
            candidate = (loc[0] + mod[0], loc[1] + mod[1])
            if candidate not in terrain:
                yield candidate


def _parse_valley(input_: str) -> Valley:
    walls = set()
    blizzards = []

    # To disallow sneaking around.
    input_ = "#" * 122 + "\n" + input_ + "\n" + "#" * 122

    lines = input_.splitlines()

    first_line_idx = 1
    last_line_idx = len(lines) - 2
    start = None
    end = None

    for y, line in enumerate(lines):
        y *= -1
        for x, char in enumerate(line):
            match char:
                case "#":
                    walls.add((x, y))
                case "<":
                    blizzards.append((Direction.WEST, (x, y)))
                case "^":
                    blizzards.append((Direction.NORTH, (x, y)))
                case ">":
                    blizzards.append((Direction.EAST, (x, y)))
                case "v":
                    blizzards.append((Direction.SOUTH, (x, y)))
                case "V":
                    blizzards.append((Direction.SOUTH, (x, y)))
                case ".":
                    if y == first_line_idx * -1:
                        start = (x, y)
                    elif y == last_line_idx * -1:
                        end = (x, y)
    assert start is not None
    assert end is not None
    return Valley(start, end, blizzards, walls)


@dataclass(frozen=True)
class Situation:
    time: int
    place: Coordinate
    target: Coordinate

    def __lt__(self, other):
        return self.time < other.time


def _search_exit(valley: Valley, start_time=0):
    start_situation = Situation(start_time, valley.start, valley.end)
    heap = [start_situation]
    memo = set()
    while heap:
        situation = heapq.heappop(heap)

        if situation in memo:
            continue
        else:
            memo.add(situation)

        if situation.place == situation.target:
            return situation.time

        new_time = situation.time + 1
        for new_place in valley.branch(new_time, situation.place):
            heapq.heappush(heap, Situation(new_time, new_place, situation.target))


@time_it
def part_a(input_: str):
    valley = _parse_valley(input_)
    return _search_exit(valley)


@time_it
def part_b(input_: str):
    sys.setrecursionlimit(10_000)
    valley = _parse_valley(input_)
    first = _search_exit(valley)
    reverse_valley = Valley(valley.end, valley.start, valley.blizzards, valley.walls)
    second = _search_exit(reverse_valley, first)
    third = _search_exit(valley, second)
    return third
