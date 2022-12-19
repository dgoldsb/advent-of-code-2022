"""Solve day 19."""
import heapq
import re
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from typing import Generator

from aoc.helpers import time_it

MINUTES = 24


class RobotType(Enum):
    ORE = "ore"
    CLAY = "clay"
    OBSIDIAN = "obsidian"
    GEODE = "geode"


@dataclass(frozen=True)
class Minerals:
    ore: int
    clay: int
    obsidian: int
    geode: int

    def __add__(self, other):
        return Minerals(
            self.ore + other.ore,
            self.clay + other.clay,
            self.obsidian + other.obsidian,
            self.geode + other.geode,
        )

    def __sub__(self, other):
        return Minerals(
            self.ore - other.ore,
            self.clay - other.clay,
            self.obsidian - other.obsidian,
            self.geode - other.geode,
        )

    def __gt__(self, other):
        return (
            self.ore >= other.ore
            and self.clay >= other.clay
            and self.obsidian >= other.obsidian
            and self.geode >= other.geode
        )


@dataclass(frozen=True)
class Robots:
    ore: int
    clay: int
    obsidian: int
    geode: int

    def __add__(self, other):
        return Robots(
            self.ore + other.ore,
            self.clay + other.clay,
            self.obsidian + other.obsidian,
            self.geode + other.geode,
        )

    def produce(self) -> Minerals:
        return Minerals(
            self.ore,
            self.clay,
            self.obsidian,
            self.geode,
        )


@dataclass(frozen=True)
class State:
    next_robot_type: RobotType
    time: int = 0
    minerals: Minerals = Minerals(0, 0, 0, 0)
    robots: Robots = Robots(1, 0, 0, 0)

    def get_branches(self) -> Generator[RobotType, None, None]:
        if self.robots.obsidian:
            yield RobotType.GEODE
        if self.robots.clay:
            yield RobotType.OBSIDIAN
        yield RobotType.CLAY
        yield RobotType.ORE

    def __lt__(self, other):
        # Explore promising paths, heap will sort the other way around.
        return self.minerals.geode > other.minerals.geode or self.time > other.time

    def prune(self, best: int, costs: dict[RobotType, Minerals]):
        # Prevent that...
        time_remaining = MINUTES - self.time

        # We are behind our best and have no hope of catching up.
        if (
            self.minerals.geode
            + self.robots.geode * time_remaining
            + sum(range(time_remaining + 1))
        ) < best:
            return True

        # Never build more gathering robots than we can spend per turn.
        if (
            self.robots.clay > max((c.clay for c in costs.values()))
            or self.robots.ore > max((c.ore for c in costs.values()))
            or self.robots.obsidian > max((c.obsidian for c in costs.values()))
        ):
            return True

        return False


@dataclass
class Blueprint:

    id: int
    costs: dict[RobotType, Minerals]

    @property
    def quality_level(self):
        return self.crack_geodes() * self.id

    def crack_geodes(self):
        """Notes...

        We do not always spend all resources.
        Recursive function to find all branches.
        """
        best = 0
        heap = [State(RobotType.ORE), State(RobotType.CLAY)]
        visited = set()
        best_at_time = defaultdict(int)

        while heap:
            state = heapq.heappop(heap)

            minerals = state.minerals
            robots = state.robots

            best = max(best, state.minerals.geode)
            best_at_time[state.time] = max(
                best_at_time[state.time], state.minerals.geode
            )

            if state.time == MINUTES or state.prune(
                best_at_time[state.time], self.costs
            ):
                continue

            # Can I order my next robot?
            price = self.costs[state.next_robot_type]
            if price < state.minerals:
                building = True
                minerals -= price
            else:
                building = False

            # Mine
            minerals += state.robots.produce()

            # Build, if any
            if building:
                match state.next_robot_type:
                    case RobotType.ORE:
                        robots += Robots(1, 0, 0, 0)
                    case RobotType.CLAY:
                        robots += Robots(0, 1, 0, 0)
                    case RobotType.OBSIDIAN:
                        robots += Robots(0, 0, 1, 0)
                    case RobotType.GEODE:
                        robots += Robots(0, 0, 0, 1)

            # Prepare next, if we just built one, otherwise just update the state.
            updated_state = State(
                time=state.time + 1,
                minerals=minerals,
                robots=robots,
                next_robot_type=state.next_robot_type,
            )
            if building:
                for new_type in updated_state.get_branches():
                    new_state = State(
                        time=state.time + 1,
                        minerals=minerals,
                        robots=robots,
                        next_robot_type=new_type,
                    )
                    if new_state not in visited:
                        visited.add(new_state)
                        heapq.heappush(heap, new_state)
            else:
                heapq.heappush(heap, updated_state)

        return best


def _parse(input_: str) -> Generator[Blueprint, None, None]:
    regex = re.compile(
        "Blueprint (\d+)\D+(\d+)\D+(\d+)\D+(\d+)\D+(\d+)\D+(\d+)\D+(\d+)\D+\."
    )
    for result in regex.findall(input_):
        yield Blueprint(
            id=int(result[0]),
            costs={
                RobotType.ORE: Minerals(int(result[1]), 0, 0, 0),
                RobotType.CLAY: Minerals(int(result[2]), 0, 0, 0),
                RobotType.OBSIDIAN: Minerals(int(result[3]), int(result[4]), 0, 0),
                RobotType.GEODE: Minerals(int(result[5]), 0, int(result[6]), 0),
            },
        )


@time_it
def part_a(input_: str):
    result = sum((b.quality_level for b in _parse(input_)))
    #assert result == 1487, f"Got {result}"
    return result


@time_it
def part_b(input_: str):
    global MINUTES
    MINUTES = 32
    blueprints = list(_parse(input_))[:3]
    result = 1
    # 3472 in example
    # 13104 is too low, it is what I keep getting: 16, 39, 21
    for count in (b.crack_geodes() for b in blueprints):
        print(count)
        result *= count
    return result
