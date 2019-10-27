from typing import NamedTuple


class New(NamedTuple):
    pass


class Open(NamedTuple):
    path: str


class Save(NamedTuple):
    path: str


class Duplicate(NamedTuple):
    path: str
