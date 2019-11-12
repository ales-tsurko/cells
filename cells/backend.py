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
        self.add_responder(events.view.track.Deserialized,
                           self.track_new_responder)
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
            backend.evaluate(template.setup_code)
            self.backends[template.run_command].increment_references()

            return

        backend = Backend(self.event_loop, template, self.subject)
        self.backends[template.run_command] = backend
        self.backends[template.run_command].increment_references()
        backend.run()

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
        backend.evaluate(event.code)

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

        self.stdin_middleware_re = None

        if len(template.backend_middleware.stdin.regex) > 1:
            self.stdin_middleware_re = re.compile(
                template.backend_middleware.stdin.regex, flags=re.MULTILINE)

        self.stdout_middleware_re = None

        if len(template.backend_middleware.stdout.regex) > 1:
            self.stdout_middleware_re = re.compile(
                template.backend_middleware.stdout.regex, flags=re.MULTILINE)

        self.proc = None
        self.references = 0
        self.evaluation_queue = []

        self.add_responder(events.app.Quit, self.app_quit_responder)

    def app_quit_responder(self, e):
        self.stop()

    def run(self):
        self.evaluation_queue.append(
            self.event_loop.create_task(self.run_task()))

    async def run_task(self):
        if not self.template.run_command or \
                self.proc and self.proc.returncode is None:

            return

        if len(self.evaluation_queue) > 1 and self.proc:
            await self.evaluation_queue.pop(0)

        self.proc = await asyncio.create_subprocess_shell(
            self.template.run_command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        output = await self.collect_output()
        self.notify(events.backend.Stdout(output))
        self.evaluate(self.template.setup_code)

    def stop(self):
        if self.proc:
            self.evaluation_queue.append(
                self.event_loop.create_task(self.stop_task()))

    async def stop_task(self):
        if len(self.evaluation_queue) > 1:
            await self.evaluation_queue.pop(0)
        self.proc.stdin.close()
        try:
            output = await asyncio.wait_for(self.proc.stdout.read(), 10)
            print(output.decode("utf-8"))
        except asyncio.futures.TimeoutError:
            print("Timeout on reading STDOUT after process stop")

    def evaluate(self, code):
        if len(code) < 1:
            # self.notify(events.backend.Ready(...))

            return

        if self.stdin_middleware_re:
            code = self.stdin_middleware_re.sub(
                self.template.backend_middleware.stdin.substitution, code)

        self.evaluation_queue.append(
            self.event_loop.create_task(self.evaluate_task(code)))

    async def evaluate_task(self, code):
        if len(self.evaluation_queue) > 1:
            await self.evaluation_queue.pop(0)

        for line in code.encode("utf-8").splitlines():
            self.proc.stdin.write(line)
            self.proc.stdin.write(b"\n")
            await self.proc.stdin.drain()
            output = await self.collect_output()

            self.notify(events.backend.Stdout(output))
            # self.notify(events.backend.Ready(...))

    async def collect_output(self):
        data = b""

        while True:
            try:
                chunk = await asyncio.wait_for(self.proc.stdout.read(64), 10)
                data += chunk
                print(data)

                if self.prompt_re.search(chunk) is not None:
                    break
            except asyncio.futures.TimeoutError:
                return "Error: timeout for reading STDOUT of backend " + \
                      f"{self.template.backend_name} with command " + \
                      f"`{self.template.run_command}`"

        print("have to be returned already")

        data = self.prompt_re.sub(b"", data)
        result = data.strip().decode("utf-8")

        if self.stdout_middleware_re:
            result = self.stdout_middleware_re.sub(
                self.template.backend_middleware.stdout.substitution, result)

        return result

    def increment_references(self):
        self.references += 1

    def decrement_references(self):
        self.references -= 1
