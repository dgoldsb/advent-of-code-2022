"""Helpers in the project."""
import re
import time
from functools import lru_cache
from itertools import zip_longest
from pathlib import Path
from typing import Generator, Iterable

INPUTS = Path(__file__).parents[1] / "inputs"
TIMES = {}


@lru_cache
def get_input(year: int, day: int) -> str:
    """Get input, first try AoC token, then input file."""
    # TODO: AoC token first, save the input.
    return (INPUTS / str(year) / f"{day}.txt").read_text()


def ints(input_: str) -> Generator[int, None, None]:
    for int_str in re.split(r"\D+", input_):
        try:
            yield int(int_str)
        except ValueError:
            pass


def group(n: int, iterable: Iterable, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)


def time_it(func):
    def wrapped(*args, **kwargs):
        begin = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"(Took {end - begin})")
        TIMES[func] = end - begin
        return result

    return wrapped
