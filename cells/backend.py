import asyncio
import re
from asyncio import subprocess

from cells import events
from cells.observation import Observation


class BackendRouter(Observation):
    def __init__(self, event_loop, subject):
        super().__init__(subject)
        self.event_loop = event_loop
        self.backends = {}

        self.add_responder(events.view.track.New, self.track_new_responder)
        self.add_responder(events.view.track.Remove,
                           self.track_remove_responder)
        self.add_responder(events.view.track.CellEvaluate,
                           self.cell_evaluate_responder)
        self.add_responder(events.view.code.Evaluate,
                           self.cell_evaluate_responder)

    def track_new_responder(self, event):
        template = event.template

        if template.run_command in self.backends:
            backend = self.backends[template.run_command]
            self.event_loop.create_task(backend.evaluate(template.setup_code))
            self.backends[template.run_command].increment_references()

            return

        backend = Backend(self.event_loop, template, self.subject)
        self.backends[template.run_command] = backend
        self.backends[template.run_command].increment_references()
        self.event_loop.create_task(backend.run())

    def track_remove_responder(self, event):
        template = event.template

        if template.run_command not in self.backends:
            return

        backend = self.backends[template.run_command]
        backend.decrement_references()

        if backend.references < 1:
            backend.stop()
            del self.backends[template.run_command]

    def cell_evaluate_responder(self, event):
        template = event.template
        if template.run_command not in self.backends:
            return

        backend = self.backends[template.run_command]
        self.event_loop.create_task(backend.evaluate(event.code))

    def delete(self):
        for backend in self.backends.values():
            backend.stop()


class Backend(Observation):
    def __init__(self, event_loop, template, subject):
        super().__init__(subject)
        self.event_loop = event_loop
        self.template = template
        self.prompt_re = re.compile(template.command_prompt.encode("utf-8"),
                                    flags=re.MULTILINE)
        self.proc = None
        self.references = 0

    async def run(self):
        if not self.template.run_command:
            return

        self.proc = await asyncio.create_subprocess_exec(
            *self.template.run_command.split(),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        output = await self.collect_output()
        self.notify(events.backend.Stdout(output))
        await self.evaluate(self.template.setup_code)
        # self.notify(events.backend.Ready(...))

    async def stop(self):
        if self.proc:
            self.proc.kill()

    async def evaluate(self, code):
        for line in code.encode("utf-8").splitlines():
            self.proc.stdin.write(line)
            self.proc.stdin.write(b"\n")
            await self.proc.stdin.drain()
            output = await self.collect_output()

            self.notify(events.backend.Stdout(output))

    async def collect_output(self):
        # self.notify(events.backend.Busy(...))
        # TODO Add timeout? But what if a user
        # wants to execute long-running process?
        data = b""

        while True:
            chunk = await self.proc.stdout.read(64)
            data += chunk

            if self.prompt_re.search(chunk) is not None:
                break

        data = self.prompt_re.sub(b"", data)
        result = data.strip().decode("utf-8")

        return result

    def increment_references(self):
        self.references += 1

    def decrement_references(self):
        self.references -= 1
