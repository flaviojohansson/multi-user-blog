from google.appengine.ext import db
from app.base_handler import BaseHandler
import re


def blogs_key(name='default'):
    return db.Key.from_path('blogs', name)


class Post(db.Model):
    user_id = db.ReferenceProperty(required=True)
    user_name = db.StringProperty(required=True)
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    total_comments = 0
    total_likes = 0
    liked = False

    def render(self, user):
        self._render_text = self.content.replace('\n', '<br>')
        # Find URL inside the text and converts to clickable links
        urls = re.compile(r"((https?):((//)|(\\\\))+[\w\d:#@%/;$()~_?\+-=\\\.&]*)", 
                          re.MULTILINE | re.UNICODE)
        self._render_text = urls.sub(r'<a href="\1" target="_blank">\1</a>',
                                     self._render_text)
        if self.comments:
            self.total_comments = self.comments.count()
        if self.likes:
            self.total_likes = self.likes.count()
            mylike = self.likes.filter("user_name =", user.name)
            self.liked = mylike.count() == 1

        # As long as this is a DB class, it's calling a class method,
        # so it does not inherites BaseHandler user attribute
        return BaseHandler.simple_render_str("post.html",
                                             p=self,
                                             user=user)

