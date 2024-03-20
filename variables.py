class VariableStack:
	def __init__(self):
		self._stack = []

	def bind(self, name, type, value):
		self._stack.insert(0, (name, type, value))

	def lookup(self, name_to_find):
		for name, type in self._stack:
			if name == name_to_find:
				return name
		return None

	def enter(self):
		self._stack.insert(0, "#")

	def exit(self):
		variable = self._stack.pop(0)
		while len(self.stack) > 0 and variable != "#":
			variable = self._stack.pop(0)
