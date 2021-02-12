import inspect

from classes.command import Command


class ModuleMeta(type):
    def __new__(cls, *args):
        name, bases, attrs = args
        attrs["__module_name__"] = name

        commands = []
        new_cls = super().__new__(cls, name, bases, attrs)
        for base in reversed(new_cls.__mro__):
            for element, value in base.__dict__.items():
                if isinstance(value, Command):
                    commands.append(value)
        new_cls.commands = commands
        return new_cls


class Module(metaclass=ModuleMeta):
    def __new__(cls, *args):
        self = super().__new__(cls)
        return self

    def __init__(self, *args):
        super().__init__(*args)

    @property
    def name(self):
        return self.__module_name__

    @property
    def description(self):
        return inspect.getdoc(self)

    def inject(self, handler):
        for command in self.commands:
            command.module = self
            handler.add_command(command)
