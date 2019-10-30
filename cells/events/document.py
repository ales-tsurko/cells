from typing import NamedTuple

from cells.models.document import DocumentModel


class New(NamedTuple):
    document: DocumentModel


class Open(NamedTuple):
    document: DocumentModel


class Save(NamedTuple):
    document: DocumentModel


class SaveAs(NamedTuple):
    document: DocumentModel


class Close(NamedTuple):
    document: DocumentModel


class Update(NamedTuple):
    document: DocumentModel


class Error(NamedTuple):
    document: DocumentModel
    message: str
