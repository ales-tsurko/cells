from rx import operators as op


class Observation:
    def __init__(self, subject):
        self.subject = subject
        self._disposables = []

    def add_responder(self, event_type, responder):
        unregister = self.subject.pipe(
            op.filter(lambda e: isinstance(e, event_type))
        ).subscribe(responder)
        self._disposables.append(unregister)

    def notify(self, event):
        self.subject.on_next(event)

    def unregister(self):
        for unreg in self._disposables:
            unreg.dispose()