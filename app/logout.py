from app.base_handler import BaseHandler


class Logout(BaseHandler):
    'Logout class'

    def get(self):
        # Clear the cookie and go to main page
        self.logout()
        self.redirect('/')
