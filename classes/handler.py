import importlib.util

from classes.character import Character
from classes.context import Context
from classes.errors import NotFound


class Handler:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.character = Character(name=self.name)
        self.modules = {}
        self.commands = {}

    def add_command(self, command):
        self.commands[command.name] = command

    def add_module(self, module):
        module.inject(self)
        self.modules[module.name] = module

    def load_module(self, name):
        spec = importlib.util.find_spec(name)
        lib = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(lib)
        setup = getattr(lib, "setup")
        setup(self)

    def invoke(self, message):
        command = message.split(" ")[0]
        command = self.commands.get(command)
        if not command:
            raise NotFound()
        ctx = Context(message=message, command=command)
        ctx.command.invoke(ctx)
