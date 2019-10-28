from typing import NamedTuple
from cells.settings import Settings


class Load(NamedTuple):
    settings: Settings


class Save(NamedTuple):
    settings: Settings


class Update(NamedTuple):
    settings: Settings
