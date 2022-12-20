"""Solve day 20."""
from collections import deque
from copy import copy

from aoc.helpers import time_it


def _parse(input_: str) -> deque[tuple[int, int]]:
    return deque((i, int(v)) for i, v in enumerate(input_.split("\n")))


def _mix(q: deque, r: int):
    v = q.popleft()
    q.rotate(-1 * r)
    q.appendleft(v)


def _put_first(q: deque, v):
    rota = q.index(v) + 1
    q.rotate(-1 * (rota - 1))


@time_it
def part_a(input_: str):
    all_items = _parse(input_)

    all_items_copy = copy(all_items)

    zero_item = None
    for t in all_items_copy:
        _put_first(all_items, t)
        if (rotation := all_items[0][1]) != 0:
            _mix(all_items, rotation)
        else:
            zero_item = t

    # Rotate to a zero.
    _put_first(all_items, zero_item)

    result = 0
    for _ in range(3):
        all_items.rotate(-1000)
        print(all_items[0][1])
        result += all_items[0][1]
    return result


@time_it
def part_b(input_: str):
    return None
