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

        self.model = DocumentModel("New Document", [])

        self.add_responder(events.document.Open, self.on_open_responder)
        self.add_responder(events.document.Save, self.on_save_responder)
        self.add_responder(events.document.SaveAs, self.on_save_as_responder)
        self.add_responder(events.track.New, self.on_new_track_responder)
        self.add_responder(events.track.Move, self.on_track_move)
        self.add_responder(events.track.Remove, self.on_track_remove)

    def on_open_responder(self, e):
        self.open(e.path)

    def on_save_responder(self, e):
        self.save()

    def on_save_as_responder(self, e):
        self.save_as(e.path)

    def on_new_track_responder(self, e):
        track = TrackModel("Track " + str(len(self.model.tracks) + 1))
        self.model.tracks.append(track)
        self.notify(events.document.Update(self))

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
                self.notify(events.document.Load(self))
            except TypeError as e:
                print(e)
                self.notify(events.document.Error(self, "Can't open file"))

    def save(self):
        with open(self.path, "w+") as f:
            f.write(self.model.to_json())
            self.saved = True

    def _update_name(self):
        base = os.path.basename(self.path)
        self.model.name, _ = os.path.splitext(base)

    def save_as(self, path):
        with open(path, "w+") as f:
            try:
                f.write(self.model.to_json())
                self.path = path
                self._update_name()
                self.saved = True
            except TypeError as e:
                print(e)
                self.notify(events.document.Error(self, "Can't save file"))
