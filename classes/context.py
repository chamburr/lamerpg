class Context:
    def __init__(self, **kwargs):
        self.message = kwargs.get("message")
        self.command = kwargs.get("command")

    def print(self, content, *, indent=0, **kwargs):
        if indent > 0:
            lines = content.split("\n")
            for line in lines:
                prefix = "| " * indent
                print(prefix + line, **kwargs)
        else:
            print(content, **kwargs)

    def print_empty(self, indent=0):
        if indent > 0:
            print("| " * indent)
        else:
            print()
