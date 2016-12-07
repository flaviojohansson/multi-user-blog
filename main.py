import jinja2
import webapp2

from app.handlers.signup import Register
from app.handlers.login import Login
from app.handlers.logout import Logout
from app.handlers.blog import Blog
from app.handlers.new_post import NewPost
from app.handlers.edit_post import EditPost
from app.handlers.view_post import ViewPost
from app.handlers.edit_comment import EditComment


app = webapp2.WSGIApplication([('/', Blog),
                               ('/signup', Register),
                               ('/login', Login),
                               ('/logout', Logout),
                               ('/post/new', NewPost),
                               ('/post/edit/([0-9]+)', EditPost),
                               ('/post/([0-9]+)', ViewPost),
                               ('/comment/edit/([0-9]+)/([0-9]+)', EditComment),
                               ],
                              debug=True)
