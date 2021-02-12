import random
from datetime import datetime, timedelta

import config
from classes.command import command
from classes.module import Module


class Adventure(Module):
    """
    Always be adventurous!
    """

    def __init__(self, handler):
        self.handler = handler

    @command(description="Get the list of adventures", usage="adventures")
    def adventures(self, ctx):
        """
        Get the full list of adventures.
        Hopefully you will find an adventure you like.
        """
        ctx.print("These are the adventures you can go on.")
        ctx.print("Success rate depends on difficulty of the adventure and your xp.")
        ctx.print('Use "adventure <number>" to begin on an adventure!')
        for i in range(len(config.adventure_names)):
            ctx.print_empty()
            ctx.print(f"{i + 1}. {config.adventure_names[i]}", indent=1)
            ctx.print(config.adventure_descriptions[i], indent=1)
            if i == 0:
                difficulty = "Very easy"
            elif i == 1:
                difficulty = "Easy"
            elif i == 2:
                difficulty = "Medium"
            elif i == 3:
                difficulty = "Hard"
            else:
                difficulty = "Very hard"
            ctx.print(f"Difficulty level: {difficulty}", indent=1)
            ctx.print(f"Duration: {config.adventure_durations[i]}", indent=1)
            success_rate = (
                config.adventure_chances[i] + self.handler.character.level * 5
            )
            if success_rate > 95:
                success_rate = 95
            ctx.print(f"Success rate: {success_rate}%", indent=1)

    @command(description="Go on an adventure!", usage="adventure <number>")
    def adventure(self, ctx, number: int):
        """
        Hooray! It is time to go on an adventure! Best of luck to you.
        Specify the adventure number which you can find using the "adventures" command/
        """
        if number <= 0 or number > len(config.adventure_names):
            return ctx.print(
                'Oops! Invalid adventure number. Use "adventures" to see all of them.'
            )
        if self.handler.character.adventure_end:
            return ctx.print(
                'Oops! You are already on an adventure. Check with "status".'
            )
        self.handler.character.adventure(number - 1)
        ctx.print("Going on an adventure... Good luck!")
        ctx.print(
            'Check the status of the adventure and collect rewards with "status".'
        )

    @command(description="Cancel the adventure.", usage="cancel")
    def cancel(self, ctx):
        """
        Cancel the adventure. This is irreversible!
        """
        if not self.handler.character.adventure_end:
            return ctx.print(
                "You are not on an adventure. Don't try to cancel nothing!"
            )
        self.handler.character.reset_adventure()
        ctx.print("Adventure has been cancelled. Be sure to start on a new one.")

    @command(description="Status of the adventure.", usage="status")
    def status(self, ctx):
        """
        Check the status of the adventure.
        This command should be used after completion of an adventure to receive rewards too.
        """
        if not self.handler.character.adventure_end:
            return ctx.print("You are not on an adventure yet!")
        if self.handler.character.adventure_end <= datetime.now():
            rand = random.randint(1, 100)
            success_rate = config.adventure_chances[self.handler.character.adventure_id]
            success_rate += self.handler.character.level * 5
            if success_rate > 95:
                success_rate = 95
            if rand > success_rate:
                ctx.print("RIP. You found nothing during the adventure.")
            else:
                _type = random.choice(["sword", "shield"])
                action = "attack"
                if _type == "shield":
                    action = "defense"
                min_level = (self.handler.character.adventure_id + 1) * 5
                max_level = min_level + 5
                level = random.randint(min_level, max_level)
                self.handler.character.add_item(_type, level)
                xp = random.randint(min_level, max_level) * 2
                self.handler.character.add_xp(xp)
                ctx.print(f"Congratulations! You gained {xp} XP.")
                ctx.print(f"You also got a new {_type} with {action} {level}.")
            self.handler.character.reset_adventure()
        else:
            remaining = self.handler.character.adventure_end - datetime.now()
            remaining -= timedelta(microseconds=remaining.microseconds)
            ctx.print(f"The time left till completion of the adventure is {remaining}.")


def setup(handler):
    handler.add_module(Adventure(handler))
