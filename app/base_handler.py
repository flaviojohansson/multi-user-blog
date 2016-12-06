import os
import webapp2
import jinja2
import urllib
from app.lib.security import make_secure_val, check_secure_val
from app.models.user import User


class BaseHandler(webapp2.RequestHandler):
    '''Base handler class for all the requests
    Take care of rendering templates always sending the current user
    '''

    user = ""
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                                   autoescape=True)

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    @classmethod
    def simple_render_str(cls, template, **params):
        '''Renders a template directly.
        Can be used by Data models classes.
        '''

        jinja_template = cls.jinja_env.get_template(template)
        return jinja_template.render(params)

    def render_str(self, template, **params):
        jinja_template = self.jinja_env.get_template(template)

        # Not logged users can login and then get redirected to the current page
        baseurl = ''
        if not self.user:
            baseurl = urllib.pathname2url(self.request.path)

        # Always send the user to the templates
        return jinja_template.render(params, user=self.user, baseurl=baseurl)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def set_secure_cookie(self, name, val):
        cookie_val = make_secure_val(val)
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))

    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))
