"""Solve day 4."""
from functools import lru_cache

from aoc.helpers import time_it


@lru_cache
def _solve(input_):
    a_count = 0
    b_count = 0
    for line in input_.split("\n"):
        a, b = line.split(",")
        a1, a2 = a.split("-")
        b1, b2 = b.split("-")
        ar = set(range(int(a1), int(a2) + 1))
        br = set(range(int(b1), int(b2) + 1))
        if ar.issubset(br) or br.issubset(ar):
            a_count += 1
        if ar.intersection(br):
            b_count += 1
    return a_count, b_count


@time_it
def part_a(input_: str):
    return _solve(input_)[0]


@time_it
def part_b(input_: str):
    return _solve(input_)[1]
