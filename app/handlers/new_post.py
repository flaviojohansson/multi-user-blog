import urllib
from google.appengine.ext import db
from app.handlers.base_handler import BaseHandler
from app.models.post import Post, blogs_key


class NewPost(BaseHandler):
    'New post class'

    def get(self):
        # Not logged users are redirect to the login page and then
        # redirected back here
        if self.user:
            self.render('edit_post.html')
        else:
            self.redirect('/login?redirect=' + urllib.pathname2url('/post/new'))

    def post(self):
        # Not logged users are redirected to the login page
        if not self.user:
            self.redirect('/login')
            return

        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            post = Post(parent=blogs_key(),
                        user_id=self.user.key(),
                        user_name=self.user.name,
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
