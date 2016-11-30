from app.base_handler import BaseHandler


class Welcome(BaseHandler):
    '''
    '''
    def get(self):
        if self.user:
            self.redirect("/blog")
        else:
            self.render("welcome.html")
