import urllib
from google.appengine.ext import db
from app.handlers.base_handler import BaseHandler
from app.models.post import Post
from app.lib.decorators import check_if_logged


class NewPost(BaseHandler):
    'Add new post class'

    @check_if_logged
    def get(self):
        self.render('edit_post.html')

    @check_if_logged
    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            post = Post(user=self.user,
                        subject=subject,
                        content=content)
            post.put()
            self.redirect('/post/%s' % str(post.key().id()))
        else:
            error = "Subject and content, please!"
            self.render("edit_post.html",
                        subject=subject,
                        content=content,
                        error=error)
