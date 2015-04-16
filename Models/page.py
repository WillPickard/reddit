#from post import Post
from post import Post
from comment import Comment
from user import User
from extractor import Extractor
from bs4 import BeautifulSoup as Soup
import requests

def soup_getter(url):
	headers = {
		'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36',
		'Connection' : 'keep-alive',
		'Referer' : 'https://www.google.com',
		'Cache-Control' : 'max-age=0',
		'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Encoding' : 'gzip, deflate, sdch',
		'Accept-Language' : 'en-US,en;q=0.8'
	}

	return Soup(requests.get(url, headers=headers).text)

class Page:
	url = ""
	soup = None
	comments = []
	users = []
	posts = []
	last_update = 0
	update_list = []
	title = ""
	id = 0

	def __init__(self, url="", soup=None, id=0, comments=[], users=[], posts=[], title=""):
		self.url = url
		self.soup = soup
		self.id = id
		self.comments = comments
		self.users = users
		self.posts = posts
		self.title = title

	def log_update(self):
		self.last_update = get_time()
		self.update_list.append(self.last_update)		

	def refresh(self):
		return False

	def set_soup(self, soup):
		if type(soup) != type(None):
			self.soup = soup


			self.log_update()

	def has_soup(self):
		return type(self.soup) != type(None)


	def set_url(self, url=""):
		if len(url) > 0:
			if self.url != url:
				self.set_soup(soup_getter(url))
			self.url = url

	def load_soup(self):
		if len(self.url) > 0:
			self.soup = soup_getter(self.url)

	def extract_comments(self):
		if self.has_soup():
			comments = self.soup.find_all("div", class_="comment") or []
			for comment in comments:
				extractor = Extractor(comment)
				
				author = extractor.extract_comment_author_user_name()
				post_url = "" #this needs to be set with the post in scope
				date = extractor.extract_comment_date()
				score = extractor.extract_comment_score()
				body = extractor.extract_comment_body()

				self.comments.append(Comment(
					author=author,
					post_url=post_url,
					date=date,
					score=score,
					body=body
				))

		return self.comments

	def extract_users(self):
		return []

	def extract_posts(self):
		if self.has_soup():
			raw_posts = self.soup.find_all("div", class_="entry") or []
			for post in raw_posts:
				#get the anchor whose href will be the post url
				anchor = post.find_all("a", class_="comments")
				if len(anchor) > 0 and anchor[0].has_attr("href"):
					#make sure we have an absolute url
					url = anchor[0]["href"] if anchor[0]["href"][:4] == "http" else "http://www.reddit.com" + anchor[0]["href"] 
					#make a new page to help wth extracting data
					page = Page(url=url)
					page.load_soup() 

					comments = page.extract_comments()
					for comment in comments:
						comment.post_url = url
					users = page.extract_users()
					title = page.extract_title()

					extractor = Extractor(page.soup)
					description = extractor.extract_post_description()
					author = extractor.extract_post_author_user_name()
					date = extractor.extract_post_date()
					score = extractor.extract_post_score()
					
					self.posts.append(Post(
						url=url, 
						description=description, 
						comments=comments, 
						users=users,
						author=author,
						title=title,
						score=score
					))
				break #testing only

		return self.posts

	def extract_title(self):
		if self.has_soup():
			self.title = self.soup.title.get_text()
		return self.title

	def serialize(self):
		return False
	def unserialize(self):
		return False


