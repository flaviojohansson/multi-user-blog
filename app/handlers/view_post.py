from google.appengine.ext import db
from app.handlers.base_handler import BaseHandler
from app.models.post import Post
from app.models.comment import Comment
from app.models.like import Like
from app.lib.decorators import check_if_logged, check_if_owner, check_if_valid


class ViewPost(BaseHandler):
    '''View post class.
    List the post itself and all its comments
    '''

    @check_if_valid
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id))
        post = db.get(key)
        self.render('view_post.html', post=post)

    def like(self, post):
        '''Like or Unlike the post.
        User can only like one time. The next time this function is called,
        it unlikes the Post
        '''

        # The owner of the post cannot like his own post
        if self.user.key() != post.user.key():
            # Check if the user already has liked the post
            mylike = post.likes.filter('user =', self.user.key())
            if mylike.count() > 0:
                # Unlike. Delete the like record
                for single_like in mylike:
                    single_like.delete()
            else:
                # Like. Insert the record
                like = Like(post=post,
                            user=self.user)
                like.put()

        self.redirect('/post/%s' % str(post.key().id()))
        return

    def comment(self, post):
        '''Add the comment to the post
        '''

        content = self.request.get('content')
        if content:
            comment = Comment(post=post,
                              user=self.user,
                              content=content)
            comment.put()
            self.redirect('/post/%s' % str(post.key().id()))
        else:
            error = 'Please write something'
            self.render('view_post.html',
                        post=post,
                        error=error)

    @check_if_logged
    @check_if_valid("Post")
    def post(self, post_id):
        # Get the post itself
        key = db.Key.from_path('Post', int(post_id))
        post = db.get(key)

        # When the user clicks on the like button the actions becomes 'like'
        if self.request.get('action') == 'like':
            self.like(post)
            return

        # The default post operation is comment the post
        self.comment(post)
