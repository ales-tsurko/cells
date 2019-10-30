from typing import NamedTuple


class NameChanged(NamedTuple):
    index: int
    name: str


class Remove(NamedTuple):
    index: int
