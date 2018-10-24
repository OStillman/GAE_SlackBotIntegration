import jinja2
import os
import webapp2
import logging
import json

template_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.getcwd())  # Get the templates in current directory
)


class MainPage(webapp2.RequestHandler):
    def post(self):
        data = json.loads(self.request.body)
        #data = json.loads(data)
        #logging.info("The data = " + str(data['challenge']))
        template = template_env.get_template('auth.html')
        context = {
            'data': data['challenge'],
        }
        self.response.out.write(template.render(context))


application = webapp2.WSGIApplication([('/', MainPage)], debug=True)  # Debug will be false when in production
