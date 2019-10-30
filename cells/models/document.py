import os
from dataclasses import dataclass
from typing import List

from dataclasses_json import dataclass_json
from cells import events
from cells.observation import Observation


DUMMY_TRACK_NAME = "IMADUMMYTRACKDONTEVENTTRYTOUSETHISNAMEFORYOURTRACKSYOUWILLLOSTTHEM"


@dataclass_json
@dataclass
class TrackModel:
    name: str


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

        # main view events
        self.add_responder(events.view.main.FileNew, self.main_new_responder)
        self.add_responder(events.view.main.FileOpen, self.main_open_responder)
        self.add_responder(events.view.main.FileSave, self.main_save_responder)
        self.add_responder(events.view.main.FileSaveAs,
                           self.main_save_responder)
        self.add_responder(events.view.main.TrackNew,
                           self.main_track_new_responder)

        self.add_responder(events.view.track.NameChanged,
                           self.track_name_changed_responder)
        self.add_responder(events.view.track.Remove, self.track_remove_responder)

        self.add_responder(events.track.Move, self.on_track_move)

    def main_new_responder(self, e):
        self.model = DocumentModel("New Document", [], None)
        self.notify(events.document.New(self.model))

    def main_open_responder(self, e):
        self.open(e.path)

    def main_save_responder(self, e):
        self.save(e.path)

    def main_track_new_responder(self, e):
        name = "Track " + str(len(self.model.tracks) + 1)
        track = TrackModel(name)
        self.model.tracks.append(track)
        self.notify(events.track.New(track))

    @notify_update
    def track_name_changed_responder(self, e):
        self.model.tracks[e.index].name = e.name

    @notify_update
    def on_track_move(self, e):
        track = self.tracks.pop(e.index)
        self.model.tracks.insert(track, e.new_index)

    @notify_update
    def track_remove_responder(self, e):
        dummy = TrackModel(DUMMY_TRACK_NAME)
        self.model.tracks[e.index] = dummy

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
