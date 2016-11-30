from google.appengine.ext import db
from app.base_handler import BaseHandler
from app.models.post import Post, blogs_key


class PostPage(BaseHandler):
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blogs_key())
        post = db.get(key)

        if not post:
            self.error(404)
            return

        self.render("permalink.html", post=post)
