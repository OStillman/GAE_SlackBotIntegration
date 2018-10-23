import jinja2
import os
import webapp2

template_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.getcwd())  # Get the templates in current directory
)

class MainPage(webapp2.RequestHandler):


application = webapp2.WSGIApplication([('/', MainPage)], debug=True) # Debug will be false when in production