"""Solve day 20."""
from dataclasses import dataclass

from aoc.helpers import time_it


@dataclass
class LinkedListItem:
    value: int
    previous: "LinkedListItem" = None
    next: "LinkedListItem" = None

    def __getitem__(self, item):
        current = self
        for _ in range(item):
            current = current.next
        return current

    def __len__(self):
        return len(list(iter(self)))

    def __iter__(self):
        current = self
        while True:
            yield current
            current = current.next
            if current is self:
                return

    def find(self, value) -> "LinkedListItem":
        for candidate in iter(self):
            if candidate.value == value:
                return candidate
        else:
            raise ValueError(f"Value {value} not found")

    def mix(self):
        # Zero does not move.
        if self.value == 0:
            return

        # Iterate forward or backward. Backward requires an extra iteration because
        # we want to select the first of the pair in which we want to wedge between.
        is_negative = self.value < 0
        start_wedge = self
        for _ in range(abs(self.value) + is_negative):
            start_wedge = start_wedge.previous if is_negative else start_wedge.next

        # Cycle does not move.
        if start_wedge is self:
            return

        # Stitch up the old spot.
        self.previous.next = self.next
        self.next.previous = self.previous

        # Stitch into the new spot.
        end_wedge = start_wedge.next
        start_wedge.next = self
        end_wedge.previous = self

        # u[date own references
        self.previous = start_wedge
        self.next = end_wedge


def _parse(input_: str) -> list[LinkedListItem]:
    iterator = iter(input_.split("\n"))
    head = LinkedListItem(int(next(iterator)))
    all_items = [head]
    last = head
    for ri in iterator:
        new = LinkedListItem(int(ri))
        last.next = new
        new.previous = last
        last = new
        all_items.append(new)
    else:
        last.next = head
        head.previous = last
    return all_items


@time_it
def part_a(input_: str):
    all_items = _parse(input_)

    # Sequence is important in mixing.
    for item in all_items:
        item.mix()

    zero = all_items[0].find(0)

    # Check that we lost nothing.
    assert len(zero) == len(all_items)

    # TODO: not -18746, 2342 too low, so answer should be positive!
    return (
        zero[1000].value +
        zero[2000].value +
        zero[3000].value
    )


@time_it
def part_b(input_: str):
    return None
