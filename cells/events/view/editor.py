from typing import List, NamedTuple

from cells.model import TrackTemplateModel


class TrackRestartBackend(NamedTuple):
    templates: List[TrackTemplateModel]


class BackendRestartAll(NamedTuple):
    templates: List[TrackTemplateModel]
