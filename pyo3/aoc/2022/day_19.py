"""Solve day 19."""
import heapq
import re
from collections import defaultdict
from dataclasses import dataclass
from typing import Generator

from aoc.helpers import time_it

MINUTES = 24

# TODO: Go by which robot next.


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


# Bit hacky, maximum we want before pruning.
MAX_MINERALS = Minerals(0, 0, 0, 0)


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
    time: int = 0
    minerals: Minerals = Minerals(0, 0, 0, 0)
    robots: Robots = Robots(1, 0, 0, 0)

    def __lt__(self, other):
        # First sort by time, less is earlier, then by geode count.
        # TODO: Go deep first
        return self.time > other.time or (
            self.time == other.time and self.minerals.geode > other.minerals.geode
        )

    def prune(self, best: int):
        # Prevent that...
        return (
            # We have too many arbitrary robots.
            self.robots.clay > 10 or
            self.robots.ore > 20 or
            self.robots.obsidian > 10 or
            # We saved too much.
            self.minerals.clay > MAX_MINERALS.clay or
            self.minerals.ore > MAX_MINERALS.ore or
            self.minerals.obsidian > MAX_MINERALS.obsidian or
            # We are behind our best.
            # TODO: part 2 has catchup possibilities, part 1 does not.
            self.minerals.geode + 2 < best
        )


@dataclass
class Blueprint:

    id: int
    ore_robot_cost: Minerals
    clay_robot_cost: Minerals
    obsidian_robot_cost: Minerals
    geode_robot_cost: Minerals

    @property
    def quality_level(self):
        return self.crack_geodes() * self.id

    def _get_branches(
        self, current_minerals: Minerals
    ) -> list[tuple[Robots, Minerals]]:
        bought = []

        if current_minerals > self.geode_robot_cost:
            bought.append((Robots(0, 0, 0, 1), self.geode_robot_cost))
            return bought

        if current_minerals > self.ore_robot_cost:
            bought.append((Robots(1, 0, 0, 0), self.ore_robot_cost))

        if current_minerals > self.clay_robot_cost:
            bought.append((Robots(0, 1, 0, 0), self.clay_robot_cost))

        if current_minerals > self.obsidian_robot_cost:
            bought.append((Robots(0, 0, 1, 0), self.obsidian_robot_cost))

        bought.append((Robots(0, 0, 0, 0), Minerals(0, 0, 0, 0)))

        return bought

    def crack_geodes(self):
        """Notes...

        We do not always spend all resources.
        Recursive function to find all branches.
        """
        global MAX_MINERALS

        MAX_MINERALS = Minerals(
            2 * max(self.ore_robot_cost.ore, self.clay_robot_cost.ore, self.obsidian_robot_cost.ore, self.geode_robot_cost.ore),
            2 * max(self.ore_robot_cost.clay, self.clay_robot_cost.clay, self.obsidian_robot_cost.clay, self.geode_robot_cost.clay),
            2 * max(self.ore_robot_cost.obsidian, self.clay_robot_cost.obsidian, self.obsidian_robot_cost.obsidian, self.geode_robot_cost.obsidian),
            0,
        )

        best = 0
        heap = [State()]
        visited = set()
        best_at_time = defaultdict(int)

        while heap:
            state = heapq.heappop(heap)

            best = max(best, state.minerals.geode)
            best_at_time[state.time] = max(
                best_at_time[state.time], state.minerals.geode
            )

            if state.time == MINUTES or state.prune(best_at_time[state.time]):
                continue
            print(state)
            # Order robots
            branches = self._get_branches(state.minerals)

            # Mine
            post_mine_minerals = state.minerals + state.robots.produce()

            # Build
            for robot, cost in branches:
                post_build_state = State(
                    state.time + 1,
                    minerals=post_mine_minerals - cost,
                    robots=state.robots + robot,
                )

                if post_build_state not in visited:
                    visited.add(post_build_state)
                    heapq.heappush(heap, post_build_state)
        return best


def _parse(input_: str) -> Generator[Blueprint, None, None]:
    regex = re.compile(
        "Blueprint (\d+)\D+(\d+)\D+(\d+)\D+(\d+)\D+(\d+)\D+(\d+)\D+(\d+)\D+\."
    )
    for result in regex.findall(input_):
        yield Blueprint(
            id=int(result[0]),
            ore_robot_cost=Minerals(int(result[1]), 0, 0, 0),
            clay_robot_cost=Minerals(int(result[2]), 0, 0, 0),
            obsidian_robot_cost=Minerals(int(result[3]), int(result[4]), 0, 0),
            geode_robot_cost=Minerals(int(result[5]), 0, int(result[6]), 0),
        )


@time_it
def part_a(input_: str):
    result = sum((b.quality_level for b in _parse(input_)))
    assert result == 1487, f"Got {result}"
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
