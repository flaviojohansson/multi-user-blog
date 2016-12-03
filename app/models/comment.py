from google.appengine.ext import db
from app.base_handler import BaseHandler
from app.models.post import Post


class Comment(db.Model):
    post = db.ReferenceProperty(Post, collection_name='comments')
    user_name = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)
