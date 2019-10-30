from typing import NamedTuple

from cells.models.document import Document


class New(NamedTuple):
    document: Document


class Open(NamedTuple):
    document: Document


class Save(NamedTuple):
    document: Document


class SaveAs(NamedTuple):
    document: Document


class Close(NamedTuple):
    document: Document


class Update(NamedTuple):
    document: Document


class Error(NamedTuple):
    document: Document
    message: str
