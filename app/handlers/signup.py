import re
from app.handlers.base_handler import BaseHandler
from app.models.user import User


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")


def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")


def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')


def valid_email(email):
    return not email or EMAIL_RE.match(email)


class Signup(BaseHandler):
    'Signup Class'

    username = ''
    password = ''
    verify = ''
    email = ''

    def get(self):
        self.render('signup.html')

    def post(self):
        have_error = False
        self.username = self.request.get('username').lower()
        self.password = self.request.get('password')
        self.verify = self.request.get('verify')
        self.email = self.request.get('email')

        params = dict(username=self.username,
                      email=self.email)

        # Validate the values
        if not valid_username(self.username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not valid_password(self.password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif self.password != self.verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(self.email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.render('signup.html', **params)
        else:
            self.done()

    def done(self, *a, **kw):
        raise NotImplementedError


class Register(Signup):
    def done(self):
        # Make sure the user doesn't already exist
        user = User.by_name(self.username)
        if user:
            msg = 'That user already exists.'
            # Show the username, so users can check for typos
            params = dict(username=self.username,
                          email=self.email,
                          error_username=msg)
            self.render('signup.html', **params)
        else:
            # Save the user entity and redirects to main page
            user = User.register(self.username, self.password, self.email)
            user.put()
            self.login(user)
            self.redirect('/')
