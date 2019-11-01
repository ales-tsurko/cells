from typing import NamedTuple


class NameChanged(NamedTuple):
    index: int
    name: str


class Remove(NamedTuple):
    index: int


class Select(NamedTuple):
    index: int


class Clicked(NamedTuple):
    index: int


class Move(NamedTuple):
    index: int
    new_index: int

class CellAdd(NamedTuple):
    track_index: int
    name: str

class CellSelect(NamedTuple):
    index: int


class CellNameChanged(NamedTuple):
    track_index: int
    index: int
    name: str
