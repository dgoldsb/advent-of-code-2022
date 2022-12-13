"""Solve day 13."""
from json import dumps, loads

from aoc.helpers import time_it


class EqualError(RuntimeError):
    """(Sub)packets are equal when one is expected to be bigger."""


class Packet:
    def __init__(self, packet_string: str):
        self.is_int = packet_string.isnumeric()
        self.packet_string = packet_string
        self.__deserialized = loads(self.packet_string)

    def wrap(self):
        return type(self)(dumps([loads(self.packet_string)]))

    def __getitem__(self, item):
        if isinstance(self.__deserialized, list):
            return Packet(dumps(self.__deserialized[item]))
        else:
            raise TypeError("Packet does not contain a list")

    def __len__(self):
        return len(loads(self.packet_string))

    def __int__(self):
        return int(self.packet_string)

    def __lt__(self, other):
        if self.is_int and other.is_int:
            if int(self) == int(other):
                raise EqualError()
            return int(self) < int(other)
        elif self.is_int:
            return self.wrap() < other
        elif other.is_int:
            return self < other.wrap()
        else:
            for idx in range(max(len(self), len(other))):
                if idx >= len(self) and idx >= len(other):
                    raise EqualError()
                if idx >= len(self):
                    return True
                elif idx >= len(other):
                    return False
                else:
                    try:
                        return self[idx] < other[idx]
                    except EqualError:
                        continue
            else:
                raise EqualError()


@time_it
def part_a(input_: str):
    result = 0
    for idx, line in enumerate(input_.split("\n\n")):
        first, second = line.split("\n")
        if Packet(first) < Packet(second):
            result += idx + 1
    return result


@time_it
def part_b(input_: str):
    dividers = [Packet("[[2]]"), Packet("[[6]]")]
    packets = [Packet(s) for s in input_.replace("\n\n", "\n").split("\n")]
    all_packets = list(sorted(packets + dividers))
    first, second = (all_packets.index(d) for d in dividers)
    return (first + 1) * (second + 1)
