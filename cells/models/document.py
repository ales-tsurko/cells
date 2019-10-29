from cells.observation import Observation
from cells import events


class Document(Observation, dict):
    def __init__(self, subject):
        dict.__init__(self)
        Observation.__init__(self, subject)

        self.saved = True
        self.name = "* New Document"

        self.add_responder(events.document.Open, self.on_open_responder)
        self.add_responder(events.document.Save, self.on_save_responder)

    def __setattr__(self, name, value):
        self.__dict__["saved"] = False
        super().__setattr__(name, value)
        self.notify(events.document.Update(self))

    def on_open_responder(self, e):
        self.open()

    def on_save_responder(self, e):
        self.save()

    def open(self):
        self.notify(events.document.Load(self))
        self.saved = True

    def save(self):
        self.saved = True

