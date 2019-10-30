from typing import NamedTuple

from cells.models.document import TrackModel


class New(NamedTuple):
    track: TrackModel


class Rename(NamedTuple):
    index: int
    name: str


class Move(NamedTuple):
    index: int
    new_index: int


class Remove(NamedTuple):
    index: int
