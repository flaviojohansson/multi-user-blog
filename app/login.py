from app.base_handler import BaseHandler
from app.models.user import User


class Login(BaseHandler):
    '''
    '''
    def get(self):
        '''
        '''
        self.render("login.html")

    def post(self):
        username = self.request.get('username').lower()
        password = self.request.get('password')

        user = User.login(username, password)
        if user:
            self.login(user)
            self.redirect('/blog')
        else:
            msg = 'Invalid login'
            self.render('login.html', error=msg, username=username)
