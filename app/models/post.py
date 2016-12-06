from google.appengine.ext import db
from app.base_handler import BaseHandler
import re


def blogs_key(name='default'):
    return db.Key.from_path('blogs', name)


class Post(db.Model):
    '''Post DataModel. Contains 3 extra attributes.

    Extra attributes:
        total_comments (int): The total of the comments of the post
        total_likes (int): The total of likes of the post
        liked (bool): Whether or not the user's already liked a post
    '''

    user_id = db.ReferenceProperty(required=True)
    user_name = db.StringProperty(required=True)
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    total_comments = 0
    total_likes = 0
    liked = False

    def format_content(self, content):
        '''Find URLs inside the text and converts into clickable links

        Parameters:
            content (string): Full text to search for URLs
        '''

        content = content.replace('\n', '<br>')
        urls = re.compile(r"((https?):((//)|(\\\\))+[\w\d:#@%/;$()~_?\+-=\\\.&]*)", 
                          re.MULTILINE | re.UNICODE)
        content = urls.sub(r'<a href="\1" target="_blank">\1</a>', content)
        return content

    def render(self, user):
        '''Render a single post, without comments.

        Parameters:
            user: The user DataModel object.
        '''

        # Convert the URL into clickable links
        self._render_text = self.format_content(self.content)

        # Class attribute with the total of comments
        if self.comments:
            self.total_comments = self.comments.count()
        # Class attribute with the total of likes
        if self.likes:
            self.total_likes = self.likes.count()
            if user:
                # Class attribute to whether or not the user has liked the post
                mylike = self.likes.filter('user_name =', user.name)
                self.liked = mylike.count() == 1

        # As long as this is a DataModel class, it doesn't
        # inherits BaseHandler self.user
        return BaseHandler.simple_render_str('post.html',
                                             p=self,
                                             user=user)
