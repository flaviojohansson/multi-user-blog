from classes.handler import Handler


class Signup(Handler):
    '''
    '''
    def get(self):
        self.render("signup-form.html")
