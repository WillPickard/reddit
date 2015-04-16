#extractor
class Extractor:
	soup = None
	
	def __init__(self, soup=None):
		self.soup = soup

	def has_soup(self):
		return True if self.soup else False

	def extract_post_score(self):
		score = 0
		#score is in .side .score .number.get_Text()
		if self.has_soup():
			for side in self.soup.find_all("div", class_="side"):
				for score in side.find_all("div", class_="score"):
					for number in score.find_all("span", class_="number"):
						#first one is the target the for loops are just to save typing,  this could be coded without them
						return int(number.get_text())
		return score

	def extract_post_description(self):
		description = ""
		if self.has_soup():
			#the post description is in #siteTable .entry .usertext-body
			siteTable = self.soup.find("div", id="siteTable")
			if siteTable:
				for post in siteTable.find_all("div", class_="entry"):
					usertext = post.find_all("div", class_="usertext-body")
					if len(usertext) > 0:
						description = usertext[0].get_text()
		return description

	def extract_post_date(self):
		date = ""
		if self.has_soup():
			#title is in #siteTable .entry time["datetime"]
			siteTable = self.soup.find("div", id="siteTable")
			if siteTable:
				for post in siteTable.find_all("div", class_="entry"):
					for date in siteTable.find_all("time"):
						if date.has_attr("datetime"):
							return date["datetime"]
		return date
	def extract_post_author_user_name(self):
		user_name = ""
		if self.has_soup():
			#user_name is in #siteTable .entry .author.get_text()
			siteTable = self.soup.find("div", id="siteTable")
			if siteTable:
				for post in siteTable.find_all("div", class_="entry"):
					for anchor in post.find_all("a", class_="author"):
						return anchor.get_text()
		return user_name


	def extract_comment_date(self):
		date = ""
		if self.has_soup():
			time = self.soup.find_all("time")
			if len(time) > 0 and time[0].has_attr("title"):
				date = time[0]["title"]
			

		return date	

	def extract_comment_author_user_name(self):
		author = ""
		if self.has_soup():
			author_anchor = self.soup.find_all("a", class_="author")
			if len(author_anchor) > 0 and author_anchor[0].has_attr("href"):
				author = author_anchor[0].get_text()
				
		return author


	def extract_comment_score(self):
		score = 0
		if self.has_soup():
			span = self.soup.find_all("span", class_="score unvoted")
			if len(span) > 0:
				score = int(span[0].get_text()
					.replace("points", "")
					.replace("point", ""))
		return score

	def extract_comment_body(self):
		body = ""
		if self.has_soup():
			body = self.soup.find_all("div", class_="usertext-body")
			if len(body) > 0:
				body = body[0].get_text()
		return body
