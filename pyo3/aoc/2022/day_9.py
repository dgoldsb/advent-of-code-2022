"""Solve day 9."""
from aoc.helpers import time_it


def _get_mod(diff: int, contract: bool):
    if contract:
        _mod = 1 if diff > 1 or diff < -1 else 0
        if _mod == 0:
            return 0
    else:
        if diff == 0:
            return 0
        _mod = diff

    if diff < 0 and _mod:
        return -1
    return 1


class Rope:
    def __init__(self, length=2):
        self.__segment_locations = [(0, 0)] * length
        self.tail_locations = set()

    def _follow(self, index: int):
        head_x, head_y = self.__segment_locations[index - 1]
        tail_x, tail_y = self.__segment_locations[index]
        x_diff = head_x - tail_x
        y_diff = head_y - tail_y

        if not (-1 <= x_diff <= 1 and -1 <= y_diff <= 1):
            contraction = x_diff == 0 or y_diff == 0
            x_mod = _get_mod(x_diff, contraction)
            y_mod = _get_mod(y_diff, contraction)

            self.__segment_locations[index] = (tail_x + x_mod, tail_y + y_mod)

    def _apply(self, instruction: chr):
        match instruction:
            case "U":
                mod = (0, 1)
            case "D":
                mod = (0, -1)
            case "L":
                mod = (-1, 0)
            case "R":
                mod = (1, 0)
            case _:
                raise RuntimeError("Unknown operation!")
        self.__segment_locations[0] = (
            self.__segment_locations[0][0] + mod[0],
            self.__segment_locations[0][1] + mod[1],
        )
        for i in range(1, len(self.__segment_locations)):
            self._follow(i)
        self.tail_locations.add(self.__segment_locations[-1])

    def apply(self, instruction: chr, times: int):
        for _ in range(times):
            self._apply(instruction)


@time_it
def part_a(input_: str):
    rope = Rope()
    for line in input_.split("\n"):
        op, num = line.split(" ")
        rope.apply(op, int(num))
    return len(rope.tail_locations)


@time_it
def part_b(input_: str):
    rope = Rope(10)
    for line in input_.split("\n"):
        op, num = line.split(" ")
        rope.apply(op, int(num))
    return len(rope.tail_locations)
