from google.appengine.ext import db
from app.base_handler import BaseHandler
from app.models.post import Post, blogs_key


class NewPost(BaseHandler):
    def get(self):
        if self.user:
            self.render("edit_post.html")
        else:
            self.redirect("/login")

    def post(self):
        if not self.user:
            self.redirect('/login')

        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            post = Post(parent=blogs_key(),
                        user_id=self.user.key(),
                        user_name=self.user.name,
                        subject=subject,
                        content=content)
            post.put()
            self.redirect('/blog/%s' % str(post.key().id()))
        else:
            error = "Subject and content, please!"
            self.render("edit_post.html",
                        subject=subject,
                        content=content,
                        error=error)


class EditPost(BaseHandler):
    def get(self, post_id):
        if not self.user:
            self.redirect("/login")

        key = db.Key.from_path('Post', int(post_id), parent=blogs_key())
        post = db.get(key)

        if not post:
            self.error(404)
            return

        self.render("edit_post.html",
                    post_id=post_id,
                    subject=post.subject,
                    content=post.content)

    def post(self, post_id):
        if not self.user:
            self.redirect('/login')
            return

        self.redirect('/signup')

        if self.request.get('action') == "delete":
            key = db.Key.from_path('Post', int(post_id), parent=blogs_key())
            post = db.get(key)

            # Make sure the logger user is the owner of the post
            if self.user.name != post.user_name:
                self.redirect('/blog')
                return

            post.delete()
            self.redirect('/blog')
            return

        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:

            key = db.Key.from_path('Post', int(post_id), parent=blogs_key())
            post = db.get(key)
            # TODO : Check if user is the owner of the post
            # TODO : Check if post found
            post.subject = subject
            post.content = content

            post.put()
            self.redirect('/blog/%s' % str(post.key().id()))
        else:
            error = "Subject and content, please!"
            self.render("edit_post.html",
                        subject=subject,
                        content=content,
                        error=error)
