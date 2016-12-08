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
    '''Make sure the entity exists
     Parameter:
        class_name: Datamodel name. e.g: Post, Comment'''

    def entity_exists(func):
        def func_wrapper(self, entity_id):

            key = db.Key.from_path(class_name, int(entity_id))
            entity = db.get(key)

            if entity:
                func(self, entity_id)  # Carry on
            else:
                self.redirect('/')  # Smoothly goes to main page
                return

        return func_wrapper
    return entity_exists


def check_if_owner(class_name):
    '''Make sure the logged user is the owner of the entity
    Parameter:
        class_name: Datamodel name. e.g: Post, Comment'''

    def is_user_the_owner(func):
        def func_wrapper(self, entity_id):

            key = db.Key.from_path(class_name, int(entity_id))
            entity = db.get(key)

            if self.user.key() == entity.user.key():
                func(self, entity_id)  # Carry on
            else:
                # Always back to the related Post page, even for comments
                self.redirect('/post/%s' % str(entity_id))
                return

        return func_wrapper
    return is_user_the_owner
