from google.appengine.ext import db
from app.models.post import Post
from app.models.user import User


class Comment(db.Model):
    post = db.ReferenceProperty(Post, collection_name='comments')
    user = db.ReferenceProperty(User, required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)
