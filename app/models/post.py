from google.appengine.ext import db
from app.base_handler import BaseHandler


def blogs_key(name = 'default'):
    return db.Key.from_path('blogs', name)

class Post(db.Model):
    user_id = db.ReferenceProperty(required=True)
    user_name = db.StringProperty(required=True)
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return BaseHandler.simple_render_str("post.html", p=self)
