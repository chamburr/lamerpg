import random
from datetime import datetime

import config
from classes.item import Item


class Character:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.xp = 0
        self.coins = 100
        self.items = []
        self.adventure_id = None
        self.adventure_end = None
        self._equipped_sword = 0
        self._equipped_shield = 1

    @property
    def level(self):
        for xp in reversed(config.levels):
            if self.xp > xp:
                return config.levels.index(xp)
        return 0

    @property
    def equipped_sword(self):
        return self.items[self._equipped_sword]

    @property
    def equipped_shield(self):
        return self.items[self._equipped_shield]

    def add_xp(self, xp):
        self.xp += xp

    def remove_xp(self, xp):
        self.xp -= xp

    def add_coins(self, coins):
        self.coins += coins

    def remove_coins(self, coins):
        self.coins -= coins

    def add_item(self, _type, level):
        name = random.choice(config.item_names)
        item = Item(type=_type, name=name, level=level)
        self.items.append(item)

    def remove_item(self, index):
        if self._equipped_sword > index:
            self._equipped_sword -= 1
        if self._equipped_shield > index:
            self._equipped_shield -= 1
        self.items.pop(index)

    def equip_item(self, index):
        if self.items[index].type == "sword":
            self._equipped_sword = index
        else:
            self._equipped_shield = index

    def adventure(self, index):
        self.adventure_id = index
        duration = config.adventure_durations[index]
        self.adventure_end = datetime.now() + duration

    def reset_adventure(self):
        self.adventure_id = None
        self.adventure_end = None
