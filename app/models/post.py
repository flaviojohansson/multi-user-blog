from google.appengine.ext import db
from app.handlers.base_handler import BaseHandler
import re


def blogs_key(name='default'):
    return db.Key.from_path('blogs', name)


class Post(db.Model):
    'Post DataModel'

    user_id = db.ReferenceProperty(required=True)
    user_name = db.StringProperty(required=True)
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)

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

        # As long as this is a DataModel class, it doesn't
        # inherits BaseHandler self.user
        return BaseHandler.simple_render_str('post.html',
                                             p=self,
                                             user=user)
