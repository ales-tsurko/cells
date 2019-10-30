from typing import NamedTuple


class FileOpen(NamedTuple):
    path: str


class FileSave(NamedTuple):
    path: str


class FileSaveAs(NamedTuple):
    path: str


class FileNew(NamedTuple):
    pass


class TrackNew(NamedTuple):
    pass


class Close(NamedTuple):
    pass
