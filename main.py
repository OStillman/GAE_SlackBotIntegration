import jinja2
import os
import webapp2

template_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.getcwd())  # Get the templates in current directory
)

class MainPage(webapp2.RequestHandler):
    def post(self):
        recieved_data = self.request.get('challenge')
        template = template_env.get_template('auth.html')
        context = {
            'data': recieved_data,
        }
        self.response.out.write(template.render(context))


application = webapp2.WSGIApplication([('/', MainPage)], debug=True)  # Debug will be false when in production
