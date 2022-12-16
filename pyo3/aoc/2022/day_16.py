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


@dataclass(frozen=True)
class Valve:
    name: str
    value: int


@dataclass(frozen=True)
class State:
    location: Valve
    active: set[Valve]

    time: int = 0
    pressure_released: int = 0

    def __lt__(self, other):
        # For the heap, invert.
        return self.pressure_released > other.pressure_released

    def __str__(self):
        return str(
            (
                self.location.name,
                tuple(sorted((a.name for a in self.active))),
                self.time,
                self.pressure_released,
            )
        )

    def __hash__(self):
        return hash(str(self))

    def _move_time(self, location: Valve, active: set[Valve]) -> "State":
        return State(
            location=location,
            time=self.time + 1,
            pressure_released=self.pressure_released + sum((v.value for v in active)),
            active=active,
        )

    def open(self) -> "State":
        active = copy(self.active)
        active.add(self.location)
        return self._move_time(self.location, active)

    def move(self, valve: Valve) -> "State":
        return self._move_time(valve, self.active)

    def can_reach(self, target: int, bound: int) -> bool:
        steps_remaining = STEPS - self.time
        gap = target - self.pressure_released
        return steps_remaining * bound > gap


def _parse(input_: str) -> tuple[Valve, dict[Valve, list[Valve]]]:
    _valves = {}
    _map = {}
    for result in REGEX.findall(input_):
        valve = Valve(result[0], int(result[1]))
        _valves[valve.name] = valve
        _map[valve.name] = list(result[2].split(", "))
    return _valves[START], {
        _valves[k]: [_valves[w] for w in v] for k, v in _map.items()
    }


def _solve(start: Valve, valve_map: dict[Valve, list[Valve]]):
    best = 100
    heap = [State(start, set())]
    bound = sum((v.value for v in valve_map.keys()))

    visited = set()

    while heap:
        state = heapq.heappop(heap)

        # Pruning.
        if state.time >= STEPS or state in visited or not state.can_reach(best, bound):
            continue

        visited.add(state)

        if state.location not in state.active and state.location.value:
            heapq.heappush(heap, state.open())

        for next_valve in valve_map[state.location]:
            heapq.heappush(heap, state.move(next_valve))

        best = max(state.pressure_released, best)

    return best


@time_it
def part_a(input_: str):
    # Example: 1651.
    return _solve(*_parse(input_))


@time_it
def part_b(input_: str):
    # 26 minutes, elephants
    return None
