from Models.user import User
from Models.comment import Comment
from Models.post import Post
from reddit import Reddit
from DB.database import Database

database_name = "reddit"

reddit = Reddit()
database = Database(name=database_name)


page = reddit.get_page("http://reddit.com/r/falcons")
posts = page.extract_posts()

for post in posts:
	database.put(post)

database.save()
