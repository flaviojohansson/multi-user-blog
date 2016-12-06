import jinja2
import webapp2

from app.signup import Register
from app.login import Login
from app.logout import Logout
from app.blog import Blog
from app.new_post import NewPost
from app.edit_post import EditPost
from app.view_post import ViewPost
from app.edit_comment import EditComment


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
