"""Solve day 21."""
# TODO: Try tree for faster less hacky way.
import re

from aoc.helpers import time_it

PURE_EQUATION = re.compile("^[^a-z]+$")


def _parse(input_: str) -> dict[str, str]:
    return {l.split(": ")[0]: l.split(": ")[1] for l in input_.splitlines()}


def _get_equation(d: dict[str, str]):
    while True:
        if PURE_EQUATION.match(d["root"]):
            return d["root"]
        else:
            for kr, er in d.items():
                for kt, et in d.items():
                    d[kt] = et.replace(kr, f"({er})")


@time_it
def part_a(input_: str):
    return int(eval(_get_equation(_parse(input_))))


@time_it
def part_b(input_: str):
    d = _parse(input_)
    d["humn"] = "X"
    d["root"] = d["root"].replace(" + ", " == ")
    eql, eqr = _get_equation(d).split(" == ")
    min_, max_ = 0, 1000_000_000_000_000_000
    target = eval(eqr)
    while True:
        X = (min_ + max_) // 2
        if (actual := eval(eql)) == target:
            return X
        elif actual > target:
            min_ = X
        else:
            max_ = X
