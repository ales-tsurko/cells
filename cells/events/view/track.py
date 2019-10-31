from typing import NamedTuple


class NameChanged(NamedTuple):
    index: int
    name: str


class WillRemove(NamedTuple):
    index: int


class Remove(NamedTuple):
    index: int


class Select(NamedTuple):
    index: int


class Move(NamedTuple):
    index: int
    new_index: int
