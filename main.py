import webapp2
import jinja2
from classes.main_page import MainPage
from classes.signup import Signup
from classes.signin import Signin


APP = webapp2.WSGIApplication([('/', MainPage),
                               ('/signup', Signup),
                               ('/signin', Signin),
                              ],
                              debug=True)
