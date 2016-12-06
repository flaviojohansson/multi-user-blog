import urllib
from google.appengine.ext import db
from app.base_handler import BaseHandler
from app.models.post import Post, blogs_key


class EditPost(BaseHandler):
    '''Edit post class.
    Users can only edit one's own post
    '''

    def get(self, post_id):
        # Not logged users are redirect to the login page and then
        # redirected back here
        if not self.user:
            self.redirect('/login?redirect=' +
                          urllib.pathname2url('/post/edit/' + post_id))
            return

        key = db.Key.from_path('Post', int(post_id), parent=blogs_key())
        post = db.get(key)

        if not post:
            self.error(404)
            return

        # Make sure the logged user is the owner of the post
        if self.user.name != post.user_name:
            self.redirect('/post/%s' % str(post_id))
            return

        self.render("edit_post.html",
                    post_id=post_id,
                    subject=post.subject,
                    content=post.content)

    def delete(self, post):
        post.delete()
        self.redirect('/')
        return

    def post(self, post_id):
        # Not logged users are redirected to the login page
        if not self.user:
            self.redirect('/login')
            return

        # Get the post itself
        key = db.Key.from_path('Post', int(post_id), parent=blogs_key())
        post = db.get(key)

        # Make sure the logged user is the owner of the post
        if self.user.name != post.user_name:
            self.redirect('/post/%s' % str(post.key().id()))
            return

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
