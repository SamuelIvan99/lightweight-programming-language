class Bindings:
    def __init__(self):
        self._stack = []

    def bind(self, name, mapping):
        self._stack.insert(0, (name, mapping))

    def lookup(self, name_to_find):
        scope_depth = []
        for result in self._stack:
            if result == "#":
                scope_depth.append(True)
            else:
                name, mapping = result
                if name == name_to_find:
                    return name, mapping

                if len(scope_depth) == self._stack.count("#"):
                    break
        return None

    def enter(self):
        self._stack.insert(0, "#")

    def exit(self):
        popped = []
        while len(self._stack) > 0 and self._stack[0] != "#":
            variable = self._stack.pop(0)
            popped.append(variable)
        if self._stack:
            self._stack.pop(0)
        return popped
