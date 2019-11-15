import asyncio
import os
import re
from asyncio import subprocess

from cells import events
from cells.model import standard_track_template_dir
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
        self.add_responder(events.view.editor.TrackRestartBackend,
                           self.track_restart_backend_responder)
        self.add_responder(events.view.editor.BackendRestartAll,
                           self.backend_restart_all_responder)

    def track_new_responder(self, event):
        self.new_backend_from_template(event.template)

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

    def track_restart_backend_responder(self, e):
        self.restart_backends_for_templates(e.templates)

    def backend_restart_all_responder(self, e):
        self.restart_backends_for_templates(e.templates)

    def restart_backends_for_templates(self, templates):
        run_commands = set()

        for template in templates:
            if template.run_command not in run_commands:
                run_commands.add(template.run_command)
                backend = self.backends.pop(template.run_command)
                backend.stop()
            self.new_backend_from_template(template)

    def new_backend_from_template(self, template):
        if template.run_command in self.backends:
            backend = self.backends[template.run_command]
            backend.evaluate(template.setup_code)
            self.backends[template.run_command].increment_references()

            return

        backend = Backend(self.event_loop, template, self.subject)
        self.backends[template.run_command] = backend
        self.backends[template.run_command].increment_references()
        backend.run(template.setup_code)

    def delete(self):
        for backend in self.backends.values():
            backend.stop()


class Backend(Observation):
    def __init__(self, event_loop, template, subject):
        super().__init__(subject)
        self.event_loop = event_loop
        self.template = template

        self.input_middleware_re = None

        if len(template.backend_middleware.input.regex) > 1:
            self.input_middleware_re = re.compile(
                template.backend_middleware.input.regex, flags=re.MULTILINE)

        self.output_middleware_re = None

        if len(template.backend_middleware.output.regex) > 1:
            self.output_middleware_re = re.compile(
                template.backend_middleware.output.regex, flags=re.MULTILINE)

        self.proc = None
        self.references = 0
        self.evaluation_queue = []
        self.pipe_task = None

        self.add_responder(events.app.Quit, self.app_quit_responder)

    def app_quit_responder(self, e):
        self.stop()

    def run(self, setup_code):
        self.evaluation_queue.append(
            self.event_loop.create_task(self.run_task(setup_code)))

    async def run_task(self, setup_code):
        if not self.template.run_command or \
                self.proc and self.proc.returncode is None:

            return

        if len(self.evaluation_queue) > 1 and self.proc:
            await self.evaluation_queue.pop(0)

        self.proc = await asyncio.create_subprocess_shell(
            self.template.run_command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=self.artifacts_path())
        self.pipe_task = asyncio.gather(
            self.pipe(self.proc.stdout,
                      lambda out: self.notify(events.backend.Stdout(out))),
            self.pipe(self.proc.stderr,
                      lambda out: self.notify(events.backend.Stderr(out))))
        self.evaluate(setup_code)
        # self.notify(events.backend.Ready(...))

    def stop(self):
        if self.proc:
            self.evaluation_queue.append(
                self.event_loop.create_task(self.stop_task()))

    async def stop_task(self):
        if len(self.evaluation_queue) > 1:
            await self.evaluation_queue.pop(0)
        self.proc.stdin.write_eof()
        try:
            await asyncio.wait_for(self.pipe_task, 10)
            self.notify(
                events.backend.Stdout(f"Quit {self.template.backend_name}."))
        except asyncio.futures.TimeoutError:
            print("Timeout on reading STDOUT after process stop")

    def evaluate(self, code):
        if len(code) < 1:
            return

        if self.input_middleware_re:
            code = self.input_middleware_re.sub(
                self.template.backend_middleware.input.substitution, code)

        print(code)

        self.evaluation_queue.append(
            self.event_loop.create_task(self.evaluate_task(code)))

    async def evaluate_task(self, code):
        if len(self.evaluation_queue) > 1:
            await self.evaluation_queue.pop(0)

        self.proc.stdin.write(code.encode("utf-8") + b"\n")
        await self.proc.stdin.drain()
        #  self.notify(events.backend.Ready(...))

    async def pipe(self, stream, callback=None):
        async for out in stream:
            out = out.rstrip().decode("utf-8")

            if self.output_middleware_re:
                out = self.output_middleware_re.sub(
                    self.template.backend_middleware.output.substitution, out)

            if callback:
                callback(out)

    def artifacts_path(self):
        regex = re.compile(r'[\W_]+', re.UNICODE)
        name = regex.sub("", self.template.backend_name).lower()
        path = os.path.join(artifacts_dir(), name)

        if not os.path.exists(path):
            os.makedirs(path)

        return path

    def increment_references(self):
        self.references += 1

    def decrement_references(self):
        self.references -= 1


def artifacts_dir():
    path = os.path.join(standard_track_template_dir(), "artifacts")

    if not os.path.exists(path):
        os.makedirs(path)

    return path
