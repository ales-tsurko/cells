import asyncio
import re
from asyncio import subprocess

from cells import events
from cells.observation import Observation


class BackendRouter(Observation):
    # Collections of backends
    # this class keeps them in table, using their
    # commands as keys
    def __init__(self, event_loop, subject):
        super().__init__(subject)
        self.event_loop = event_loop
        self.backends = {}
        self.add_responder(events.view.track.New, self.track_new_responder)

    def track_new_responder(self, event):
        if event.template.run_command in self.backends:
            backend = self.backends[event.template.run_command]
            self.event_loop.create_task(
                backend.evaluate(event.template.setup_code))

            return
        backend = Backend(self.event_loop, event.template, self.subject)
        self.backends[event.template.run_command] = backend
        self.event_loop.create_task(backend.run())


class Backend(Observation):
    def __init__(self, event_loop, template, subject):
        super().__init__(subject)
        self.event_loop = event_loop
        self.template = template
        self.prompt_re = re.compile(template.command_prompt.encode("utf-8"),
                                    flags=re.MULTILINE)
        self.proc = None

    async def run(self):
        self.proc = await asyncio.create_subprocess_exec(
            *self.template.run_command.split(),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        output = await self.collect_output()
        self.notify(events.backend.Stdout(output))
        await self.evaluate(self.template.setup_code)
        # self.notify(events.backend.Ready(...))

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
