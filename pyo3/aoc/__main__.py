"""Runs and times all days."""
from importlib import import_module
from typing import Any, Callable

from aoc.helpers import TIMES, get_input


def _get_solver(year: int, day: int, part: str) -> Callable[[str], Any]:
    """Dynamically import fetch an AoC solver."""
    mod = import_module(f"aoc.{year}.day_{day}")
    return getattr(mod, f"part_{part}")


def main():
    for year in (2022,):
        for day in range(17, 26):
            for part in ("a", "b"):
                try:
                    solver = _get_solver(year, day, part)
                    solution = solver(get_input(year, day))
                    print(f"{year}.{day}.{part}: {solution}")
                except (AttributeError, ImportError):
                    continue
    total_time = sum(TIMES.values())
    print(f"\nTotal time taken (solvers only): {total_time}")


if __name__ == "__main__":
    main()
