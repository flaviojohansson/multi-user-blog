import jinja2
import webapp2

from app.welcome import Welcome
from app.signup import Register
from app.login import Login
from app.logout import Logout
from app.blog import Blog
from app.new_post import NewPost, EditPost
from app.post_page import PostPage


APP = webapp2.WSGIApplication([('/', Welcome),
                               ('/signup', Register),
                               ('/login', Login),
                               ('/logout', Logout),
                               ('/blog', Blog),
                               ('/blog/newpost', NewPost),
                               ('/blog/edit/([0-9]+)', EditPost),
                               ('/blog/([0-9]+)', PostPage),
                               ],
                              debug=True)
