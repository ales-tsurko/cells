import os
from dataclasses import dataclass
from typing import List

from dataclasses_json import dataclass_json
from cells import events
from cells.observation import Observation


@dataclass_json
@dataclass
class TrackModel:
    name: str


@dataclass_json
@dataclass
class DocumentModel:
    name: str
    tracks: List[TrackModel]


class Document(Observation, dict):
    def __init__(self, subject):
        dict.__init__(self)
        Observation.__init__(self, subject)

        self.saved = True
        self.path = None

        # main view events
        self.add_responder(events.view.main.FileNew, self.main_new_responder)
        self.add_responder(events.view.main.FileOpen, self.main_open_responder)
        self.add_responder(events.view.main.FileSave, self.main_save_responder)
        self.add_responder(events.view.main.FileSaveAs,
                           self.main_save_responder)
        self.add_responder(events.view.main.TrackNew,
                           self.main_track_new_responder)

        self.add_responder(events.track.Move, self.on_track_move)
        self.add_responder(events.track.Remove, self.on_track_remove)

    def main_new_responder(self, e):
        self.model = DocumentModel("New Document", [])
        self.notify(events.document.New(self))

    def main_open_responder(self, e):
        self.open(e.path)

    def main_save_responder(self, e):
        self.save(e.path)

    def main_track_new_responder(self, e):
        track = TrackModel("Track " + str(len(self.model.tracks) + 1))
        self.model.tracks.append(track)
        self.notify(events.document.Update(self))
        self.notify(events.track.New(track))

    def on_track_move(self, e):
        track = self.tracks.pop(e.index)
        self.model.tracks.insert(track, e.new_index)
        self.model.notify(events.document.Update(self))

    def on_track_remove(self, e):
        del self.tracks[e.index]
        self.notify(events.document.Update(self))

    def open(self, path):
        with open(path, "r") as f:
            try:
                self.model = DocumentModel.from_json(f.read())
                self.path = path
                self._update_name()
                self.saved = True
                self.notify(events.document.Open(self))
            except TypeError as e:
                print(e)
                self.notify(events.document.Error(self, "Can't open file"))

    def _update_name(self):
        base = os.path.basename(self.path)
        self.model.name, _ = os.path.splitext(base)

    def save(self, path):
        with open(path, "w+") as f:
            try:
                f.write(self.model.to_json())
                self.path = path
                self._update_name()
                self.saved = True
            except TypeError as e:
                print(e)
                self.notify(events.document.Error(self, "Can't save file"))
