import json
import os

from cells import events
from cells.observation import Observation


class Document(Observation, dict):
    def __init__(self, subject):
        dict.__init__(self)
        Observation.__init__(self, subject)

        self.saved = True
        self.name = "New Document"
        self.path = None
        self.tracks = []

        self.add_responder(events.document.Open, self.on_open_responder)
        self.add_responder(events.document.Save, self.on_save_responder)
        self.add_responder(events.document.SaveAs, self.on_save_as_responder)
        self.add_responder(events.track.New, self.on_new_track_responder)
        self.add_responder(events.track.Move, self.on_track_move)
        self.add_responder(events.track.Remove, self.on_track_remove)

    def __setattr__(self, name, value):
        self.__dict__["saved"] = False
        if name != "subject":
            self.__setitem__(name, value)
        super().__setattr__(name, value)
        self.notify(events.document.Update(self))

    def on_open_responder(self, e):
        self.open(e.path)

    def on_save_responder(self, e):
        self.save()

    def on_save_as_responder(self, e):
        self.save_as(e.path)

    def on_new_track_responder(self, e):
        track = Track(self.subject, "Track " + str(len(self.tracks) + 1))
        self.tracks.append(track)
        self.notify(events.document.Update(self))

    def on_track_move(self, e):
        track = self.tracks.pop(e.index)
        self.tracks.insert(track, e.new_index)
        self.notify(events.document.Update(self))

    def on_track_remove(self, e):
        del self.tracks[e.index]
        self.notify(events.document.Update(self))

    def open(self, path):
        with open(path, "r") as f:
            try:
                self.__dict__.update(json.load(f))
                self.path = path
                self._update_name()
                self.saved = True
                self.notify(events.document.Load(self))
            except json.decoder.JSONDecodeError:
                self.notify(events.document.Error(self, "Can't open file"))

    def save(self):
        with open(self.path, "w+") as f:
            json.dump(dict(self), f)
            self.saved = True

    def _update_name(self):
        base = os.path.basename(self.path)
        self.name, _ = os.path.splitext(base)

    def save_as(self, path):
        with open(path, "w+") as f:
            try:
                json.dump(dict(self), f)
                self.path = path
                self._update_name()
                self.saved = True
            except json.decoder.JSONDecodeError:
                self.notify(events.document.Error(self, "Can't save file"))


class Track(Observation, dict):
    def __init__(self, subject, name):
        Observation.__init__(self, subject)
        dict.__init__(self)
        self.name = name

    def __setattr__(self, name, value):
        if name != "subject":
            self.__setitem__(name, value)
        super().__setattr__(name, value)

