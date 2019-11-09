import glob
import os
from dataclasses import dataclass, field
from time import time
from typing import List
from uuid import uuid4

from appdirs import user_data_dir
from cells import events
from cells.observation import Observation
from cells.settings import ApplicationInfo
from dataclasses_json import dataclass_json

TRACK_TEMPLATE_EXT = ".ctt"


@dataclass_json
@dataclass
class CellModel:
    name: str = field(default="")
    code: str = field(default="")


@dataclass_json
@dataclass
class TrackTemplateModel:
    backend_name: str = field(default="Default")
    setup_code: str = field(default="")
    run_command: str = field(default="")
    command_prompt: str = field(default="")
    description: str = field(default="")
    editor_mode: str = field(default="plain text")
    path: str = field(default="")

    def __repr__(self):
        return f"Path: {self.path}\n" +\
               f"Backend Name: {self.backend_name}\n" +\
               f"Run Command: {self.run_command}\n" +\
               f"Command Prompt: {self.command_prompt}\n" +\
               f"Editor Mode: {self.editor_mode}\n" +\
               f"Description: {self.description}\n" +\
               f"Setup Code: {self.setup_code}"


@dataclass_json
@dataclass
class TrackModel:
    name: str
    cells: List[CellModel]
    template: TrackTemplateModel = field(default=TrackTemplateModel())


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

        self.add_responder(events.view.main.FileOpen, self.main_open_responder)
        self.add_responder(events.view.main.FileSave, self.main_save_responder)
        self.add_responder(events.view.main.FileSaveAs,
                           self.main_save_responder)
        self.add_responder(events.view.track.New, self.track_new_responder)
        self.add_responder(events.view.track.CellAdd, self.cell_add_responder)
        self.add_responder(events.view.track.CellRemove,
                           self.cell_remove_responder)
        self.add_responder(events.view.track.NameChanged,
                           self.track_name_changed_responder)
        self.add_responder(events.view.track.TemplateUpdated,
                           self.track_template_updated_responder)
        self.add_responder(events.view.track.CellNameChanged,
                           self.cell_name_changed_responder)
        self.add_responder(events.view.track.CellCodeChanged,
                           self.cell_code_changed_responder)
        self.add_responder(events.view.track.Remove,
                           self.track_remove_responder)
        self.add_responder(events.view.track.Move, self.track_move_responder)
        self.add_responder(events.view.track.CellMove,
                           self.cell_move_responder)

    def main_open_responder(self, e):
        self.open(e.path)

    def main_save_responder(self, e):
        self.save(e.path)

    @notify_update
    def track_new_responder(self, e):
        track = TrackModel(e.name, [])
        self.model.tracks.append(track)
        self.notify(events.track.New(track))

    @notify_update
    def cell_add_responder(self, e):
        cell = CellModel(e.name, "")
        self.model.tracks[e.track_index].cells.append(cell)

    @notify_update
    def cell_remove_responder(self, e):
        del self.model.tracks[e.track_index].cells[e.index]

    @notify_update
    def track_name_changed_responder(self, e):
        self.model.tracks[e.index].name = e.name

    @notify_update
    def track_template_updated_responder(self, e):
        track = self.model.tracks[e.index]
        track.template = e.template

    @notify_update
    def cell_name_changed_responder(self, e):
        self.model.tracks[e.track_index].cells[e.index].name = e.name

    @notify_update
    def cell_code_changed_responder(self, e):
        if len(self.model.tracks) < e.track_index + 1:
            return
        track = self.model.tracks[e.track_index]
        cell = track.cells[e.index]
        cell.code = e.code

    @notify_update
    def track_move_responder(self, e):
        track = self.model.tracks.pop(e.index)
        self.model.tracks.insert(e.new_index, track)

    @notify_update
    def cell_move_responder(self, e):
        track = self.model.tracks[e.track_index]
        cell = track.cells.pop(e.index)
        track.cells.insert(e.new_index, cell)

    @notify_update
    def track_remove_responder(self, e):
        del self.model.tracks[e.index]

    def open(self, path):
        with open(path, "r") as f:
            try:
                self.update_name_from_path(path)
                self.model = DocumentModel.from_json(f.read())
                self.model.path = path
                self.notify(events.document.Open(self.model))
            except TypeError as e:
                print(e)
                self.notify(
                    events.document.Error(self.model, "Can't open file"))

    def save(self, path):
        with open(path, "w+") as f:
            try:
                self.model.path = path
                self.update_name_from_path(path)
                f.write(self.model.to_json())
            except TypeError as e:
                print(e)
                self.notify(
                    events.document.Error(self.model, "Can't save file"))

    def update_name_from_path(self, path):
        base = os.path.basename(path)
        self.model.name, _ = os.path.splitext(base)


class TrackTemplateManager(Observation):
    def __init__(self, document, subject):
        super().__init__(subject)

        self.templates = []
        self.document = document

        self.read_dir(standard_track_template_dir())

        self.add_responder(events.view.track.SaveAsTemplate,
                           self.track_save_as_template_responder)

    def track_save_as_template_responder(self, e):
        self.save(e.template, self.new_template_path())

    def read_dir(self, path):
        self.templates = [
            self.read(p) for p in sorted(
                glob.glob(os.path.join(path, "*" + TRACK_TEMPLATE_EXT)))
        ]

    def read(self, path):
        with open(path, "r") as f:
            try:
                template = TrackTemplateModel.from_json(f.read())
                template.path = path

                return template
            except TypeError as e:
                print(e)
                self.notify(
                    events.document.Error(
                        self.document, f"Can't read track template {path}."))

    def save(self, template, path, notify=True):
        with open(path, "w+") as f:
            try:
                template.path = path
                f.write(template.to_json())
                self.templates.append(template)

                if notify:
                    self.notify(events.track.TrackTemplateSaved(template))
            except TypeError as e:
                print(e)
                self.notify(
                    events.document.Error(self.document,
                                          "Can't save track template file."))

    def delete_at(self, index):
        template = self.templates.pop(index)
        try:
            os.remove(template.path)
        except FileNotFoundError as e:
            print(e)
            self.notify(
                events.document.Error(
                    self.document,
                    f"Can't find track template file at path {template.path}.")
            )

    def new_template_path(self):
        file_name = str(int(time() * 10)) + "-" + \
            str(uuid4()) + TRACK_TEMPLATE_EXT

        return os.path.join(standard_track_template_dir(), file_name)


def standard_track_template_dir():
    data_dir = user_data_dir(ApplicationInfo.name, ApplicationInfo.author)
    templates_dir = os.path.join(data_dir, "track_templates")
    not os.path.exists(templates_dir) and os.makedirs(templates_dir)

    return templates_dir
