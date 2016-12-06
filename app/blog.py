from app.base_handler import BaseHandler
from app.models.post import Post


class Blog(BaseHandler):
    '''Main page class.
    List all the posts for any user
    '''

    def get(self):
        posts = Post.\
                all().\
                order('-created')

        self.render('front.html', posts=posts)
