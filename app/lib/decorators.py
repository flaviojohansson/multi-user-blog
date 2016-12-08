from google.appengine.ext import db


def check_if_logged(func):
    '''Not logged users are redirect to the login page and then
    redirected back to the original page'''

    def func_wrapper(self, *args):

        if self.user:
            func(self, *args)  # Carry on
        else:
            self.redirect('/login?redirect=' + self.base_url)
            return

    return func_wrapper


def check_if_valid(class_name):
    '''Make sure the entity exists, based on class_name and
    the last method parameter
     Parameter:
        class_name: Datamodel name. e.g: Post, Comment'''

    def wrapper(func):
        def func_wrapper(self, *args):
            # Always the last parameter. Being post or comment
            entity_id = args[-1]

            key = db.Key.from_path(class_name, int(entity_id))
            entity = db.get(key)

            if entity:
                func(self, *args)  # Carry on
            else:
                self.redirect('/')  # Smoothly goes to main page
                return

        return func_wrapper
    return wrapper


def check_if_owner(class_name):
    '''Make sure the logged user is the owner of the entity
    Parameter:
        class_name: Datamodel name. e.g: Post, Comment'''

    def wrapper(func):
        def func_wrapper(self, *args):

            # Always the last parameter. Being post or comment
            entity_id = args[-1]

            # In the other hand, the post_id is always the first
            post_id = args[0]

            key = db.Key.from_path(class_name, int(entity_id))
            entity = db.get(key)

            if self.user.key() == entity.user.key():
                func(self, *args)  # Carry on
            else:
                # Always back to the related Post page, even for comments
                self.redirect('/post/%s' % str(post_id))
                return

        return func_wrapper
    return wrapper
