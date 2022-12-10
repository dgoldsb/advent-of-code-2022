"""Solve day 10."""
from functools import lru_cache

from aoc.helpers import time_it


@lru_cache
def _solve(input_: str):
    x_register, result, operations, pixels = 1, 0, [], ""

    for line in input_.split("\n"):
        match line.split(" "):
            case "addx", num:
                operations.extend([0, int(num)])
            case _:
                operations.append(0)

    for i, op in enumerate(operations):
        cycle = i + 1

        if cycle in (20, 60, 100, 140, 180, 220):
            result += x_register * cycle

        if x_register - 1 <= i % 40 <= x_register + 1:
            pixels += "#"
        else:
            pixels += " "

        if cycle % 40 == 0:
            pixels += "\n"

        x_register += op
    return result, pixels


@time_it
def part_a(input_: str):
    result, _ = _solve(input_)
    return result


@time_it
def part_b(input_: str):
    _, pixels = _solve(input_)
    print(pixels)
    return None
