from typing import NamedTuple

from cells.model import TrackModel, TrackTemplateModel


class New(NamedTuple):
    track: TrackModel


class TrackTemplateSaved(NamedTuple):
    template: TrackTemplateModel
