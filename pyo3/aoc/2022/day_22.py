"""Solve day 22."""
import re
from dataclasses import dataclass
from enum import Enum
from typing import NewType, Sequence

from aoc.helpers import time_it

Coordinate = NewType("Coordinate", tuple[int, int])
PART_B = False


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


def _translate(
    pos: Coordinate, orientation: Orientation
) -> tuple[Coordinate, Orientation]:
    x, y = pos
    match (x, y, orientation):
        # Note: mind off-by-one errors, ranges go 0-49 etc.
        case (0, yy, Orientation.LEFT):
            if 100 <= yy < 150:
                return Coordinate((50, 149 - yy)), Orientation.RIGHT
            if 150 <= yy < 200:
                return Coordinate((yy - 100, 0)), Orientation.DOWN
        case (49, yy, Orientation.RIGHT):
            if 150 <= yy < 200:
                return Coordinate((yy - 100, 149)), Orientation.UP
        case (50, yy, Orientation.LEFT):
            if 0 <= yy < 50:
                return Coordinate((0, 149 - yy)), Orientation.RIGHT
            if 50 <= yy < 100:
                return Coordinate((yy - 50, 100)), Orientation.DOWN
        case (99, yy, Orientation.RIGHT):
            if 50 <= yy < 100:
                return Coordinate((yy + 50, 49)), Orientation.UP
            if 100 <= yy < 150:
                return Coordinate((149, 149 - yy)), Orientation.LEFT
        case (149, yy, Orientation.RIGHT):
            if 0 <= yy < 50:
                return Coordinate((99, 149 - yy)), Orientation.LEFT
        case (xx, 0, Orientation.UP):
            if 50 <= xx < 100:
                return Coordinate((0, 100 + xx)), Orientation.RIGHT
            if 100 <= xx < 150:
                return Coordinate((xx - 100, 199)), Orientation.UP
        case (xx, 49, Orientation.DOWN):
            if 100 <= xx < 150:
                return Coordinate((99, xx - 50)), Orientation.LEFT
        case (xx, 100, Orientation.UP):
            if 0 <= xx < 50:
                return Coordinate((50, 50 + xx)), Orientation.RIGHT
        case (xx, 149, Orientation.DOWN):
            if 50 <= xx < 100:
                return Coordinate((49, 100 + xx)), Orientation.LEFT
        case (xx, 199, Orientation.DOWN):
            if 0 <= xx < 50:
                return Coordinate((xx + 100, 0)), Orientation.DOWN
    raise RuntimeError("Not yet translated using the cardboard cube!!")


class RejectError(Exception):
    """Reject a cube step, there is a wall!"""


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

    def __evaluate_candidate(self, pos, candidate, orientation):
        if PART_B:
            try:
                new_candidate, new_orientation = _translate(pos, orientation)
            except RuntimeError:
                pass

        if candidate in self.__walls:
            # Reject candidate.
            raise RejectError("Wall!")
        elif candidate in self.__topology:
            # Accept candidate
            return candidate, orientation

        # Find a new candidate the old way.
        if not PART_B:
            match orientation:
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
            new_orientation = orientation

        try:
            return self.__evaluate_candidate(
                new_candidate, new_candidate, new_orientation
            )
        except RejectError:
            return pos, orientation

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
            try:
                pos, self.__orientation = self.__evaluate_candidate(
                    pos, candidate, self.__orientation
                )
            except RejectError:
                pass
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
    global PART_B
    PART_B = True
    start, topology, walls, instructions = _parse(input_)
    walker = Walker(start, topology, walls)
    walker.execute(instructions)
    return walker.score()
