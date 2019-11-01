import os
from dataclasses import dataclass, field
from typing import List

from dataclasses_json import dataclass_json
from cells import events
from cells.observation import Observation


@dataclass_json
@dataclass
class Cell:
    name: str = field(default="")
    code: str = field(default="")


@dataclass_json
@dataclass
class TrackModel:
    name: str
    cells: List[Cell]


@dataclass_json
@dataclass
class DocumentModel:
    name: str
    tracks: List[TrackModel]
    path: str


def notify_update(method):
    def inner(instance, *args, **kwargs):
        method(instance, *args, **kwargs)
        instance.notify(events.document.Update(instance.model))
    return inner


class Document(Observation, dict):
    def __init__(self, subject):
        dict.__init__(self)
        Observation.__init__(self, subject)

        self.model = DocumentModel("New Document", [], None)
        self.notify(events.document.New)

        # main view events
        self.add_responder(events.view.main.FileOpen, self.main_open_responder)
        self.add_responder(events.view.main.FileSave, self.main_save_responder)
        self.add_responder(events.view.main.FileSaveAs,
                           self.main_save_responder)
        self.add_responder(events.view.main.TrackNew,
                           self.main_track_new_responder)

        self.add_responder(events.view.track.NameChanged,
                           self.track_name_changed_responder)
        self.add_responder(events.view.track.Remove,
                           self.track_remove_responder)

        self.add_responder(events.view.track.Move, self.track_move_responder)

    def main_open_responder(self, e):
        self.open(e.path)

    def main_save_responder(self, e):
        self.save(e.path)

    def main_track_new_responder(self, e):
        name = "Track " + str(len(self.model.tracks) + 1)
        track = TrackModel(name, [Cell()])
        self.model.tracks.append(track)
        self.notify(events.track.New(track))

    @notify_update
    def track_name_changed_responder(self, e):
        self.model.tracks[e.index].name = e.name

    @notify_update
    def track_move_responder(self, e):
        track = self.model.tracks.pop(e.index)
        self.model.tracks.insert(e.new_index, track)

    @notify_update
    def track_remove_responder(self, e):
        del self.model.tracks[e.index]

    def open(self, path):
        with open(path, "r") as f:
            try:
                self.model.path = path
                self.update_name()
                self.model = DocumentModel.from_json(f.read())
                self.notify(events.document.Open(self.model))
            except TypeError as e:
                print(e)
                self.notify(events.document.Error(self.model,
                                                  "Can't open file"))

    def save(self, path):
        with open(path, "w+") as f:
            try:
                self.model.path = path
                self.update_name()
                f.write(self.model.to_json())
            except TypeError as e:
                print(e)
                self.notify(events.document.Error(self.model,
                                                  "Can't save file"))

    def update_name(self):
        base = os.path.basename(self.model.path)
        self.model.name, _ = os.path.splitext(base)
