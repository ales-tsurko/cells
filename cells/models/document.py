import json

from cells import events
from cells.observation import Observation


class Document(Observation, dict):
    def __init__(self, subject):
        dict.__init__(self)
        Observation.__init__(self, subject)

        self.saved = True
        self.name = "* New Document"
        self.path = None

        self.add_responder(events.document.Open, self.on_open_responder)
        self.add_responder(events.document.Save, self.on_save_responder)
        self.add_responder(events.document.SaveAs, self.on_save_as_responder)

    def __setattr__(self, name, value):
        self.__dict__["saved"] = False
        super().__setattr__(name, value)
        self.notify(events.document.Update(self))

    def on_open_responder(self, e):
        self.open(e.path)

    def on_save_responder(self, e):
        self.save()

    def on_save_as_responder(self, e):
        self.save_as(e.path)

    def open(self, path):
        with open(path, "w+") as f:
            self.update(json.load(f))
            self.path = path
            self.notify(events.document.Load(self))

    def save(self):
        with open(self.path, "w+") as f:
            f.write(json.dumps(dict(self)))
            self.saved = True

    def save_as(self, path):
        with open(path, "w+") as f:
            f.write(json.dumps(dict(self)))
            self.saved = True
            self.path = path
