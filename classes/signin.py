from classes.handler import Handler


class Signin(Handler):
    '''
    '''
    def get(self):
        self.render("signin-form.html")
