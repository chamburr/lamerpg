import inspect
import typing

from classes.errors import BadArgument
from utils.converter import convert_to_bool, convert_to_int


class Command:
    def __init__(self, func, **kwargs):
        self.name = func.__name__
        self.callback = func
        self.params = inspect.signature(func).parameters.copy()
        self.long_description = inspect.getdoc(func)
        self.description = kwargs.get("description")
        self.usage = kwargs.get("usage")
        self.module = kwargs.get("module")

    def do_conversion(self, converter, argument):
        if not converter:
            return None
        elif converter is bool:
            return convert_to_bool(argument)
        elif converter is int:
            return convert_to_int(argument)
        elif converter is str:
            if argument is None:
                raise BadArgument()
            else:
                return argument
        else:
            try:
                origin = converter.__origin__
            except AttributeError:
                return None
            if origin == typing.Union:
                for conv in converter.__args__:
                    try:
                        return self.do_conversion(conv, argument)
                    except BadArgument:
                        continue
                raise BadArgument()

    def parse_arguments(self, ctx):
        ctx.arguments = [self.module, ctx]

        arguments = ctx.message.split(" ")[1:]

        iterator = iter(self.params.items())
        next(iterator)
        next(iterator)
        for index, value in enumerate(iterator):
            try:
                argument = arguments[index]
            except IndexError:
                argument = None
            converted = self.do_conversion(value[1].annotation, argument)
            ctx.arguments.append(converted)

    def invoke(self, ctx):
        self.parse_arguments(ctx)
        self.callback(*ctx.arguments)


def command(**kwargs):
    def decorator(func):
        return Command(func, **kwargs)

    return decorator
