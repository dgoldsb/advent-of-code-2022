"""Solve day 16."""
import heapq
import re
from copy import copy
from dataclasses import dataclass

from aoc.helpers import time_it

REGEX = re.compile(
    "Valve ([A-Z]+) has flow rate=(\d+); tunnels? leads? to valves? ([^\n]+)"
)
START = "AA"
STEPS = 30
VENTS_THAT_MATTER = set()


@dataclass(frozen=True)
class Valve:
    name: str
    value: int


@dataclass
class State:
    locations: list[Valve]
    active: set[Valve]

    time: int = 0
    pressure_released: int = 0

    def __lt__(self, other):
        # For the heap, invert.
        return self.pressure_released > other.pressure_released

    def __str__(self):
        return str(
            (
                tuple(sorted((a.name for a in self.locations))),
                tuple(sorted((a.name for a in self.active))),
                self.time,
                self.pressure_released,
            )
        )

    def __hash__(self):
        return hash(str(self))

    def move_time(self) -> "State":
        return State(
            locations=self.locations,
            time=self.time + 1,
            pressure_released=self.pressure_released
            + sum((v.value for v in self.active)),
            active=self.active,
        )

    def open(self, valve) -> "State":
        active = copy(self.active)
        active.add(valve)
        return State(
            locations=self.locations,
            time=self.time,
            pressure_released=self.pressure_released,
            active=active,
        )

    def move(self, new_locations: list[Valve]) -> "State":
        return State(
            locations=new_locations,
            time=self.time,
            pressure_released=self.pressure_released,
            active=self.active,
        )

    def can_reach(self, target: int, bound: int) -> bool:
        steps_remaining = 26 - self.time
        gap = target - self.pressure_released
        return steps_remaining * bound > gap

    def all_vents_open(self) -> bool:
        return self.active == VENTS_THAT_MATTER


def _parse(input_: str) -> tuple[Valve, dict[Valve, list[Valve]]]:
    _valves = {}
    _map = {}
    for result in REGEX.findall(input_):
        valve = Valve(result[0], int(result[1]))
        _valves[valve.name] = valve
        _map[valve.name] = list(result[2].split(", "))
        if valve.value:
            VENTS_THAT_MATTER.add(valve)
    return _valves[START], {
        _valves[k]: [_valves[w] for w in v] for k, v in _map.items()
    }


def _solve(starts: list[Valve], valve_map: dict[Valve, list[Valve]]):
    best = 100
    heap = [State(starts, set())]
    bound = sum((v.value for v in valve_map.keys()))
    steps = STEPS - (4 * (len(starts) - 1))
    print(steps)
    visited = set()
    best_at_time = dict()

    while heap:
        state = heapq.heappop(heap)

        # Pruning.
        # TODO: All vents open
        if (
            state.time >= steps or state in visited or not state.can_reach(best, bound)
        ):  # or state.all_vents_open():
            continue

        if state.pressure_released < best_at_time.get(state.time - 1, 0):
            continue

        visited.add(state)

        # Cross product.
        actions: list[list[tuple[bool, Valve]]] = []

        for location in state.locations:
            actions.append([])
            for next_valve in valve_map[location]:
                actions[-1].append((False, next_valve))

            if location not in state.active and location.value:
                actions[-1].append((True, location))

        if len(actions) == 2:
            for action_1 in actions[0]:
                for action_2 in actions[1]:
                    activate_1, location_1 = action_1
                    activate_2, location_2 = action_2

                    new_state = state.move([location_1, location_2])
                    if activate_1:
                        new_state = new_state.open(location_1)
                    if activate_2:
                        new_state = new_state.open(location_2)
                    new_state = new_state.move_time()
                    heapq.heappush(heap, new_state)
        else:
            for action_1 in actions[0]:
                activate_1, location_1 = action_1

                new_state = state.move([location_1])
                if activate_1:
                    new_state = new_state.open(location_1)
                new_state = new_state.move_time()
                heapq.heappush(heap, new_state)

        best = max(state.pressure_released, best)
        best_at_time[state.time] = max(
            state.pressure_released, best_at_time.get(state.time, 0)
        )

    return best


@time_it
def part_a(input_: str):
    # Example: 1651.
    start, map_ = _parse(input_)
    return _solve([start], map_)


@time_it
def part_b(input_: str):
    # 26 minutes, elephants
    start, map_ = _parse(input_)
    # Example: 1707
    return _solve([start, start], map_)
