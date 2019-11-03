from typing import NamedTuple


class New(NamedTuple):
    name: str


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


class RowRemove(NamedTuple):
    index: int


class CellAdd(NamedTuple):
    track_index: int
    name: str


class CellSelected(NamedTuple):
    track_index: int
    index: int


class CellEvaluate(NamedTuple):
    track_index: int
    index: int


class CellClicked(NamedTuple):
    index: int


class CellMove(NamedTuple):
    track_index: int
    index: int
    new_index: int


class CellRemove(NamedTuple):
    track_index: int
    index: int


class CellNameChanged(NamedTuple):
    track_index: int
    index: int
    name: str


class CellCodeChanged(NamedTuple):
    track_index: int
    index: int
    code: str
