from cells.observation import Observation
from cells import events


class Document(Observation, dict):
    def __init__(self, subject):
        dict.__init__(self)
        Observation.__init__(self, subject)

        self.saved = True

        self.add_responder(events.document.Open, self.on_open_responder)
        self.add_responder(events.document.Save, self.on_save_responder)

    def __setattr__(self, name, value):
        #  self.saved = False
        super().__setattr__(name, value)
        self.notify(events.document.Change(self))

    def on_save_responder(self, e):
        self.save()

    def save(self):
        self.saved = True

    def on_open_responder(self, e):
        self.notify(events.document.Load(self))
        self.saved = True
