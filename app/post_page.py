from google.appengine.ext import db
from app.base_handler import BaseHandler
from app.models.post import Post, blogs_key
from app.models.comment import Comment


class PostPage(BaseHandler):
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blogs_key())
        post = db.get(key)

        if not post:
            self.error(404)
            return

        self.render("permalink.html", post=post)

    def post(self, post_id):
        # Only logged users can write comments
        if not self.user:
            self.redirect('/login')
            return

        # Get the post itself
        key = db.Key.from_path('Post', int(post_id), parent=blogs_key())
        post = db.get(key)

        content = self.request.get('content')
        if content:
            comment = Comment(post=post,
                              user_name=self.user.name,
                              content=content)
            comment.put()
            self.redirect('/blog/%s' % str(post.key().id()))
        else:
            error = "Please write something"
            self.render("permalink.html",
                        post=post,
                        error=error)
