import typing

from classes.command import command
from classes.module import Module


class General(Module):
    """
    Start the journey well...
    """

    def __init__(self, handler):
        self.handler = handler

    @command(description="Need help? Use this command.", usage="help [command]")
    def help(self, ctx, command: typing.Optional[str]):
        """
        Get the list of commands.
        If an argument is specified, get information for the specific command instead.
        """
        if command:
            command = self.handler.commands.get(command)
            if not command:
                return ctx.print(
                    'That command could not be found. Use "help" for a full list of commands.'
                )
            ctx.print(command.name)
            ctx.print_empty()
            ctx.print(f"Description:\n{command.long_description}", indent=1)
            ctx.print_empty()
            ctx.print(f"Usage:\n{command.usage}", indent=1)
            ctx.print_empty()
            ctx.print(f"Legend:\n<> Required argument\n[] Optional argument", indent=1)
        else:
            ctx.print(
                "Lame RPG is the lamest role-playing game ever invented by mankind."
            )
            ctx.print(
                'Note: For more information on a specific command, use "help <command>".'
            )
            for name, module in iter(self.handler.modules.items()):
                ctx.print_empty()
                ctx.print(name, indent=1)
                ctx.print(module.description, indent=1)
                for command in module.commands:
                    ctx.print_empty(indent=1)
                    ctx.print(command.name, indent=2)
                    ctx.print(command.description, indent=2)

    @command(description="Get some info about me.", usage="about")
    def about(self, ctx):
        """
        Very very very cool information about this game.
        Let me repeat, it is very very very VERY very cool.
        """
        ctx.print("Thank you for playing Lame RPG!")
        ctx.print("As you would expect, only the lamest person can make such a game.")
        ctx.print("Thus, this game is proudly created by Cen Han (2K). :D")
        ctx.print("Note: If you like this game, you are probably pretty lame too!")

    @command(description="Leave the game.", usage="exit")
    def exit(self, ctx):
        """
        Leave the game.
        I know the game is lame and this command will be used the most often, definitely.
        """
        pass


def setup(handler):
    handler.add_module(General(handler))
