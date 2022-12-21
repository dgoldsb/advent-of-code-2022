"""Solve day 21."""
from dataclasses import dataclass
from typing import Any

from aoc.helpers import time_it


@dataclass
class Node:
    name: str
    operator: str
    left_child: Any
    right_child: Any

    @property
    def linked(self):
        # Quick litmus test.
        return not isinstance(self.left_child, str)

    def __bool__(self):
        return float(self.left_child) == float(self.right_child)

    def __gt__(self, other):
        return float(self) > float(other)

    def __int__(self):
        return int(float(self))

    def __float__(self):
        if self.operator == "+":
            return float(self.left_child) + float(self.right_child)
        elif self.operator == "-":
            return float(self.left_child) - float(self.right_child)
        elif self.operator == "*":
            return float(self.left_child) * float(self.right_child)
        elif self.operator == "/":
            return float(self.left_child) / float(self.right_child)


def _link_node(node: Node, node_dict: dict[str, Node | int]):
    left = node_dict[node.left_child]
    right = node_dict[node.right_child]
    node.left_child = left
    node.right_child = right

    if isinstance(left, Node) and not left.linked:
        _link_node(left, node_dict)

    if isinstance(right, Node) and not right.linked:
        _link_node(right, node_dict)


def _parse(input_: str) -> tuple[Node, Node]:
    name_node_dict: dict[str, Node | float] = {}
    for line in input_.splitlines():
        name, eq = line.split(": ")
        try:
            left, operator, right = eq.split(" ")
            name_node_dict[name] = Node(name, operator, left, right)
        except Exception:
            name_node_dict[name] = float(eq)

    # For part 2.
    name_node_dict["humn"] = Node("humn", "+", name_node_dict["humn"], 0)
    _link_node(name_node_dict["root"], name_node_dict)

    return name_node_dict["root"], name_node_dict["humn"]


@time_it
def part_a(input_: str):
    root, _ = _parse(input_)
    return int(root)


@time_it
def part_b(input_: str):
    root, human = _parse(input_)
    min_, max_ = 0, 1000_000_000_000_000_000

    while True:
        human.left_child = (min_ + max_) // 2
        if root:
            return human.left_child
        elif root.left_child > root.right_child:
            min_ = human.left_child
        else:
            max_ = human.left_child
