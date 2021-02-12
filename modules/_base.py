from classes.command import command
from classes.module import Module


class Base(Module):
    """
    This is where the description of the module goes.
    It will be shown in the help menu.
    """

    def __init__(self, handler):
        self.handler = handler

    @command(
        description="",
        usage="",
    )
    def _example(self, ctx):
        """
        This is where the long description for the command goes.
        It will be shown when help is used with this specific command.
        """
        pass


def setup(handler):
    handler.add_module(Base(handler))
