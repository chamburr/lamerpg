class Item:
    def __init__(self, **kwargs):
        self.type = kwargs.get("type")
        self._name = kwargs.get("name")
        self.level = kwargs.get("level")

    def add_level(self, level):
        self.level += level

    @property
    def name(self):
        if self.type == "sword":
            return f"Sword of {self._name}"
        else:
            return f"Shield of {self._name}"

    @property
    def action(self):
        if self.type == "sword":
            return "attack"
        else:
            return "defense"
