from typing import NamedTuple

from cells.models.document import Document


class Load(NamedTuple):
    document: Document
