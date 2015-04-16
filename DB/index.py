#index.py
from indexsegment import IndexSegment

class Index:
	index_segments = dict()
	name = ""
	def __init__(self, name=""):
		self.name = name
		return

	def merge_segments(self, segment1, segment2):
		return False

	def split_segment(self, segment):
		return False

	def resize_segments(self):
		return False

	def test_segments(self):
		return False

	def add_index_segment(self, key, segment):
		self.index_segments[key] = segment

	def get_index_segment_for_prop(self, prop):
		key = prop[0]
		count = len(self.index_segments)
		if count is 0 or key not in self.index_segments:
			self.add_index_segment(key, IndexSegment())

		return self.index_segments[key]


	def flush(self, to):
		return False

	def put(self, prop, id):
		index_segment = self.get_index_segment_for_prop(prop)
		index_segment.put(prop, id)

	def get(self, q):
		res = set()
		index_segment = self.get_index_segment_for_prop(q)
		res.update(set(index_segment.get(q)))
		return res

	def has(self, q):
		return False

	def serialize(self):
		s = "{" 
		for c, segment in self.index_segments.items():
			s += "'" + c + "':" + segment.serialize() +","
		s = s[:-1] + "}"
		return s

	def unserialize(self):
		return False