#comment.py
class Comment:
	author = ""
	#page = None
	post_url = ""
	score = 0
	date = ""
	body = ""
	id = 0
	type_ = "Comment"
	post_id = 0


	def __init__(self, post_url="", author="", date="", score=0, body="", id=0):
		self.author = author
		self.post_url = post_url
		#self.set_page(page)
		self.date = date
		self.score = score
		#self.set_soup(soup)
		self.body = body
		self.id = id



	def serialize(self):
		s = "{"
		s += "id:'" + str(self.id) + "',"
		s += "type_:'" + self.type_ + "',"
		s += "author:'" + self.author +"',"
		s += "date:'" + self.date + "',"
		s += "post_url:'" + self.post_url + "',"
	#	s += "page:'" + "-" + "',"
		#s += "date:'" + self.date + "',"
		s += "score:" + str(self.score) + ","
		s += "body:'" + self.body +  "',"
		s += "post_id:" + str(self.post_id) + ""
		s += "}"

		return s
	def unserialize(self):
		return False

 