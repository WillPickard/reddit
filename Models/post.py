#post.py

class Post:
	title = ""
	description = ""
	comments = []
	users = []
	author = ""
	url = ""
	score = 0
	id = 0

	def __init__(self, url="", description="", comments=[], users=[], author="", id=0, title="", score=0):
		self.url = url
		self.description = description
		self.comments = comments
		self.users = users
		self.author = author
		self.id = id
		self.title = title
		self.score = score

		#if not self.page and len(self.url) > 0:
		#	self.page = Page(url=self.url)#soup_getter(self.url)

	
	def serialize(self):
		s = "{" 
		s += "type: 'Post',"
		s += "url:'" + self.url + "',"
		s += "title:'" + self.title +"',"
		s += "description:'" + self.description +"',"
		s += "comments:" + str(map(lambda x : x.serialize(), self.comments)) +","
		s += "users:" + str(map(lambda x : x.user_name, self.users)) +","
		s += "score:" + str(self.score) + ","
		s += "author:'" + self.author + "'"
		s += "}"
		return s

	def unserialize(self):
		return False