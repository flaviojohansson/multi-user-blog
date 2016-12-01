from app.base_handler import BaseHandler
from app.models.post import Post


class Blog(BaseHandler):
    def get(self):
        if self.user:
            posts = Post.\
                    all().\
                    filter("user_name =", self.user.name).\
                    order('-created')

            self.render('front.html', posts=posts)
        else:
            self.redirect("/login")
