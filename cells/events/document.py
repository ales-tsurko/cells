from typing import NamedTuple

from cells.models.document import Document


class New(NamedTuple):
    pass


class Open(NamedTuple):
    path: str


class Save(NamedTuple):
    pass


class SaveAs(NamedTuple):
    path: str


class Load(NamedTuple):
    document: Document


class Close(NamedTuple):
    document: Document


class Update(NamedTuple):
    document: Document


class Error(NamedTuple):
    document: Document
    message: str
