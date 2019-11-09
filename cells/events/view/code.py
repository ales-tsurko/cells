from typing import NamedTuple

from cells.model import TrackTemplateModel


class Evaluate(NamedTuple):
    template: TrackTemplateModel
    code: str
