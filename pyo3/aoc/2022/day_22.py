"""Solve day 22."""
import re
from dataclasses import dataclass
from enum import Enum
from typing import NewType, Sequence

from aoc.helpers import time_it

Coordinate = NewType("Coordinate", tuple[int, int])


class Rotation(Enum):
    LEFT = "L"
    RIGHT = "R"
    NEUTRAL = "N"


class Orientation(Enum):
    UP = "^"
    DOWN = "v"
    LEFT = "<"
    RIGHT = ">"

    def turn(self, rotation: Rotation) -> "Orientation":
        class_ = type(self)
        match self:
            case class_.RIGHT:
                match rotation:
                    case Rotation.RIGHT:
                        return class_.DOWN
                    case Rotation.LEFT:
                        return class_.UP
            case class_.DOWN:
                match rotation:
                    case Rotation.RIGHT:
                        return class_.LEFT
                    case Rotation.LEFT:
                        return class_.RIGHT
            case class_.LEFT:
                match rotation:
                    case Rotation.RIGHT:
                        return class_.UP
                    case Rotation.LEFT:
                        return class_.DOWN
            case class_.UP:
                match rotation:
                    case Rotation.RIGHT:
                        return class_.RIGHT
                    case Rotation.LEFT:
                        return class_.LEFT
        return self


@dataclass
class Instruction:
    walk: int
    rotate: Rotation


class Walker:
    def __init__(
        self, start: Coordinate, topology: set[Coordinate], walls: set[Coordinate]
    ):
        self.__position = start
        self.__orientation = Orientation.RIGHT
        self.__topology = topology
        self.__walls = walls
        self.__all = topology.union(walls)

    def execute(self, instructions: Sequence[Instruction]):
        for instruction in instructions:
            self.__position = self.__move(distance=instruction.walk)
            self.__orientation = self.__orientation.turn(instruction.rotate)

    def __evaluate_candidate(self, pos, candidate):
        if candidate in self.__walls:
            # Reject candidate.
            return pos
        elif candidate in self.__topology:
            # Accept candidate
            return candidate
        else:
            # Find a new candidate.
            match self.__orientation:
                # Loading topology left -> right, up -> down. This flips the up/down
                # directions of the player.
                case Orientation.RIGHT:
                    new_candidate = (
                        min(p[0] for p in self.__all if p[1] == candidate[1]),
                        candidate[1],
                    )
                case Orientation.LEFT:
                    new_candidate = (
                        max(p[0] for p in self.__all if p[1] == candidate[1]),
                        candidate[1],
                    )
                case Orientation.UP:
                    new_candidate = (
                        candidate[0],
                        max(p[1] for p in self.__all if p[0] == candidate[0]),
                    )
                case Orientation.DOWN:
                    new_candidate = (
                        candidate[0],
                        min(p[1] for p in self.__all if p[0] == candidate[0]),
                    )
                case _:
                    raise RuntimeError("Invalid orientation.")
            return self.__evaluate_candidate(pos, new_candidate)

    def __move(self, distance: int) -> Coordinate:
        pos = self.__position
        for _ in range(distance):
            match self.__orientation:
                # Loading topology left -> right, up -> down. This flips the up/down
                # directions of the player.
                case Orientation.RIGHT:
                    candidate = (pos[0] + 1, pos[1])
                case Orientation.LEFT:
                    candidate = (pos[0] - 1, pos[1])
                case Orientation.UP:
                    candidate = (pos[0], pos[1] - 1)
                case Orientation.DOWN:
                    candidate = (pos[0], pos[1] + 1)
                case _:
                    raise RuntimeError("Invalid orientation.")
            pos = self.__evaluate_candidate(pos, candidate)
        return pos

    def score(self) -> int:
        row = self.__position[1] + 1
        column = self.__position[0] + 1
        match self.__orientation:
            case Orientation.RIGHT:
                facing = 0
            case Orientation.LEFT:
                facing = 2
            case Orientation.UP:
                facing = 3
            case Orientation.DOWN:
                facing = 1
            case _:
                raise RuntimeError("Invalid orientation.")
        return 1000 * row + 4 * column + facing


def _parse(input_: str):
    rt, ri = input_.split("\n\n")

    topology = set()
    walls = set()
    start_yielded = False

    for y, line in enumerate(rt.splitlines()):
        for x, char in enumerate(line):
            match char:
                case "#":
                    walls.add((x, y))
                case ".":
                    if not start_yielded:
                        yield x, y
                        start_yielded = True
                    topology.add((x, y))
    yield topology
    yield walls

    regex = re.compile("(\d+)([LRN])")
    ri += "N"  # safety for regex, this is a no-op
    instructions = []
    for match in regex.findall(ri):
        instructions.append(Instruction(int(match[0]), Rotation(match[1])))
    yield instructions


@time_it
def part_a(input_: str):
    start, topology, walls, instructions = _parse(input_)
    walker = Walker(start, topology, walls)
    walker.execute(instructions)
    return walker.score()


@time_it
def part_b(input_: str):
    return None
