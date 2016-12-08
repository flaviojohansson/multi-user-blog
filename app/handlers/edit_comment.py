import urllib
from google.appengine.ext import db
from app.handlers.base_handler import BaseHandler
from app.models.post import Post
from app.lib.decorators import check_if_logged, check_if_owner, check_if_valid


class EditComment(BaseHandler):
    '''Edit comment class.
    Users can edit one's own post comments
    '''

    @check_if_logged
    @check_if_valid("Comment")
    @check_if_owner("Comment")
    def get(self, post_id, comment_id):
        # Not logged users are redirect to the login page and then
        # redirected back here
        if not self.user:
            self.redirect('/login?redirect=' +
                          urllib.pathname2url('/comment/edit/{}/{}'.format(
                              [str(post), str(comment_id)]
                          )))
            return

        key = db.Key.from_path('Comment', int(comment_id))
        comment = db.get(key)

        if not comment:
            self.error(404)
            return

        # Make sure the logged user is the owner of the post
        if self.user.key() != comment.user.key():
            self.redirect('/post/%s' % str(post_id))
            return

        self.render('edit_comment.html',
                    post_id=post_id,
                    content=comment.content)

    def delete(self, comment):
        post_id = comment.post.key().id()
        comment.delete()
        self.redirect('/post/%s' % str(post_id))
        return

    def post(self, post_id, comment_id):
        # Not logged users are redirected to the login page
        if not self.user:
            self.redirect('/login')
            return

        # Get the comment itself
        key = db.Key.from_path('Comment', int(comment_id))
        comment = db.get(key)

        if not comment:
            self.error(404)
            return

        # Make sure the logged user is the owner of the comment
        if self.user.key() != comment.user.key():
            self.redirect('/post/%s' % str(post_id))
            return

        # When the user clicks on the delete button the action becomes 'delete'
        if self.request.get('action') == 'delete':
            self.delete(comment)
            return

        # The default post method is update the comment
        content = self.request.get('content')

        if content:
            comment.content = content
            comment.put()
            self.redirect('/post/%s' % str(post_id))
        else:
            error = 'Please write something'
            self.render('edit_comment.html',
                        content=content,
                        error=error)
