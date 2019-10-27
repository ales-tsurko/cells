from typing import NamedTuple


class New(NamedTuple):
    pass


class Open(NamedTuple):
    path: str


class Save(NamedTuple):
    pass


class SaveAs(NamedTuple):
    path: str
