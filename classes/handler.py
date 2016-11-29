import os
import webapp2
import jinja2


class Handler(webapp2.RequestHandler):
    '''

    '''
    template_dir = os.path.join(os.path.dirname(__file__), '../templates')
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                                   autoescape=True)

    def write(self, *a, **kw):
        '''
        '''
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        '''
        '''
        jinja_template = self.jinja_env.get_template(template)
        return jinja_template.render(params)

    def render(self, template, **kw):
        '''
        '''
        self.write(self.render_str(template, **kw))
