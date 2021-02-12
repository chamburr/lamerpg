import random

from classes.command import command
from classes.module import Module


class Gambling(Module):
    """
    Gambling can be fun sometimes...
    """

    def __init__(self, handler):
        self.handler = handler

    @command(description="Flip the coin.", usage="flip <side> <amount>")
    def flip(self, ctx, side: str, amount: int):
        """
        Flip a coin! On success, you will get doubled the amount.
        Choose the side (either heads of tails) and amount of coins to bet.
        """
        if side not in ["heads", "tails"]:
            return ctx.print("Either choose heads or tails!")
        if amount <= 0 or amount > self.handler.character.coins:
            return ctx.print(
                f"Choose an amount between 1 and {self.handler.character.coins} coins."
            )
        rand = random.choice(["heads", "tails"])
        if rand == side:
            self.handler.character.add_coins(amount)
            ctx.print(f"Yay! It's {rand}! You won {amount} coins.")
        else:
            self.handler.character.remove_coins(amount)
            ctx.print(f"Uh oh! It's {rand}! You lost {amount} coins.")

    @command(description="Roll a dice", usage="roll <maximum> <tip> <amount>")
    def roll(self, ctx, maximum: int, tip: int, amount: int):
        """
        Roll a dice. You will get (maximum - 1) * amount coins on success.
        Choose the number of sides, your bet, and the amount of coins to bet.
        """
        if maximum < 2:
            return ctx.print("Oops! The dice needs at least 2 sides.")
        if tip < 1 or tip > maximum:
            return ctx.print("Oops! That is not a valid tip.")
        if amount <= 0 or amount > self.handler.character.coins:
            return ctx.print(
                f"Choose an amount between 1 and {self.handler.character.coins} coins."
            )
        rand = random.randint(1, maximum)
        if rand == tip:
            coins = (maximum - 1) * amount
            self.handler.character.add_coins(coins)
            ctx.print(f"Yay! You won {coins} coins.")
        else:
            self.handler.character.remove_coins(amount)
            ctx.print(f"Uh oh! You lost {amount} coins.")


def setup(handler):
    handler.add_module(Gambling(handler))
