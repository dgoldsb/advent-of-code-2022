"""Solve day 5."""
from collections import defaultdict

from aoc.helpers import time_it


def _solve(input_: str, is_a: bool):
    raw_state, raw_ops = input_.split("\n\n")

    keys = tuple(str(i) for i in range(1, 10))

    state = defaultdict(list)
    for line in raw_state.split("\n"):
        for i in range(0, 9):
            index = 1 + i * 4
            try:
                crate = line[index]
                if crate != " " and crate not in state:
                    state[keys[i]].append(crate)
            except IndexError:
                pass

    for op in raw_ops.split("\n"):
        _, num, _, fr, _, to = op.split(" ")

        movestack = []
        for _ in range(int(num)):
            crate = state[fr].pop(0)
            movestack.append(crate)
        if is_a:
            movestack.reverse()
        state[to] = movestack + state[to]

    result = ""
    for key in keys:
        if state[key]:
            result += state[key][0]
    return result


@time_it
def part_a(input_: str):
    return _solve(input_, True)


@time_it
def part_b(input_: str):
    return _solve(input_, False)
