import random

import config
from classes.command import command
from classes.module import Module


class Profile(Module):
    """
    Commands related to your profile.
    """

    def __init__(self, handler):
        self.handler = handler

    @command(description="Change your name.", usage="username <name>")
    def username(self, ctx, username: str):
        """
        Change your name. It should not contain spaces.
        Can't think of one? Why not stick to your old name?
        """
        self.handler.character.name = username
        ctx.print("Changed your name.")

    @command(description="See your profile.", usage="profile")
    def profile(self, ctx):
        """
        See your (hopefully amazing) profile.
        Even if it's not amazing, you can always make it better!
        """
        character = self.handler.character
        ctx.print(self.handler.character.name)
        sword = character.equipped_sword
        shield = character.equipped_shield
        ctx.print(f"Level: {character.level}")
        ctx.print(f"XP: {character.xp}")
        ctx.print(f"Coins: {character.coins}")
        ctx.print(f"Sword: {sword.name} ({sword.action} {sword.level})")
        ctx.print(f"Shield: {shield.name} ({shield.action} {shield.level})")

    @command(description="Get more information on levels.", usage="level")
    def level(self, ctx):
        """
        Get more information on levels.
        You definitely wanna know when you're gonna reach the next level, no?
        """
        for index, value in enumerate(config.levels):
            ctx.print(f"Level {index + 1} - {value} XP")

    @command(description="View your inventory.", usage="inventory")
    def inventory(self, ctx):
        """
        View your inventory of amazing stuff.
        Nothing much yet? Get some from adventures!
        """
        for index, value in enumerate(self.handler.character.items):
            if index in [
                self.handler.character._equipped_sword,
                self.handler.character._equipped_shield,
            ]:
                equipped = " (equipped)"
            else:
                equipped = ""
            ctx.print(
                f"{index + 1}. {value.name} ({value.action} {value.level}){equipped}"
            )

    @command(description="Equip an item.", usage="equip <number>")
    def equip(self, ctx, number: int):
        """
        Equip an item. The number of the item must be specified.
        You can find the full list of items you have using the "inventory" command.
        """
        if number <= 0 or number > len(self.handler.character.items):
            return ctx.print('Oops! Invalid item. View all items with "inventory".')
        number -= 1
        self.handler.character.equip_item(number)
        ctx.print("Equipped the item.")

    @command(description="Sell an item.", usage="sell <number>")
    def sell(self, ctx, number: int):
        """
        Sell an item for coins.
        Amount will be random but partially dependent on the level of the item.
        """
        if number <= 0 or number > len(self.handler.character.items):
            return ctx.print('Oops! Invalid item. View all items with "inventory".')
        number -= 1
        if number in [
            self.handler.character._equipped_sword,
            self.handler.character._equipped_shield,
        ]:
            return ctx.print("Oops! You cannot sell an equipped item.")
        item = self.handler.character.items[number]
        min_amount = item.level * 2
        max_amount = item.level * 3
        amount = random.randint(min_amount, max_amount)
        self.handler.character.add_coins(amount)
        self.handler.character.remove_item(number)
        ctx.print(f"Sold the item for {amount} coins.")

    @command(description="Upgrade an item.", usage="upgrade <number>")
    def upgrade(self, ctx, number: int):
        """
        Increase an item's attack or defense by 1.
        This will cost you current attack/defense * 2 coins.
        """
        if number <= 0 or number > len(self.handler.character.items):
            return ctx.print('Oops! Invalid item. View all items with "inventory".')
        number -= 1
        coins = self.handler.character.items[number].level * 2
        if coins > self.handler.character.coins:
            return ctx.print("Oops! You do not have enough coins to upgrade this item.")
        self.handler.character.remove_coins(coins)
        self.handler.character.items[number].add_level(1)
        ctx.print(f"Upgraded the item and it costed you {coins} coins.")


def setup(handler):
    handler.add_module(Profile(handler))
