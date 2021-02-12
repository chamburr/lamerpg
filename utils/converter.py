from classes.errors import BadArgument


def convert_to_bool(argument):
    argument = argument.lower()
    if argument in ("yes", "y"):
        return True
    elif argument in ("no", "n"):
        return False
    else:
        raise BadArgument()


def convert_to_int(argument):
    try:
        return int(argument)
    except (ValueError, TypeError):
        raise BadArgument()
