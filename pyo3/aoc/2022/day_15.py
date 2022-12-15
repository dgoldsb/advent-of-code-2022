"""Solve day 15."""
import re
from dataclasses import dataclass
from typing import Generator, Iterable

from aoc.helpers import time_it

MAGIC_ROW_A = 2000000
RANGE_MAX = 4000000
REGEX = re.compile("x=([-0-9]+), y=([-0-9]+)")


@dataclass
class Diamond:
    centre: tuple[int, int]
    manhattan: int

    def spans_row(self, y):
        """Return if `y` intersects this diamond."""
        return self.centre[1] + self.manhattan >= y > self.centre[1] - self.manhattan

    def row(self, y) -> range:
        """Return all points in row `y`."""
        y_mod = abs(max(self.centre[1], y) - min(self.centre[1], y))
        x_mod = self.manhattan - y_mod
        return range(self.centre[0] - x_mod, self.centre[0] + x_mod)


def _parse(input_: str) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
    sensors, beacons = [], []
    results = iter(REGEX.findall(input_))
    while True:
        try:
            result = next(results)
            sensors.append((int(result[0]), int(result[1])))
            result = next(results)
            beacons.append((int(result[0]), int(result[1])))
        except StopIteration:
            break
    return sensors, beacons


def _manhattan_distance(x: tuple[int, int], y: tuple[int, int]) -> int:
    return abs(max(x[0], y[0]) - min(x[0], y[0])) + abs(
        max(x[1], y[1]) - min(x[1], y[1])
    )


def _diamonds(sensors, beacons) -> Generator[Diamond, None, None]:
    for sensor, beacon in zip(sensors, beacons):
        yield Diamond(sensor, _manhattan_distance(sensor, beacon))


def overlap(range1, range2):
    if range1.start <= range2.stop and range2.start <= range1.stop:
        return True
    return False


def _merge_ranges(ranges: Iterable[range]) -> list[range]:  # TODO: Rework with b.
    ranges = list(ranges)
    ranges_copy = sorted(ranges.copy(), key=lambda x: x.stop)
    ranges_copy = sorted(ranges_copy, key=lambda x: x.start)
    merged_ranges = []

    while ranges_copy:
        range1 = ranges_copy[0]
        del ranges_copy[0]

        merges = []

        for i, range2 in enumerate(ranges_copy):
            if overlap(range1, range2):
                range1 = range(
                    min([range1.start, range2.start]),
                    max([range1.stop, range2.stop]),
                )
                merges.append(i)

        merged_ranges.append(range1)

        for i in reversed(merges):
            del ranges_copy[i]

    return merged_ranges


@time_it
def part_a(input_: str):
    result = sum(
        (
            len(r)
            for r in _merge_ranges(
                d.row(MAGIC_ROW_A)
                for d in _diamonds(*_parse(input_))
                if d.spans_row(MAGIC_ROW_A)
            )
        )
    )
    return result


@time_it
def part_b(input_: str):
    for i in range(0, RANGE_MAX):
        ranges = [
            d.row(i) for d in _diamonds(*_parse(input_))
            if d.spans_row(i)
        ]
        bounded_ranges = [
            range(max(0, min(r.start, r.stop)), min(RANGE_MAX, max(r.start, r.stop)))
            for r in ranges
        ]
        merged_ranges = _merge_ranges(bounded_ranges)
        if merged_ranges != [range(0, RANGE_MAX)]:
            for range_ in merged_ranges:
                if range_.start == 0:
                    return i + ((range_.stop + 1) * 4000000)
            return merged_ranges
    else:
        raise RuntimeError("No answer found...")
