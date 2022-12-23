"""Solve day 23."""
from collections import defaultdict
from enum import Enum
from typing import Generator, Collection

from aoc.helpers import time_it


class Direction(Enum):
    NORTH = "N"
    SOUTH = "S"
    WEST = "W"
    EAST = "E"


class Elf:
    def __init__(self, loc: tuple[int, int]):
        self.loc = loc
        self.__history = [
            Direction.NORTH,
            Direction.SOUTH,
            Direction.WEST,
            Direction.EAST,
        ]
        self.__idx = 0

    def move(self, new_loc: tuple[int, int]):
        self.loc = new_loc

    def shift_priority(self):
        self.__idx += 1

    def propose_move(self, others: set[tuple[int, int]]) -> tuple[int, int]:
        # Is someone around us?
        if not {
            (self.loc[0] + 1, self.loc[1]),
            (self.loc[0] - 1, self.loc[1]),
            (self.loc[0], self.loc[1] + 1),
            (self.loc[0], self.loc[1] - 1),
            (self.loc[0] + 1, self.loc[1] + 1),
            (self.loc[0] - 1, self.loc[1] + 1),
            (self.loc[0] + 1, self.loc[1] - 1),
            (self.loc[0] - 1, self.loc[1] - 1),
        }.intersection(others):
            return self.loc

        # If someone is, we move!
        for i in range(4):
            idx = (self.__idx + i) % 4
            d = self.__history[idx]
            match d:
                case Direction.NORTH:
                    if {
                        (self.loc[0], self.loc[1] + 1),
                        (self.loc[0] + 1, self.loc[1] + 1),
                        (self.loc[0] - 1, self.loc[1] + 1),
                    }.isdisjoint(others):
                        return self.loc[0], self.loc[1] + 1
                case Direction.SOUTH:
                    if {
                        (self.loc[0], self.loc[1] - 1),
                        (self.loc[0] + 1, self.loc[1] - 1),
                        (self.loc[0] - 1, self.loc[1] - 1),
                    }.isdisjoint(others):
                        return self.loc[0], self.loc[1] - 1
                case Direction.WEST:
                    if {
                        (self.loc[0] - 1, self.loc[1]),
                        (self.loc[0] - 1, self.loc[1] + 1),
                        (self.loc[0] - 1, self.loc[1] - 1),
                    }.isdisjoint(others):
                        return self.loc[0] - 1, self.loc[1]
                case Direction.EAST:
                    if {
                        (self.loc[0] + 1, self.loc[1]),
                        (self.loc[0] + 1, self.loc[1] + 1),
                        (self.loc[0] + 1, self.loc[1] - 1),
                    }.isdisjoint(others):
                        return self.loc[0] + 1, self.loc[1]
        else:
            return self.loc


def _parse(input_: str) -> Generator[Elf, None, None]:
    for y, line in enumerate(input_.splitlines()):
        y *= -1
        for x, char in enumerate(line):
            if char == "#":
                yield Elf((x, y))


def _evolve(elves: Collection[Elf]) -> Generator[Elf, None, None]:
    elf_locations = {e.loc for e in elves}
    desired_moves = defaultdict(list)

    for elf in elves:
        target_loc = elf.propose_move(elf_locations)
        desired_moves[target_loc].append(elf)
        elf.shift_priority()

    for target_loc, elves in desired_moves.items():
        if len(elves) < 2:
            for elf in elves:
                elf.loc = target_loc
                yield elf
        else:
            for elf in elves:
                yield elf


def _score(elves: Collection[Elf]) -> int:
    return (
        (max((e.loc[0] for e in elves)) - min((e.loc[0] for e in elves)) + 1)
        * (max((e.loc[1] for e in elves)) - min((e.loc[1] for e in elves)) + 1)
    ) - len(elves)


@time_it
def part_a(input_: str):
    elves = list(_parse(input_))
    for _ in range(10):
        elves = list(_evolve(elves))
    return _score(elves)


@time_it
def part_b(input_: str):
    elves = list(_parse(input_))
    moves = 0
    while True:
        old_locs = {e.loc for e in elves}
        elves = list(_evolve(elves))
        moves += 1
        new_locs = {e.loc for e in elves}
        if old_locs == new_locs:
            break
    return moves
