import random

from classes.command import command
from classes.module import Module
from utils.getch import getch


class Battle(Module):
    """
    The battle begins...
    """

    def __init__(self, handler):
        self.handler = handler

    @command(description="The deadly battle.", usage="battle <difficulty>")
    def battle(self, ctx, difficulty: int):
        """
        The deadly battle begins... Choose a difficulty between 1 and 5.
        Get coins when you succeed! The more difficult, the more coins you get.
        """
        if difficulty < 1 or difficulty > 5:
            return ctx.print("Please choose a difficulty between 1 and 5.")
        field = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ]
        boss_row = random.randint(0, 4)
        boss_column = random.randint(0, 4)
        field[boss_row][boss_column] = 1
        player_row = random.randint(0, 4)
        player_column = random.randint(0, 4)
        field[player_row][player_column] = 2
        if player_row == boss_row and player_column == boss_column:
            ctx.print("Oh, it looks like the boss is eager to fight with you.")
            ctx.print("They have come to you...")
        else:

            def print_field(field):
                ctx.print_empty()
                for row in field:
                    for column in row:
                        if column == 0:
                            ctx.print("•", end=" ")
                        elif column == 1:
                            ctx.print("X", end=" ")
                        else:
                            ctx.print("O", end=" ")
                    ctx.print_empty()

            move_speed = 6 - difficulty
            ctx.print("Before the battle starts, you need to catch the boss.")
            ctx.print(
                f"The boss will move every {move_speed} times you move to a random location."
            )
            ctx.print('You are represented "O" and the boss is represented by "X".')
            ctx.print(f"Use [w] [a] [s] [d] to move.")
            print_field(field)

            end = False
            moves = 0
            while not end:
                ctx.print("\nEnter a move: ", end="")
                try:
                    movement = getch().decode("utf-8").lower()
                except UnicodeDecodeError:
                    return ctx.print(
                        "Uh oh, you entered an invalid character. Battle ends..."
                    )
                ctx.print(f"{movement}")
                ctx.print_empty()
                if movement not in ["w", "a", "s", "d"]:
                    return ctx.print(
                        "Uh oh, you entered an invalid movement. Battle ends..."
                    )
                if (
                    (movement == "w" and player_row == 0)
                    or (movement == "a" and player_column == 0)
                    or (movement == "s" and player_row == 4)
                    or (movement == "d" and player_column == 4)
                ):
                    return ctx.print("Uh oh, you bumped into the wall. Battle ends...")
                field[player_row][player_column] = 0
                if movement == "w":
                    player_row -= 1
                elif movement == "a":
                    player_column -= 1
                elif movement == "s":
                    player_row += 1
                elif movement == "d":
                    player_column += 1
                if field[player_row][player_column] == 1:
                    end = True
                else:
                    field[player_row][player_column] = 2
                    print_field(field)
                    moves += 1
                    if moves == move_speed:
                        moves = 0
                        ctx.print_empty()
                        ctx.print("The boss is moving...")
                        field[boss_row][boss_column] = 0
                        boss_row = random.randint(0, 4)
                        boss_column = random.randint(0, 4)
                        while boss_row == player_row and boss_column == player_column:
                            boss_row = random.randint(0, 4)
                        field[boss_row][boss_column] = 1
                        print_field(field)
            ctx.print("You caught the boss!")
            ctx.print_empty()
        ctx.print("THE DEADLY BATTLE BEGINS...")
        ctx.print_empty()
        character = self.handler.character
        sword = character.equipped_sword
        shield = character.equipped_shield
        boss_hp = difficulty * 100
        player_hp = 100 + character.level * 10
        while boss_hp > 0 and player_hp > 0:
            ctx.print(f"Boss HP: {boss_hp}")
            ctx.print(f"Player HP: {player_hp}")
            ctx.print_empty()
            boss_damage = random.randint(difficulty * 15, difficulty * 20)
            player_damage = random.randint(sword.level * 10, sword.level * 15)
            player_shield = random.randint(shield.level * 5, shield.level * 10)
            effective_damage = boss_damage - player_shield
            if effective_damage < 5:
                effective_damage = 5
            ctx.print(f"The boss attacked and dealt {boss_damage} damage.")
            ctx.print(
                f"Because of your shield, effective damage was {effective_damage}."
            )
            player_hp -= effective_damage
            if player_hp < 0:
                break
            ctx.print("Press any key to attack...")
            getch()
            boss_hp -= player_damage
            ctx.print(f"You dealt {player_damage} damage.")
            ctx.print_empty()
        if boss_hp < 0:
            ctx.print("The boss was defeated!")
            xp = random.randint(difficulty * 15, difficulty * 20)
            coins = random.randint(difficulty * 15, difficulty * 20)
            self.handler.character.add_xp(xp)
            self.handler.character.add_coins(coins)
            ctx.print(f"You received {xp} XP and {coins} coins.")
        else:
            ctx.print("You were defeated! Better luck next time...")


def setup(handler):
    handler.add_module(Battle(handler))
