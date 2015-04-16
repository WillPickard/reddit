#exclusion_set = set(string.punctuation)
from invertedindex import InvertedIndex
class IndexSegment:
	inverted_index = None

	def __init__(self):
		self.inverted_index = InvertedIndex()

	def prepare_string(self, s=""):
		s = s.strip().lower()
		#s = "".join(c for c in s if c not in exclusion_set)

		return s

	def flush(self, to):
		return False

	def put(self, key="", documentId=0):
		prepared = self.prepare_string(key)
		for s in prepared.split():
			self.inverted_index.put(s, documentId)

	def get(self, s=""):
		res = set()
		for k in self.prepare_string(s).split():
			tup = self.inverted_index.get(k)
			#tup is a tuple with 
			#	0 - frequency of k in index 
			#	1 - array of ids
			if len(tup) == 2:
				ids = tup[1]

				res.update(ids)

		return res

	def has(self, s=""):
		return False

	def split(self):
		return False

	def merge(self, w):
		return False

	def serialize(self):
		s = "{"
		s += "'inverted_index':" + self.inverted_index.serialize()
		s += "}"
		return s

	def unserialize(self):
		return False