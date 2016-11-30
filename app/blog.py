'''
Module
'''
from app.base_handler import BaseHandler
from app.models.post import Post


class Blog(BaseHandler):
    def get(self):
        if self.user:
            posts = Post.all().order('-created')
            self.render('front.html', posts=posts)
        else:
            self.redirect("/login")
