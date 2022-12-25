"""Solve day 25."""
from aoc.helpers import time_it


class Snafu:
    def __init__(self, value: str):
        self.value = value

    @staticmethod
    def __digit_to_int(digit: str) -> int:
        match digit:
            case "=":
                return -2
            case "-":
                return -1
            case "0":
                return 0
            case "1":
                return 1
            case "2":
                return 2
            case _:
                raise RuntimeError(f"{digit=} is invalid!")

    @staticmethod
    def __int_to_digit(number: int) -> str:
        match number:
            case -2:
                return "="
            case -1:
                return "-"
            case 0:
                return "0"
            case 1:
                return "1"
            case 2:
                return "2"
            case _:
                raise RuntimeError(f"{number=} is invalid!")

    def __add__(self, other) -> "Snafu":
        self_value = str(self)
        other_value = str(other)
        result_value = ""
        remainder_value = 0
        while self_value or other_value:
            try:
                self_int = self.__digit_to_int(self_value[-1])
            except IndexError:
                self_int = 0
            try:
                other_int = self.__digit_to_int(other_value[-1])
            except IndexError:
                other_int = 0

            sum_ = self_int + other_int + remainder_value
            remainder_value = 0
            while sum_ > 2:
                sum_ -= 5
                remainder_value += 1
            while sum_ < -2:
                sum_ += 5
                remainder_value -= 1

            new_digit = self.__int_to_digit(sum_)
            result_value += new_digit

            self_value = self_value[:-1]
            other_value = other_value[:-1]
        if remainder_value:
            new_digit = self.__int_to_digit(remainder_value)
            result_value += new_digit
        result_value = result_value[::-1]
        return Snafu(result_value)

    def __str__(self) -> str:
        return self.value

    def __eq__(self, other) -> bool:
        return self.value == other.value

    def __repr__(self) -> str:
        return f"<{str(self)}>"

    def __int__(self) -> int:
        mult = 1
        value = self.value
        result = 0
        while value:
            char = value[-1]
            value = value[:-1]
            mult *= 5
            match char:
                case "=":
                    result += -2 * mult
                case "-":
                    result += -1 * mult
                case "0":
                    result += 0 * mult
                case "1":
                    result += 1 * mult
                case "2":
                    result += 2 * mult
        return result

    @classmethod
    def from_int(cls, number: int) -> "Snafu":
        parts = []
        tail = ""
        while number:
            remainder = number % 5
            number = number // 5
            match remainder:
                case 0:
                    parts.append(cls("0" + tail))
                case 1:
                    parts.append(cls("1" + tail))
                case 2:
                    parts.append(cls("2" + tail))
                case 3:
                    parts.append(cls("1=" + tail))
                case 4:
                    parts.append(cls("1-" + tail))
            tail += "0"
        return sum(parts, start=Snafu("0"))


# Some tests.
def _test_addition(a, b, c):
    try:
        assert a + b == c
    except AssertionError:
        raise AssertionError(f"{a} + {b} and {c} are not equal!")


for a_, b_, c_ in [
    ("1", "1", "2"),
    ("2", "1", "1="),
]:
    _test_addition(Snafu(a_), Snafu(b_), Snafu(c_))


def _test_conversion(a, b):
    try:
        assert a == b
    except AssertionError:
        raise AssertionError(f"{a} and {b} are not equal!")


for a_, b_ in [
    ("1=-0-2", 1747),
    ("12111", 906),
    ("2=0=", 198),
    ("21", 11),
    ("2=01", 201),
    ("111", 31),
    ("20012", 1257),
]:
    _test_conversion(Snafu(a_), Snafu.from_int(b_))


@time_it
def part_a(input_: str):
    return sum((Snafu(s) for s in input_.splitlines() if s), start=Snafu("0"))
