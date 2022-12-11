"""Solve day 11."""
import re

from aoc.helpers import time_it


class Monkey:
    REGEX = re.compile(
        "Monkey\s(\d)\D+([\d, ]+)\D+([\+\*])\s(old|\d+)\D+(\d+)\D+(\d)\D+(\d)"
    )

    def __init__(self, id_, multiply: bool, second: int | None, mod: int):
        self.id = id_
        self.items: list[int] = []
        self.inspect_count = 0
        self.__multiply = multiply
        self.__second = second
        self.mod = mod
        self.worry_mod = None

        self.__monkey_true: Monkey = None  # type: ignore
        self.__monkey_false: Monkey = None  # type: ignore

    def set_monkeys(self, monkey_true, monkey_false):
        self.__monkey_true = monkey_true
        self.__monkey_false = monkey_false

    def do_turn(self):
        while self.items:
            item = self.items.pop(0)
            self.inspect_count += 1

            match (self.__multiply, self.__second):
                case True, None:
                    item *= item
                case False, None:
                    item += item
                case True, second:
                    item *= second
                case False, second:
                    item += second

            if self.worry_mod is None:
                item = item // 3
            else:
                item %= self.worry_mod

            if (item % self.mod) == 0:
                self.__monkey_true.items.append(item)
            else:
                self.__monkey_false.items.append(item)

    @classmethod
    def do_round(cls, monkeys: list["Monkey"]):
        for monkey in monkeys:
            monkey.do_turn()

    @classmethod
    def from_input(cls, input_: str, is_a: bool) -> list["Monkey"]:
        results = cls.REGEX.findall(input_)
        monkeys = []
        links = []
        for result in results:
            monkey = Monkey(
                id_=result[0],
                multiply=result[2] == "*",
                second=None if result[3] == "old" else int(result[3]),
                mod=int(result[4]),
            )
            monkey.items = [int(i) for i in result[1].split(", ")]
            monkeys.append(monkey)
            links.append((int(result[5]), int(result[6])))

        for i, link in enumerate(links):
            monkeys[i].set_monkeys(monkeys[link[0]], monkeys[link[1]])

        if not is_a:
            all_mods = list(m.mod for m in monkeys)
            max_mod = max(all_mods)
            worry_mod = max_mod
            while True:
                if all(worry_mod % m == 0 for m in all_mods):
                    break
                worry_mod += max_mod

            for monkey in monkeys:
                monkey.worry_mod = worry_mod
        return monkeys

    @classmethod
    def business(cls, monkeys: list["Monkey"]):
        activities = sorted([m.inspect_count for m in monkeys], reverse=True)
        return activities[0] * activities[1]


@time_it
def part_a(input_: str):
    monkeys = Monkey.from_input(input_, True)
    for _ in range(20):
        Monkey.do_round(monkeys)
    return Monkey.business(monkeys)


@time_it
def part_b(input_: str):
    monkeys = Monkey.from_input(input_, False)
    for _ in range(10**4):
        Monkey.do_round(monkeys)

    return Monkey.business(monkeys)
