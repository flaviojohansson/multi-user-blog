import urllib
from google.appengine.ext import db
from app.base_handler import BaseHandler
from app.models.post import Post, blogs_key


class EditComment(BaseHandler):
    '''
    '''
    def get(self, post_id, comment_id):
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
        if self.user.name != comment.user_name:
            self.redirect('/post/%s' % str(post_id))
            return

        self.render('edit_comment.html',
                    post_id=post_id,
                    content=comment.content)

    def delete(self, comment):
        '''
        '''
        post_id = comment.post.key().id()
        comment.delete()
        self.redirect('/post/%s' % str(post_id))
        return

    def post(self, post_id, comment_id):
        if not self.user:
            self.redirect('/login')
            return

        # Get the comment itself
        key = db.Key.from_path('Comment', int(comment_id))
        comment = db.get(key)

        # Make sure the logged user is the owner of the comment
        if self.user.name != comment.user_name:
            self.redirect('/post/%s' % str(post_id))
            return

        # When the user clicks on the delete button the action becomes 'delete'
        if self.request.get('action') == "delete":
            self.delete(comment)
            return

        # The default operation is update the comment
        content = self.request.get('content')

        if content:
            comment.content = content
            comment.put()
            self.redirect('/post/%s' % str(post_id))
        else:
            error = "Please write something"
            self.render("edit_comment.html",
                        content=content,
                        error=error)
