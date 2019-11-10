from typing import NamedTuple

from cells.model import TrackTemplateModel


class New(NamedTuple):
    name: str
    template: TrackTemplateModel


class NameChanged(NamedTuple):
    index: int
    name: str


class TemplateUpdated(NamedTuple):
    index: int
    template: TrackTemplateModel


class SaveAsTemplate(NamedTuple):
    template: TrackTemplateModel


class WillRestart(NamedTuple):
    template: TrackTemplateModel


class InterpreterRestart(NamedTuple):
    track_index: int
    setup_code: str


class Deserialized(NamedTuple):
    track_index: int
    template: TrackTemplateModel


class Remove(NamedTuple):
    index: int
    template: TrackTemplateModel


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
    template: TrackTemplateModel
    code: str


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
