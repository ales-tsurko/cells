import os

import toml

from appdirs import user_config_dir
from cells import events
from cells.observation import Observation


class ApplicationInfo:
    name = "Cells"
    author = "Ales Tsurko"
    version = "0.1.0"


class Settings(Observation, dict):
    def __init__(self, subject):
        dict.__init__(self)
        Observation.__init__(self, subject)

        self.path = self._init_path()
        self.open()

        # self.add_responder(events.app.Quit, self.app_quit_responder)

        self.setdefault("editor", {})
        self['editor'].setdefault("theme", "Gruvbox")
        self['editor'].setdefault("keybindings", "Sublime")

        self.notify(events.settings.Load(self))

    def _init_path(self):
        settings_dir = user_config_dir(ApplicationInfo.name,
                                       ApplicationInfo.author)

        if not os.path.exists(settings_dir):
            os.makedirs(settings_dir)

        return os.path.join(settings_dir, "settings.toml")

    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        self.notify(events.settings.Update(self))

    # def app_quit_responder(self, e):
    #     self.save()

    def open(self):
        with open(self.path, "r") as f:
            self.update(toml.load(f))

    def save(self):
        with open(self.path, "w+") as f:
            toml.dump(dict(self), f)
            self.notify(events.settings.Save(self))
