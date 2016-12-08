import urllib
from google.appengine.ext import db
from app.handlers.base_handler import BaseHandler
from app.models.post import Post
from app.lib.decorators import check_if_logged, check_if_owner, check_if_valid


class EditPost(BaseHandler):
    '''Edit post class.
    Users can only edit one's own post'''

    @check_if_logged
    @check_if_valid("Post")
    @check_if_owner("Post")
    def get(self, post_id):

        key = db.Key.from_path('Post', int(post_id))
        post = db.get(key)

        self.render("edit_post.html",
                    post_id=post_id,
                    subject=post.subject,
                    content=post.content)

    def delete(self, post):
        # Delete all comments first
        for comment in post.comments:
            comment.delete()
        # Delete all likes second
        for like in post.likes:
            like.delete()
        # Delete the post itself
        post.delete()
        self.redirect('/')
        return

    @check_if_logged
    @check_if_valid("Post")
    @check_if_owner("Post")
    def post(self, post_id):

        # Get the post itself
        key = db.Key.from_path('Post', int(post_id))
        post = db.get(key)

        # When the user clicks on the delete button the action becomes 'delete'
        if self.request.get('action') == 'delete':
            self.delete(post)
            return

        # The default post method is update the post
        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            post.subject = subject
            post.content = content
            post.put()
            self.redirect('/post/%s' % str(post.key().id()))
        else:
            error = 'Subject and content, please!'
            self.render('edit_post.html',
                        subject=subject,
                        content=content,
                        error=error)
