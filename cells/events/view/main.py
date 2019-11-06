from typing import NamedTuple


class FileOpen(NamedTuple):
    path: str


class FileSave(NamedTuple):
    path: str


class FileSaveAs(NamedTuple):
    path: str


class FileNew(NamedTuple):
    pass


class TrackSetup(NamedTuple):
    pass


class TrackNew(NamedTuple):
    pass


class TrackEditName(NamedTuple):
    pass


class TrackRemove(NamedTuple):
    pass


class TrackSelectLeft(NamedTuple):
    pass


class TrackSelectRight(NamedTuple):
    pass


class TrackMoveLeft(NamedTuple):
    pass


class TrackMoveRight(NamedTuple):
    pass


class RowAdd(NamedTuple):
    pass


class RowRemove(NamedTuple):
    pass


class RowSelectUp(NamedTuple):
    pass


class RowSelectDown(NamedTuple):
    pass


class RowMoveUp(NamedTuple):
    pass


class RowMoveDown(NamedTuple):
    pass


class RowEvaluate(NamedTuple):
    pass


class RowCopy(NamedTuple):
    pass


class RowCut(NamedTuple):
    pass


class RowPaste(NamedTuple):
    pass


class CellEvaluate(NamedTuple):
    pass


class CellClear(NamedTuple):
    pass


class CellEdit(NamedTuple):
    pass


class CellEditName(NamedTuple):
    pass


class CellCopy(NamedTuple):
    pass


class CellCut(NamedTuple):
    pass


class CellPaste(NamedTuple):
    pass


class ConsoleClear(NamedTuple):
    pass


class Close(NamedTuple):
    pass
