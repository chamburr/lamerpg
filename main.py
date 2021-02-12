import config
from classes.errors import BadArgument, NotFound
from classes.handler import Handler

print(
    """
 ██▓    ▄▄▄       ███▄ ▄███▓▓█████     ██▀███   ██▓███    ▄████
▓██▒   ▒████▄    ▓██▒▀█▀ ██▒▓█   ▀    ▓██ ▒ ██▒▓██░  ██▒ ██▒ ▀█▒
▒██░   ▒██  ▀█▄  ▓██    ▓██░▒███      ▓██ ░▄█ ▒▓██░ ██▓▒▒██░▄▄▄░
▒██░   ░██▄▄▄▄██ ▒██    ▒██ ▒▓█  ▄    ▒██▀▀█▄  ▒██▄█▓▒ ▒░▓█  ██▓
░██████▒▓█   ▓██▒▒██▒   ░██▒░▒████▒   ░██▓ ▒██▒▒██▒ ░  ░░▒▓███▀▒
░ ▒░▓  ░▒▒   ▓▒█░░ ▒░   ░  ░░░ ▒░ ░   ░ ▒▓ ░▒▓░▒▓▒░ ░  ░ ░▒   ▒
░ ░ ▒  ░ ▒   ▒▒ ░░  ░      ░ ░ ░  ░     ░▒ ░ ▒░░▒ ░       ░   ░
  ░ ░    ░   ▒   ░      ░      ░        ░░   ░ ░░       ░ ░   ░
    ░  ░     ░  ░       ░      ░  ░      ░                    ░

Welcome to Lame RPG - the lamest role-playing game ever invented by mankind!

It is very lame because it is made by Cen Han (2K). But even so, it is easy-to-play,
feature-rich, and it can probably entertain you for a while!

Ok, let's begin the journey! What's your name?
"""
)

name = input("Enter your name: ")

print(f'\nHey {name}, you\'re ready to go! Check out the list of commands with "help".')


handler = Handler(name=name)
handler.character.add_item("sword", 1)
handler.character.add_item("shield", 1)

for module in config.modules:
    handler.load_module(module)

while True:
    message = input("\n> ")
    command = message.split(" ")[0]
    print()
    if command == "exit":
        break
    try:
        handler.invoke(message)
    except NotFound:
        print('Oops! The command was not found. Use "help" to view all commands.')
    except BadArgument:
        print(
            f'Oops! You\'re using this command wrongly. Use "help {command}" for usage information.'
        )

print("Goodbye! See you next time...")
