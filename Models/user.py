#user.py

class User:
	user_name = ""
	comments = []
	comment_karma = 0
	link_karma = 0
	posts = []
	url = ""
	page = None
#	soup = None
#	id = 0

	def __init__(self, user_name="", comments=[], comment_karma=0, link_karma=0, posts = [], url="", page=None):
		self.user_name = user_name
		self.comments = comments,
		self.comment_karma = comment_karma
		self.link_karma = link_karma,
		self.posts = posts
		#self.soup = soup
		self.page = page
		self.url = url

		if not soup and len(self.url) > 0:
			self.page = Page(self.url)
		#	self.soup = self.page.soup

	def has_soup(self):
		return type(self.soup) is not type(None)

	def extract_user_name(self):
		if self.has_soup():
			if len(self.url) > 0:
				self.user_name = self.url.split("/")[-1]
			else:
				header = self.soup.find(id="header")
				if header:
					span = header.find_all("span", class_="pagename")
					if span:
						self.user_name = span[0].get_text()
		return self.user_name

	def extract_comments(self):
		if self.has_soup():
			url = self.url + "/" + "comments"
			page = Page(url)
			self.comments = page.extract_comments()

		return self.comments

	def extract_comment_karma(self):
		if self.has_soup():
			span = self.soup.find_all("div", class_="karma comment-karma")
			if len(span) > 0:
				self.comment_karma = span[0].get_text()

		return self.comment_karma

	def extract_link_karma(self):
		if self.has_soup():
			span = self.soup.find_all("div", class_="karma")
			if len(span) > 0:
				self.comment_karma = span[0].get_text()

		return self.link_karma

	def extract_posts(self):
		if self.has_soup():
			url = self.url + "/" + "submitted"
			page = Page(url)
			self.posts = page.extract_posts()

		return self.posts

	def serialze(self):
		return False
	def unserialize(self):
		return False