"""Solve day 1."""
from aoc.helpers import time_it


@time_it
def part_a(input_: str):
    return max(sum(int(y) for y in x.split("\n")) for x in input_.split("\n\n"))


@time_it
def part_b(input_: str):
    return sum(
        sorted(sum(int(y) for y in x.split("\n")) for x in input_.split("\n\n"))[-3:]
    )
