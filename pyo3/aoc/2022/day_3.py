"""Solve day 3."""
from aoc.helpers import time_it


def _to_int(c):
    if ord(c) > 96:
        return ord(c) - 96
    if ord(c) > 64:
        return ord(c) - 64 + 26


def _find_a(s):
    half = len(s) // 2
    first = set(s[:half])
    second = set(s[half:])
    return first.intersection(second).pop()


def _find_b(a, b, c):
    return set(a).intersection(set(b)).intersection(set(c)).pop()


@time_it
def part_a(input_: str):
    total = 0
    for line in input_.split("\n"):
        total += _to_int(_find_a(line))
    return total


@time_it
def part_b(input_: str):
    total = 0
    split = input_.split("\n")
    for i in range(0, len(split), 3):
        badge = _find_b(split[i], split[i + 1], split[i + 2])
        total += _to_int(badge)
    return total
