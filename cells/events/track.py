from typing import NamedTuple

from cells.models.document import Track


class New(NamedTuple):
    pass


class Rename(NamedTuple):
    index: int
    name: str


class Move(NamedTuple):
    index: int
    new_index: int


class Remove(NamedTuple):
    index: int
