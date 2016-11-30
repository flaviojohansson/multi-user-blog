from app.base_handler import BaseHandler


class Logout(BaseHandler):
    def get(self):
        self.logout()
        self.redirect('/')
        