"""Solve day 17."""
from typing import Generator

from aoc.helpers import time_it


def _jets(input_: str) -> Generator[bool, None, None]:
    input_.replace("\n", "")
    pointer = 0
    while True:
        yield input_[pointer] == "<"  # > is false
        pointer = (pointer + 1) % len(input_)


def _rock_types() -> Generator[str, None, None]:
    while True:
        yield "-"
        yield "+"
        yield "L"
        yield "I"
        yield "#"


def _get_rock(current_highest_y: int, rock_type: str) -> set[tuple[int, int]]:
    match rock_type:
        case "+":
            return {
                (2, current_highest_y + 5),
                (3, current_highest_y + 4),
                (3, current_highest_y + 5),
                (3, current_highest_y + 6),
                (4, current_highest_y + 5),
            }
        case "-":
            return {
                (2, current_highest_y + 4),
                (3, current_highest_y + 4),
                (4, current_highest_y + 4),
                (5, current_highest_y + 4),
            }
        case "L":
            return {
                (2, current_highest_y + 4),
                (3, current_highest_y + 4),
                (4, current_highest_y + 4),
                (4, current_highest_y + 5),
                (4, current_highest_y + 6),
            }
        case "I":
            return {
                (2, current_highest_y + 4),
                (2, current_highest_y + 5),
                (2, current_highest_y + 6),
                (2, current_highest_y + 7),
            }
        case "#":
            return {
                (2, current_highest_y + 4),
                (3, current_highest_y + 4),
                (2, current_highest_y + 5),
                (3, current_highest_y + 5),
            }


def _collides(rock: set[tuple[int, int]], state: set[tuple[int, int]]) -> bool:
    left_wall = {(-1, y) for _, y in rock}
    right_wall = {(7, y) for _, y in rock}
    return (
        bool(rock.intersection(state))
        or bool(rock.intersection(left_wall))
        or bool(rock.intersection(right_wall))
    )


def _print(state, current_highest_y):
    for y in range(current_highest_y, 0, -1):
        line = "|"
        for x in range(7):
            if (x, y) in state:
                line += "#"
            else:
                line += "."
        line += "|"
        print(line)


def _is_cycle(increases):
    for i in range(len(increases)):
        candidate = increases[i:]
        if len(candidate) < 1000:
            continue

        if candidate[: len(candidate) // 2] == candidate[len(candidate) // 2 :]:
            return i, candidate[: len(candidate) // 2]
    return None


def _solve(input_: str, rock_count: int):
    state: set[tuple[int, int]] = {(x, 0) for x in range(7)}
    current_highest_y = 0
    jet_iterable = _jets(input_)
    rock_type_iterable = _rock_types()
    changes = []

    for _ in range(rock_count):
        rock = _get_rock(current_highest_y, next(rock_type_iterable))

        while True:
            # Jet manipulation.
            if next(jet_iterable):  # left
                shifted_rock = {(x - 1, y) for x, y in rock}
            else:
                shifted_rock = {(x + 1, y) for x, y in rock}

            # Collision check.
            if not _collides(shifted_rock, state):
                rock = shifted_rock

            # Gravity manipulation.
            fallen_rock = {(x, y - 1) for x, y in rock}

            if not _collides(fallen_rock, state):
                rock = fallen_rock
            else:
                state = state.union(rock)
                new_highest_y = max(current_highest_y, max((y for _, y in rock)))
                changes.append(new_highest_y - current_highest_y)
                current_highest_y = new_highest_y
                break

        if (cycle := _is_cycle(changes)) is not None:
            start_index, cycle = cycle
            cycles = (rock_count - start_index) // len(cycle)
            remainder = (rock_count - start_index) % len(cycle)
            return (
                sum(changes[:start_index])
                + cycles * sum(cycle)
                + sum(cycle[:remainder])
            )

    return current_highest_y


@time_it
def part_a(input_: str):
    return _solve(input_, 2022)


@time_it
def part_b(input_: str):
    return _solve(input_, 1000000000000)
