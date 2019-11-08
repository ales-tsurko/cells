import re
import asyncio
from asyncio import subprocess

from cells.observation import Observation
from cells import events


class BackendRouter(Observation):
    # Collections of backends
    # this class keeps them in table, using their
    # commands as keys
    def __init__(self, subject):
        super().__init__(subject)


class Backend(Observation):
    def __init__(self, subject):
        super().__init__(subject)
        self.proc = None
        self.prompt_re = re.compile("sc3>".encode("utf-8"))

    async def run(self):
        self.proc = await asyncio.create_subprocess_exec(*"sclang".split(),
                                                    stdin=subprocess.PIPE,
                                                    stdout=subprocess.PIPE,
                                                    stderr=subprocess.PIPE)
        output = await self.collectOutput()
        self.notify(events.backend.Stdout(output))
        # self.notify(events.backend.Ready(...))

    async def evaluate(self, code):
        # self.proc.stdin.write(...)
        # collect output
        pass

    async def collectOutput(self):
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
        result = data.decode("utf-8")
        return result
