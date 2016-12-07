from app.handlers.base_handler import BaseHandler
from app.models.user import User


class Login(BaseHandler):
    'Login class'

    def get(self):
        if self.user:
            # If user is already logged, redirect to home page
            self.redirect('/')
        else:
            self.render("login.html")

    def post(self):
        username = self.request.get('username').lower()
        password = self.request.get('password')

        # Call class method to validade the login
        user = User.login(username, password)

        if user:
            self.login(user)
            # Redirect to the desired page when needed.
            redirect = self.request.get('redirect')
            self.redirect(redirect if redirect else '/')
        else:
            msg = "Invalid login"
            self.render('login.html', error=msg, username=username)
