class InvertedIndex:
	key_store = dict()

	def __init__(self):
		return

	def put(self, key="", documentId=0):
		if key not in self.key_store:
			self.key_store[key] = [1, [documentId]]
		else:
			tup = self.key_store[key]
			tup[0] = tup[0] + 1
			tup[1].append(documentId)

	def get_size(self):
		return False

	def get(self, string=""):
		return self.key_store[string] if string in self.key_store else ()

	def serialize(self):
		s = "{"
		for key, val in self.key_store.items():
			s += "'" + str(key) + "':" + str(val) + ","
		s = s[:-1] + "}"
		return s

	def unserialize(self):
		return False




