"""Solve day 1."""
from aoc.helpers import time_it


@time_it
def part_a(input_: str):
    """Part a?"""
    score = 0
    for line in input_.split("\n"):
        try:
            them, you = line.split(" ")
        except ValueError:
            continue

        match you:
            case "X":
                score += 1
                match them:
                    case "A":
                        score += 3
                    case "B":
                        score += 0
                    case "C":
                        score += 6
            case "Y":
                score += 2
                match them:
                    case "A":
                        score += 6
                    case "B":
                        score += 3
                    case "C":
                        score += 0
            case "Z":
                score += 3
                match them:
                    case "A":
                        score += 0
                    case "B":
                        score += 6
                    case "C":
                        score += 3
    return score


@time_it
def part_b(input_: str):
    """Part b."""
    score = 0
    for line in input_.split("\n"):
        try:
            them, outcome = line.split(" ")
        except ValueError:
            continue

        match outcome:
            case "X":
                score += 0
                match them:
                    case "A":
                        score += 3
                    case "B":
                        score += 1
                    case "C":
                        score += 2
            case "Y":
                score += 3
                match them:
                    case "A":
                        score += 1
                    case "B":
                        score += 2
                    case "C":
                        score += 3
            case "Z":
                score += 6
                match them:
                    case "A":
                        score += 2
                    case "B":
                        score += 3
                    case "C":
                        score += 1
    return score