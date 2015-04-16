import requests 
from bs4 import BeautifulSoup as Soup
from datetime import datetime
import re
# from Models.user import User
# from Models.comment import Comment
# from Models.post import Post
from Models.page import Page

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

def get_time():
	return datetime.now().time().isoformat()

def serializeThing(thing):
	return thing.serialize()


class Reddit:
	base_url = "http://www.reddit.com"

	url_page_dictionary = {}
	pages = []
	subs = []
	users = []
	log = []
	url_queue = []

	def get_page(self, url):
		return Page(	soup = soup_getter(url),
						url = url
				)
		
	def is_subreddit_url(self, url):
		return url.find("/r/") > 0
	def is_subreddit_base_url(self, url):
		r = re.match("http://www.reddit.com/r/[A-Za-z0-9]*/", url)
		if r:
			return True
		return False

#bullshitting
	def load_subs(self):
		self.log_write(get_time() + " : " + "load_subs")
		base_soup = soup_getter(self.base_url + "/subreddits")
		for anchor in base_soup.find_all("a"):
			if anchor.has_attr("href") and self.is_subreddit_base_url(anchor["href"]):
				self.subs.append(anchor["href"])
			#if self.is_subreddit_url(anchor["href"]) and anchor.attrs["href"] and anchor["href"] not in self.subs:
			#	self.subs.append(anchor["href"])
		
	def flush_log(self, file_name):
		return False
	def log_write(self, msg):
		self.log.append(msg)

	def log_read(self, to_read=0):
		return self.log[0:to_read + 1]
	def log_last(self):
		return self.log_read();

	def forPageInSubs(self, callback):
		if len(self.subs) <= 0:
			self.load_subs()
		for i in range(len(self.subs)):
			page = Page(self.subs[i])
			if page:
				callback(page)	
