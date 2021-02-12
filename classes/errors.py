class CommandError(Exception):
    def __init__(self):
        super().__init__()


class BadArgument(CommandError):
    pass


class NotFound(CommandError):
    pass
