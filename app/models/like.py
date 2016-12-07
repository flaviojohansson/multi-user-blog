from google.appengine.ext import db
from app.models.post import Post
from app.models.user import User


class Like(db.Model):
    post = db.ReferenceProperty(Post, collection_name='likes')
    user = db.ReferenceProperty(User, required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)
