from typing import NamedTuple
from rx.subject import Subject
from cells.observer import Observer


class AEvent(NamedTuple):
    number: int


class BEvent(NamedTuple):
    number: int


class AClass(Observer):
    def __init__(self, subject):
        super().__init__(subject)

        self.number = 0
        self.add_responder(AEvent, self.on_test_event)

    def on_test_event(self, event):
        self.number = event.number


def test_observer():
    subject = Subject()

    test_obj = AClass(subject)

    subject.on_next(BEvent(3))

    assert test_obj.number == 0

    subject.on_next(AEvent(3))

    assert test_obj.number == 3
