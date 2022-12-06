"""Solve day 6."""
from functools import lru_cache

from aoc.helpers import time_it

PACK_LEN = 4
MESS_LEN = 14


class CircularBuffer:
    def __init__(self, size: int):
        self.__values = [None] * size
        self.__index = 0

    def put(self, value):
        self.__values[self.__index] = value
        self.__index = (self.__index + 1) % len(self.__values)

    def __len__(self):
        return len(self.__values)

    def __iter__(self):
        for _ in range(len(self.__values)):
            yield self.__values[self.__index]
            self.__index = (self.__index - 1 + len(self.__values)) % len(self.__values)


@lru_cache
def _all(input_: str):
    a_result, b_result = None, None

    buffer_packet = CircularBuffer(PACK_LEN)
    buffer_message = CircularBuffer(MESS_LEN)
    for i, char in enumerate(input_):
        buffer_packet.put(char)
        buffer_message.put(char)

        if (
            None not in (packet_set := set(buffer_packet))
            and len(packet_set) == PACK_LEN
            and a_result is None
        ):
            a_result = i + 1

        if (
            None not in (message_set := set(buffer_message))
            and len(message_set) == MESS_LEN
            and b_result is None
        ):
            b_result = i + 1
            break

    return a_result, b_result


@time_it
def part_a(input_: str):
    return _all(input_)[0]


@time_it
def part_b(input_: str):
    return _all(input_)[1]
