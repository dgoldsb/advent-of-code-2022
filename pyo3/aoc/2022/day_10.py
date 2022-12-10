"""Solve day 10."""
from functools import lru_cache

from aoc.helpers import time_it


def _reverse(pixels):
    cycle = 0
    x_register = 1
    instructions = []

    while cycle < len(pixels) - 2:
        future_cycle = (cycle + 2)
        is_lit = x_register - 1 <= future_cycle % 40 <= x_register + 1
        should_be_lit = pixels[future_cycle] == "#"

        if is_lit and should_be_lit or (not is_lit and not should_be_lit):
            instructions += ["noop"]
            cycle += 1
        elif is_lit and not should_be_lit:
            move = future_cycle  % 40 - x_register + 3
            instructions += [f"addx {move}"]
            x_register += move
            cycle += 2
        elif not is_lit and should_be_lit:
            try:
                should_be_lit_2 = pixels[future_cycle + 1] == "#"
            except IndexError:
                should_be_lit_2 = False
            try:
                should_be_lit_3 = pixels[future_cycle + 2] == "#"
            except IndexError:
                should_be_lit_3 = False

            if should_be_lit_2 and should_be_lit_3:
                move = future_cycle % 40 - x_register + 1
            elif should_be_lit_2:
                move = future_cycle % 40 - x_register + 0
            else:
                move = future_cycle % 40 - x_register - 1
            x_register += move
            instructions += [f"addx {move}"]
            cycle += 2

    instructions.extend(["noop", "noop"])
    return instructions


@lru_cache
def _solve(input_: str):
    x_register, result, operations, pixels = 1, 0, [], ""

    for line in input_.split("\n"):
        match line.split(" "):
            case "addx", num:
                operations.extend([0, int(num)])
            case _:
                operations.append(0)

    for i, op in enumerate(operations):
        cycle = i + 1

        if cycle in (20, 60, 100, 140, 180, 220):
            result += x_register * cycle

        if x_register - 1 <= i % 40 <= x_register + 1:
            pixels += "#"
        else:
            pixels += " "

        if cycle % 40 == 0:
            pixels += "\n"

        x_register += op
    return result, pixels


@time_it
def part_a(input_: str):
    result, _ = _solve(input_)
    return result


@time_it
def part_b(input_: str):
    _, pixels = _solve(input_)
    print(pixels)
    return None


art = """
######## ####### ####### ########       
   ##    ##      ##         ##          
   ##    #####   #######    ##          
   ##    ##           ##    ##          
   ##    ####### #######    ##          
""".replace("\n", "")
instructions = _reverse(art)
